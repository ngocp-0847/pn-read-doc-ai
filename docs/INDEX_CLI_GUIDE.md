# 📚 Index CLI Guide - dsRAG Search & List-Docs

## 🎯 Tổng quan

Index CLI là công cụ mạnh mẽ để quản lý knowledge base sử dụng dsRAG (Document-Structured Retrieval-Augmented Generation). Tool này cung cấp khả năng index documents, tìm kiếm semantic, và liệt kê documents đã được index.

## 🚀 Tính năng chính

### 🔍 Search (Tìm kiếm)
- **Semantic Search**: Tìm kiếm dựa trên ý nghĩa, không chỉ từ khóa
- **Relevance Scoring**: Đánh giá độ liên quan của kết quả
- **Configurable Parameters**: Tùy chỉnh số kết quả, ngưỡng relevance
- **Multiple Storage Support**: Hỗ trợ nhiều storage directory

### 📋 List-Docs (Liệt kê Documents)
- **Document Inventory**: Xem danh sách documents đã index
- **Knowledge Base Info**: Thông tin chi tiết về knowledge base
- **Storage Status**: Kiểm tra trạng thái storage
- **Query Validation**: Xác minh khả năng query

## 📦 Cài đặt

```bash
# Cài đặt dependencies
pip install -r requirements.txt

# Thiết lập OpenAI API Key
export OPENAI_API_KEY="your-openai-api-key"

# Setup storage directory
make index-setup
```

## 🛠️ Sử dụng

### 1. Index Documents

```bash
# Index cơ bản
python3 index_cli.py index --folder markdown_files --project-name "MyProject"

# Index với storage tùy chỉnh
python3 index_cli.py index --folder markdown_files --project-name "MyProject" --storage-dir "./custom_storage"

# Index với test query
python3 index_cli.py index --folder markdown_files --test-query "software development"

# Force reindex
python3 index_cli.py index --folder markdown_files --force-reindex
```

### 2. Search Documents

```bash
# Tìm kiếm cơ bản
python3 index_cli.py search --query "software development estimation"

# Tìm kiếm với số kết quả tùy chỉnh
python3 index_cli.py search --query "database design" --max-results 10

# Tìm kiếm với storage tùy chỉnh
python3 index_cli.py search --query "API development" --storage-dir "./custom_storage"

# Tìm kiếm với OpenAI key trực tiếp
python3 index_cli.py search --query "microservices" --openai-key "sk-..."
```

### 3. List Documents

```bash
# Liệt kê documents cơ bản
python3 index_cli.py index --folder markdown_files --list-docs

# Liệt kê với project name
python3 index_cli.py index --folder markdown_files --project-name "MyProject" --list-docs

# Liệt kê với storage tùy chỉnh
python3 index_cli.py index --folder markdown_files --storage-dir "./custom_storage" --list-docs
```

## 📋 Makefile Commands

### Search Commands
```bash
# Tìm kiếm cơ bản
make index-search QUERY="software development estimation"

# Tìm kiếm với số kết quả tùy chỉnh
make index-search QUERY="database design" MAX_RESULTS=10

# Tìm kiếm với storage tùy chỉnh
make index-search QUERY="API development" STORAGE_DIR="./custom_storage"
```

### List Commands
```bash
# Liệt kê documents
make index-list FOLDER=markdown_files

# Liệt kê với project name
make index-list FOLDER=markdown_files PROJECT=MyProject

# Test knowledge base
make index-test FOLDER=markdown_files TEST_QUERY="software development"
```

### Setup Commands
```bash
# Setup storage
make index-setup

# Help
make index-help
```

## 🔧 Cấu hình Search Parameters

### RSE Parameters (Retrieval Search Engine)

```python
rse_params = {
    "max_length": 5,                    # Số kết quả tối đa
    "overall_max_length": 10,           # Tổng độ dài tối đa
    "minimum_value": 0.7,               # Ngưỡng relevance tối thiểu
    "irrelevant_chunk_penalty": 0.3     # Penalty cho chunks không liên quan
}
```

### Embedding Configuration

```python
embedding_config = {
    "model": "text-embedding-3-small",  # OpenAI embedding model
    "dimensions": 1536,                 # Vector dimensions
    "normalize": True                   # Normalize vectors
}
```

### Reranker Configuration

```python
reranker_config = {
    "model": "CohereReranker",         # Cohere reranking model
    "top_k": 10,                       # Top k results to rerank
    "threshold": 0.7                   # Relevance threshold
}
```

## 📊 Ví dụ Output

### Search Output

```
🔍 Đang tìm kiếm: 'software development estimation'

📚 Tìm thấy 3 kết quả:

1. Project_Requirements.md - MyProject
   Relevance: 0.892
   Content: The software development estimation process involves analyzing requirements, breaking down tasks, and estimating time for each component. This includes understanding the scope, identifying dependencies, and considering team capabilities...

2. Technical_Specifications.md - MyProject
   Relevance: 0.845
   Content: Database design considerations include normalization, indexing strategies, and performance optimization. The system architecture should support scalability and maintainability...

3. API_Documentation.md - MyProject
   Relevance: 0.723
   Content: RESTful API endpoints for user management, authentication, and data retrieval. Each endpoint includes proper error handling and validation...
```

### List-Docs Output

```
📚 Knowledge Base: Project Documents Knowledge Base
   ID: project_documents
   Description: Knowledge base for software project estimation

✅ Knowledge base có dữ liệu và sẵn sàng query

📊 Storage Information:
   - Chunk Storage: ./dsrag_storage/chunk_storage/project_documents.pkl
   - Metadata: ./dsrag_storage/metadata/project_documents.json
   - Vector Storage: ./dsrag_storage/vector_storage/project_documents.pkl
```

## 🏗️ Storage Structure

```
dsrag_storage/
├── chunk_storage/
│   └── project_documents.pkl          # Document chunks
├── metadata/
│   └── project_documents.json         # Knowledge base metadata
└── vector_storage/
    └── project_documents.pkl          # Vector embeddings
```

## 🔄 Workflow Tích hợp

### Workflow 1: Index → Search → List

```bash
# Bước 1: Index documents
python3 index_cli.py index --folder markdown_files --project-name "MyProject"

# Bước 2: Tìm kiếm
python3 index_cli.py search --query "software development estimation"

# Bước 3: Liệt kê documents
python3 index_cli.py index --folder markdown_files --list-docs
```

### Workflow 2: Tích hợp với EST CLI

```bash
# Bước 1: Index documents
python3 index_cli.py index --folder markdown_files --project-name "MyProject"

# Bước 2: Sử dụng EST CLI với semantic search
python3 est_cli.py --folder markdown_files --project-name "MyProject" --use-semantic-search
```

## 🧪 Testing

### Test Search Functionality

```bash
# Test với query đơn giản
python3 index_cli.py search --query "test"

# Test với query phức tạp
python3 index_cli.py search --query "software development estimation and project management"

# Test với số kết quả khác nhau
python3 index_cli.py search --query "database" --max-results 3
```

### Test List Functionality

```bash
# Test liệt kê documents
python3 index_cli.py index --folder markdown_files --list-docs

# Test với project name
python3 index_cli.py index --folder markdown_files --project-name "TestProject" --list-docs
```

### Test Knowledge Base

```bash
# Test knowledge base với query cụ thể
python3 index_cli.py index --folder markdown_files --test-query "software development"

# Test với storage tùy chỉnh
python3 index_cli.py index --folder markdown_files --storage-dir "./test_storage" --test-query "test"
```

## 🔧 Troubleshooting

### Lỗi thường gặp

#### 1. OpenAI API Key không hợp lệ
```bash
❌ Lỗi: Cần cung cấp OpenAI API Key
```
**Giải pháp:**
```bash
export OPENAI_API_KEY="your-valid-api-key"
```

#### 2. Storage directory không tồn tại
```bash
❌ Lỗi: Storage directory không tồn tại
```
**Giải pháp:**
```bash
make index-setup
```

#### 3. Không tìm thấy documents
```bash
❌ Không tìm thấy kết quả nào
```
**Giải pháp:**
```bash
# Kiểm tra documents đã index
python3 index_cli.py index --folder markdown_files --list-docs

# Reindex documents
python3 index_cli.py index --folder markdown_files --force-reindex
```

#### 4. Query trả về rỗng
```bash
⚠️ Không thể query knowledge base
```
**Giải pháp:**
```bash
# Kiểm tra storage
ls -la dsrag_storage/

# Test với query đơn giản
python3 index_cli.py search --query "test"
```

## 📈 Performance Tips

### 1. Optimize Search Parameters

```python
# Cho tìm kiếm nhanh
rse_params = {
    "max_length": 3,
    "minimum_value": 0.8,
    "irrelevant_chunk_penalty": 0.5
}

# Cho tìm kiếm chi tiết
rse_params = {
    "max_length": 10,
    "minimum_value": 0.6,
    "irrelevant_chunk_penalty": 0.2
}
```

### 2. Storage Optimization

```bash
# Sử dụng storage riêng cho từng project
python3 index_cli.py index --folder markdown_files --storage-dir "./project_specific_storage"

# Cleanup storage định kỳ
rm -rf dsrag_storage/chunk_storage/*.pkl
```

### 3. Query Optimization

```bash
# Sử dụng query cụ thể
python3 index_cli.py search --query "database design patterns"

# Thay vì query chung chung
python3 index_cli.py search --query "database"
```

## 🔗 Tích hợp với các tools khác

### 1. Tích hợp với EST CLI

```bash
# Index documents
python3 index_cli.py index --folder markdown_files --project-name "MyProject"

# Sử dụng trong EST CLI
python3 est_cli.py --folder markdown_files --use-semantic-search
```

### 2. Tích hợp với Document Converter

```bash
# Convert documents
python3 convert_docs.py /path/to/documents --output ./markdown_files

# Index converted documents
python3 index_cli.py index --folder markdown_files --project-name "MyProject"
```

### 3. Tích hợp với Makefile

```bash
# Workflow hoàn chỉnh
make convert INPUT=/path/to/documents OUTPUT=./markdown_files
make index-docs FOLDER=markdown_files PROJECT=MyProject
make index-search QUERY="software development estimation"
make est-analyze FOLDER=markdown_files PROJECT=MyProject
```

## 📝 Best Practices

### 1. Naming Conventions

```bash
# Sử dụng tên project có ý nghĩa
python3 index_cli.py index --folder markdown_files --project-name "ECommerce_Platform"

# Sử dụng storage directory có cấu trúc
python3 index_cli.py index --folder markdown_files --storage-dir "./knowledge_bases/ecommerce"
```

### 2. Query Strategies

```bash
# Query cụ thể thay vì chung chung
python3 index_cli.py search --query "user authentication JWT tokens"

# Sử dụng từ khóa kỹ thuật
python3 index_cli.py search --query "microservices architecture patterns"
```

### 3. Storage Management

```bash
# Backup storage định kỳ
cp -r dsrag_storage dsrag_storage_backup_$(date +%Y%m%d)

# Cleanup storage cũ
find dsrag_storage -name "*.pkl" -mtime +30 -delete
```

## 🎯 Use Cases

### 1. Software Project Estimation

```bash
# Index project requirements
python3 index_cli.py index --folder project_docs --project-name "SoftwareProject"

# Search for estimation patterns
python3 index_cli.py search --query "development time estimation patterns"

# List indexed documents
python3 index_cli.py index --folder project_docs --list-docs
```

### 2. Technical Documentation Search

```bash
# Index technical docs
python3 index_cli.py index --folder tech_docs --project-name "TechnicalDocs"

# Search for specific topics
python3 index_cli.py search --query "API authentication methods"

# Find related documents
python3 index_cli.py search --query "database optimization techniques"
```

### 3. Knowledge Base Management

```bash
# Index multiple projects
python3 index_cli.py index --folder project_a --project-name "ProjectA"
python3 index_cli.py index --folder project_b --project-name "ProjectB"

# Search across all knowledge
python3 index_cli.py search --query "common development patterns"

# List all indexed content
python3 index_cli.py index --folder project_a --list-docs
```

## 📚 References

- [dsRAG Documentation](https://github.com/dsrag/dsrag)
- [OpenAI Embeddings](https://platform.openai.com/docs/guides/embeddings)
- [Qdrant Vector Database](https://qdrant.tech/)
- [Cohere Reranking](https://cohere.ai/rerank) 