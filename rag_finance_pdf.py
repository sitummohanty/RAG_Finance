#!/usr/bin/env python3
"""
RAG System using Persistent Chroma DB for Multiple PDFs
Reads PDF documents from a folder and creates a searchable knowledge base
"""

import os
import sys
from pathlib import Path
from typing import List, Dict
import fitz  # PyMuPDF
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import HuggingFacePipeline
from langchain.chains import RetrievalQA
from transformers import pipeline


def load_financial_pdfs(root_folder: str) -> List[Dict[str, str]]:
    """
    Load all PDF files from the specified folder
    
    Args:
        root_folder: Path to folder containing PDF files
        
    Returns:
        List of dictionaries with 'source' and 'text' keys
    """
    documents = []
    pdf_folder = Path(root_folder)
    
    if not pdf_folder.exists():
        print(f"❌ Folder not found: {root_folder}")
        return documents
    
    pdf_files = list(pdf_folder.glob("*.pdf"))
    
    if not pdf_files:
        print(f"❌ No PDF files found in: {root_folder}")
        return documents
    
    print(f"📄 Found {len(pdf_files)} PDF files in {root_folder}")
    
    for pdf_path in pdf_files:
        try:
            doc = fitz.open(str(pdf_path))
            text = ""
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                text += page.get_text()
            
            doc.close()
            
            if text.strip():
                documents.append({
                    "source": str(pdf_path),
                    "text": text
                })
                print(f"  ✓ Loaded: {pdf_path.name} ({len(text)} chars)")
            else:
                print(f"  ⚠ Empty PDF: {pdf_path.name}")
                
        except Exception as e:
            print(f"  ❌ Error loading {pdf_path.name}: {e}")
    
    print(f"\n✅ Successfully loaded {len(documents)} PDF documents\n")
    return documents


def chunk_documents(documents: List[Dict[str, str]]) -> List[Document]:
    """
    Split documents into chunks for embedding
    
    Args:
        documents: List of document dictionaries
        
    Returns:
        List of LangChain Document objects
    """
    print("🔪 Chunking documents...")
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,  # Larger chunks for better context
        chunk_overlap=300,  # More overlap to preserve context
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""]  # Better split points
    )
    
    chunks = []
    for doc in documents:
        splits = text_splitter.split_text(doc["text"])
        for i, chunk in enumerate(splits):
            chunks.append(
                Document(
                    page_content=chunk,
                    metadata={
                        "source": doc["source"],
                        "chunk_id": i
                    }
                )
            )
    
    print(f"✅ Created {len(chunks)} text chunks\n")
    return chunks


def build_persistent_chroma(chunks: List[Document], persist_directory: str = "finance_chroma_db", force_rebuild: bool = False) -> Chroma:
    """
    Build or load a persistent Chroma vector database
    
    Args:
        chunks: List of document chunks
        persist_directory: Directory to persist the database
        force_rebuild: If True, rebuild database even if it exists
        
    Returns:
        Chroma vector store instance
    """
    print(f"🗄️  Building persistent Chroma DB at: {persist_directory}")
    
    # Initialize embeddings model
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )
    
    # Check if database already exists
    if os.path.exists(persist_directory) and not force_rebuild:
        print(f"  ℹ️  Found existing database, loading...")
        vectorstore = Chroma(
            persist_directory=persist_directory,
            embedding_function=embeddings
        )
        print(f"  ✓ Loaded existing database with {vectorstore._collection.count()} documents")
    else:
        if force_rebuild and os.path.exists(persist_directory):
            print(f"  ℹ️  Force rebuild requested, recreating database...")
            import shutil
            shutil.rmtree(persist_directory)
        else:
            print(f"  ℹ️  Creating new database...")
            
        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=persist_directory
        )
        print(f"  ✓ Created database with {len(chunks)} documents")
    
    print(f"✅ Chroma DB ready\n")
    return vectorstore


def build_rag(vectorstore: Chroma) -> RetrievalQA:
    """
    Build RAG chain with retriever and LLM
    
    Args:
        vectorstore: Chroma vector store
        
    Returns:
        RetrievalQA chain
    """
    from langchain.prompts import PromptTemplate
    
    print("🤖 Building RAG chain...")
    
    # Create retriever with better search parameters
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 5}  # Retrieve top 5 most relevant chunks
    )
    
    # Load local LLM with better parameters
    print("  ℹ️  Loading language model...")
    hf_pipeline = pipeline(
        "text2text-generation",
        model="google/flan-t5-base",  # Using larger base model for better accuracy
        max_length=512,
        temperature=0.3,  # Lower temperature for more focused answers
        do_sample=True,
        top_p=0.95
    )
    
    llm = HuggingFacePipeline(pipeline=hf_pipeline)
    
    # Create custom prompt template for better answers
    prompt_template = """Use the following pieces of context to answer the question at the end. 
If you don't know the answer based on the context, just say "I don't have enough information to answer this question."
Don't try to make up an answer. Be specific and detailed in your response.

Context:
{context}

Question: {question}

Detailed Answer:"""
    
    PROMPT = PromptTemplate(
        template=prompt_template, 
        input_variables=["context", "question"]
    )
    
    # Create RAG chain with custom prompt
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": PROMPT}
    )
    
    print("✅ RAG chain ready\n")
    return qa_chain


def main():
    """Main execution function"""
    print("=" * 60)
    print("  RAG System with Persistent Chroma DB")
    print("=" * 60)
    print()
    
    # Configuration - UPDATE THIS PATH TO YOUR PDF FOLDER
    pdf_folder = "finance_pdfs"  # Path to folder containing PDF files (relative or absolute)
    persist_dir = "finance_chroma_db"  # Database storage location
    force_rebuild = False  # Set to True to rebuild database with new chunking strategy
    
    # Load PDFs
    documents = load_financial_pdfs(pdf_folder)
    
    if not documents:
        print("❌ No documents loaded. Please add PDF files to the 'finance_pdfs' folder.")
        sys.exit(1)
    
    # Chunk documents
    chunks = chunk_documents(documents)
    
    # Build persistent vector database
    vectorstore = build_persistent_chroma(chunks, persist_dir, force_rebuild)
    
    # Build RAG chain
    qa_chain = build_rag(vectorstore)
    
    # Interactive query loop
    print("=" * 60)
    print("  Ready for Questions!")
    print("=" * 60)
    print("\nType your questions below (or 'quit' to exit)\n")
    
    while True:
        try:
            query = input("❓ Question: ").strip()
            
            if not query:
                continue
            
            if query.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!")
                break
            
            print("\n🔍 Searching and generating answer...\n")
            
            result = qa_chain({"query": query})
            
            print(f"💡 Answer: {result['result']}\n")
            
            if result.get('source_documents'):
                print("📚 Sources:")
                for i, doc in enumerate(result['source_documents'], 1):
                    source = doc.metadata.get('source', 'Unknown')
                    print(f"  {i}. {os.path.basename(source)}")
                
                # Option to see retrieved context
                show_context = input("\n👁️  Show retrieved context? (y/n): ").strip().lower()
                if show_context == 'y':
                    print("\n" + "="*60)
                    print("Retrieved Context:")
                    print("="*60)
                    for i, doc in enumerate(result['source_documents'], 1):
                        print(f"\n[Chunk {i} from {os.path.basename(doc.metadata.get('source', 'Unknown'))}]")
                        print(f"{doc.page_content[:500]}...")  # Show first 500 chars
                    print("="*60)
                print()
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")


if __name__ == "__main__":
    main()
