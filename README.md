# 📚 RAG Finance System with Persistent Chroma DB

A Retrieval-Augmented Generation (RAG) system that reads multiple PDF documents and creates an intelligent Q&A system using persistent vector database storage.

## 🌟 Features

- **Multi-PDF Support**: Load and process multiple PDF documents from a folder
- **Persistent Storage**: Uses Chroma DB for persistent vector storage - no need to reprocess PDFs every time
- **Smart Chunking**: Advanced text splitting with optimal chunk size and overlap
- **Accurate Retrieval**: Retrieves top 5 most relevant document chunks for each query
- **Local LLM**: Uses Google's FLAN-T5-Base model for high-quality answer generation
- **Context Visibility**: Option to view retrieved context for transparency
- **Interactive CLI**: Simple command-line interface for asking questions

## 🎯 Use Cases

- Financial document Q&A
- Research paper analysis
- Technical documentation search
- Educational material comprehension
- Any multi-document knowledge base

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/rag-finance-system.git
   cd rag-finance-system
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your PDF folder**
   ```bash
   mkdir finance_pdfs
   # Copy your PDF files to this folder
   ```

4. **Configure the path** (Optional)
   
   Edit line 237 in `rag_finance_pdf.py`:
   ```python
   pdf_folder = "/path/to/your/pdf/folder"
   ```

5. **Run the system**
   ```bash
   python rag_finance_pdf.py
   ```

## 📖 Usage

### Basic Usage

```bash
python rag_finance_pdf.py
```

The system will:
1. Load all PDFs from the configured folder
2. Create/load the persistent Chroma database
3. Download the LLM model (first time only)
4. Start an interactive Q&A session

### Example Session

```
============================================================
  RAG System with Persistent Chroma DB
============================================================

📄 Found 40 PDF files in /path/to/pdfs
  ✓ Loaded: document1.pdf (15000 chars)
  ✓ Loaded: document2.pdf (23000 chars)
  ...

✅ Successfully loaded 40 PDF documents

🔪 Chunking documents...
✅ Created 1711 text chunks

🗄️  Building persistent Chroma DB at: finance_chroma_db
  ✓ Created database with 1711 documents
✅ Chroma DB ready

🤖 Building RAG chain...
✅ RAG chain ready

============================================================
  Ready for Questions!
============================================================

❓ Question: What is NPS?

🔍 Searching and generating answer...

💡 Answer: National Pension System (NPS) is a retirement savings program 
that provides an adequate retirement income to everyone.

📚 Sources:
  1. NPS.pdf
  2. NPS_guide.pdf

👁️  Show retrieved context? (y/n): 
```

## 🔧 Configuration

### Key Parameters

Edit these in `rag_finance_pdf.py`:

```python
# Line 237-239: Basic Configuration
pdf_folder = "/path/to/pdfs"           # Your PDF folder path
persist_dir = "finance_chroma_db"       # Database storage location
force_rebuild = False                   # Set True to rebuild database

# Line 84-87: Chunking Strategy
chunk_size = 1500                       # Characters per chunk
chunk_overlap = 300                     # Overlap between chunks

# Line 172: Retrieval
search_kwargs = {"k": 5}                # Number of chunks to retrieve

# Line 177: Model Selection
model = "google/flan-t5-base"           # LLM model to use
```

## 🗄️ Database Management

### Recreate Database

**Method 1: Use Force Rebuild Flag**
```python
force_rebuild = True  # In main() function
```

**Method 2: Delete Database Manually**
```bash
rm -rf finance_chroma_db
```

**Method 3: Change Database Name**
```python
persist_dir = "finance_chroma_db_v2"
```

### When to Recreate

- ✅ After changing chunking parameters
- ✅ After adding/removing PDFs
- ✅ After changing embedding model
- ❌ Not needed for LLM model changes
- ❌ Not needed for retrieval parameter changes

## 📊 Performance

| Metric | Value |
|--------|-------|
| Model Size | ~990MB (FLAN-T5-Base) |
| Embedding Model | all-MiniLM-L6-v2 (384 dimensions) |
| Typical Query Time | 2-5 seconds |
| Memory Usage | ~2-3GB RAM |
| Storage | ~50-100MB for database (depends on PDFs) |

## 🎓 Model Options

You can change the LLM model for different accuracy/speed trade-offs:

| Model | Size | Accuracy | Speed | Memory |
|-------|------|----------|-------|--------|
| flan-t5-small | 80MB | ⭐⭐ | ⚡⚡⚡ | 🟢 Low |
| flan-t5-base | 990MB | ⭐⭐⭐⭐ | ⚡⚡ | 🟡 Medium |
| flan-t5-large | 3GB | ⭐⭐⭐⭐⭐ | ⚡ | 🔴 High |

**Current configuration**: `flan-t5-base` (recommended balance)

## 🛠️ Technical Stack

- **PDF Processing**: PyMuPDF (fitz)
- **Text Chunking**: LangChain RecursiveCharacterTextSplitter
- **Embeddings**: HuggingFace Sentence Transformers
- **Vector Database**: Chroma DB (persistent)
- **LLM**: Google FLAN-T5 via HuggingFace Transformers
- **Orchestration**: LangChain

## 📁 Project Structure

```
rag-finance-system/
├── rag_finance_pdf.py          # Main application
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── .gitignore                   # Git ignore rules
├── finance_pdfs/                # Your PDF documents (not tracked)
└── finance_chroma_db/           # Persistent database (not tracked)
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- LangChain for the RAG framework
- Chroma for the vector database
- HuggingFace for models and embeddings
- Google for FLAN-T5 models

## 📧 Contact

Your Name - [@your_twitter](https://twitter.com/your_twitter)

Project Link: [https://github.com/YOUR_USERNAME/rag-finance-system](https://github.com/YOUR_USERNAME/rag-finance-system)

## 🔮 Future Enhancements

- [ ] Web interface with Streamlit/Gradio
- [ ] Support for more document formats (DOCX, TXT, etc.)
- [ ] Multi-language support
- [ ] Query history and conversation memory
- [ ] Batch query processing
- [ ] REST API endpoint
- [ ] Docker containerization
- [ ] Cloud deployment support

---

Made with ❤️ using Python and LangChain
