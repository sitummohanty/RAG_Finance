# How to Recreate Chroma Database

## 📊 Quick Reference Guide

### **Method 1: Use the Force Rebuild Flag (Recommended)**

Edit line 237 in `rag_finance_pdf.py`:

```python
force_rebuild = True  # Set to True to rebuild database
```

Then run:
```bash
python3 /Users/sitummohanty/Desktop/rag_finance_pdf.py
```

**When to use**: After changing chunking parameters, embeddings model, or adding/removing PDFs

---

### **Method 2: Delete Database Folder**

From terminal:
```bash
rm -rf finance_chroma_db
```

Or from Desktop if you're there:
```bash
rm -rf /Users/sitummohanty/finance_chroma_db
```

Then run the script normally - it will recreate the database.

**When to use**: Quick manual cleanup

---

### **Method 3: Change Database Name**

Edit line 238 in `rag_finance_pdf.py`:

```python
persist_dir = "finance_chroma_db_v2"  # New name
```

**When to use**: Want to keep old database for comparison

---

## 🔄 When Should You Recreate the Database?

| Scenario | Recreate? | Why? |
|----------|-----------|------|
| ✏️ Changed chunking parameters (size, overlap) | ✅ Yes | Chunks are different |
| 📝 Added/removed PDFs | ✅ Yes | Document set changed |
| 🧠 Changed embedding model | ✅ Yes | Vector representations differ |
| 🤖 Changed LLM model | ❌ No | Database is independent |
| ⚙️ Changed retrieval parameters (k value) | ❌ No | Only affects search |
| 📄 Changed prompt template | ❌ No | Only affects generation |

---

## 💡 Current Configuration

Your current settings (optimal for accuracy):

```python
# Chunking (line 84-87)
chunk_size = 1500        # Larger chunks = more context
chunk_overlap = 300      # More overlap = better continuity

# Retrieval (line 172)
search_kwargs = {"k": 5}  # Retrieve top 5 chunks

# Model (line 177)
model = "google/flan-t5-base"  # Better accuracy than small
```

---

## 🚀 Quick Commands

**Delete and rebuild:**
```bash
rm -rf finance_chroma_db && python3 /Users/sitummohanty/Desktop/rag_finance_pdf.py
```

**Check database location:**
```bash
ls -lh finance_chroma_db/
```

**Check database size:**
```bash
du -sh finance_chroma_db/
```

---

## ✅ Success Indicators

After recreation, you should see:
```
🗄️  Building persistent Chroma DB at: finance_chroma_db
  ℹ️  Force rebuild requested, recreating database...
  ✓ Created database with XXXX documents
✅ Chroma DB ready
```

Where XXXX is the number of chunks (currently 1,711 for your 40 PDFs).

---

## 🐛 Troubleshooting

**Database not recreating?**
1. Check `force_rebuild = True` is set
2. Verify database folder location
3. Check file permissions

**Out of memory?**
- Reduce `chunk_size` to 1000
- Reduce `k` value to 3
- Close other applications

**Slow recreation?**
- Normal for first time (building embeddings)
- Subsequent loads are fast
- Consider smaller embedding model if needed
