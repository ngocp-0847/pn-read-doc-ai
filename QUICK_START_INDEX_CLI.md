# Quick Start Guide - Index CLI (dsRAG)

## 🚀 Bắt đầu nhanh với Index CLI - dsRAG Knowledge Base

### Bước 1: Cài đặt và Setup

```bash
# Clone repository (nếu chưa có)
git clone <repository-url>
cd est-khobai

# Cài đặt dependencies
pip install -r requirements.txt

# Thiết lập OpenAI API Key (bắt buộc)
export OPENAI_API_KEY="your-openai-api-key-here"

# Setup Qdrant storage cho dsRAG
make index-setup
```

### Bước 2: Index Documents vào Knowledge Base

#### Index cơ bản
```bash
# Index documents từ folder markdown
python3 index_cli.py index --folder markdown_files --project-name "MyProject"

# Index với storage directory tùy chỉnh
python3 index_cli.py index --folder markdown_files --storage-dir "./custom_storage"
```

#### Sử dụng Makefile
```bash
# Index với Makefile
make index-docs FOLDER=markdown_files PROJECT="MyProject"

# Index với storage tùy chỉnh
make index-docs FOLDER=markdown_files PROJECT="MyProject" STORAGE_DIR="./custom_storage"
```

### Bước 3: Tìm kiếm trong Knowledge Base

#### Tìm kiếm cơ bản
```bash
# Tìm kiếm với query đơn giản
python3 index_cli.py search --query "software development estimation"

# Tìm kiếm với số kết quả tùy chỉnh
python3 index_cli.py search --query "database design" --max-results 10
```

#### Sử dụng Makefile
```bash
# Tìm kiếm với Makefile
make index-search QUERY="software development estimation"

# Tìm kiếm với số kết quả tùy chỉnh
make index-search QUERY="API development" MAX_RESULTS=5
```

### Bước 4: Quản lý Knowledge Base

#### Liệt kê documents đã index
```bash
# Liệt kê tất cả documents
python3 index_cli.py index --folder markdown_files --list-docs

# Liệt kê với project name cụ thể
python3 index_cli.py index --folder markdown_files --project-name "MyProject" --list-docs
```

#### Sử dụng Makefile
```bash
# Liệt kê với Makefile
make index-list FOLDER=markdown_files
make index-list FOLDER=markdown_files PROJECT="MyProject"
```

### 📋 Ví dụ Workflow hoàn chỉnh

```bash
# 1. Setup environment
export OPENAI_API_KEY="your-openai-api-key"
make index-setup

# 2. Index documents
python3 index_cli.py index --folder markdown_files --project-name "Transport System"

# 3. Tìm kiếm trong knowledge base
python3 index_cli.py search --query "user authentication system" --max-results 5

# 4. Liệt kê documents đã index
python3 index_cli.py index --folder markdown_files --list-docs

# 5. Test knowledge base
python3 index_cli.py index --folder markdown_files --test-query "database design"
```

### 🎯 Các lệnh Makefile hữu ích

```bash
# Setup và help
make index-setup     # Setup Qdrant storage
make index-help      # Hiển thị help cho Index CLI

# Index documents
make index-docs FOLDER=markdown_files PROJECT="MyProject"

# Tìm kiếm
make index-search QUERY="your search query"
make index-search QUERY="software development" MAX_RESULTS=10

# Quản lý
make index-list FOLDER=markdown_files
make index-test FOLDER=markdown_files TEST_QUERY="test query"
```

### 📊 Kết quả mong đợi

#### Kết quả Index
```
📚 Đang index documents vào dsRAG Knowledge Base...
✅ Đã index thành công 15 documents cho project: MyProject
📁 Storage location: ./dsrag_storage
🔍 Knowledge base sẵn sàng cho tìm kiếm
```

#### Kết quả Search
```
🔍 Đang tìm kiếm: 'software development estimation'

📚 Tìm thấy 3 kết quả:

1. Project_Requirements.md - MyProject
   Relevance: 0.892
   Content: The software development estimation process involves analyzing requirements...

2. Technical_Specifications.md - MyProject
   Relevance: 0.845
   Content: Database design considerations include normalization...

3. API_Documentation.md - MyProject
   Relevance: 0.723
   Content: RESTful API endpoints for user management...
```

#### Kết quả List-Docs
```
📚 Knowledge Base Info:
   Name: MyProject
   ID: myproject_documents
   Description: Knowledge base for MyProject documents

📊 Document Count: 15 documents indexed
📁 Storage Location: ./dsrag_storage
🔍 Query Status: Ready for semantic search
```

### 🏗️ Storage Structure

Index CLI tạo cấu trúc storage như sau:

```
dsrag_storage/
├── chunk_storage/
│   └── project_documents.pkl
├── metadata/
│   └── project_documents.json
└── vector_storage/
    └── project_documents.pkl
```

### ⚙️ Cấu hình Search Parameters

Index CLI sử dụng các tham số tìm kiếm tối ưu:

```python
# RSE Parameters (Retrieval Search Engine)
rse_params = {
    "max_length": 5,                    # Số kết quả tối đa
    "overall_max_length": 10,           # Tổng độ dài tối đa
    "minimum_value": 0.7,               # Ngưỡng relevance tối thiểu
    "irrelevant_chunk_penalty": 0.3     # Penalty cho chunks không liên quan
}
```

### 🔗 Tích hợp với EST CLI

Index CLI được thiết kế để tích hợp với EST CLI:

```bash
# Bước 1: Index documents
python index_cli.py index --folder markdown_files --project-name "MyProject"

# Bước 2: Sử dụng EST CLI với semantic search
python est_cli.py --folder markdown_files --project-name "MyProject" --use-semantic-search
```

### ⚠️ Lưu ý quan trọng

1. **OpenAI API Key**: Bắt buộc phải có để Index CLI hoạt động
2. **Qdrant Storage**: Cần setup trước khi index
3. **File formats**: Chỉ hỗ trợ markdown files
4. **Project naming**: Sử dụng tên project nhất quán
5. **Storage cleanup**: Có thể xóa storage để reset

### 🔧 Troubleshooting

#### Lỗi thường gặp:
```bash
# Lỗi OpenAI API Key
❌ Vui lòng thiết lập OPENAI_API_KEY: export OPENAI_API_KEY='your-api-key'

# Lỗi Qdrant storage
❌ Storage directory không tồn tại: ./dsrag_storage

# Lỗi không có file markdown
❌ Không tìm thấy file markdown trong folder

# Lỗi project không tồn tại
❌ Knowledge base không tồn tại cho project: MyProject
```

#### Giải pháp:
```bash
# Kiểm tra OpenAI API Key
echo $OPENAI_API_KEY

# Setup lại storage
make index-setup

# Kiểm tra folder markdown
ls -la markdown_files/

# Tạo lại knowledge base
rm -rf dsrag_storage/
make index-setup
make index-docs FOLDER=markdown_files PROJECT="MyProject"
```

### 📞 Hỗ trợ

Nếu gặp vấn đề:
1. Chạy `make index-setup` để setup storage
2. Kiểm tra OpenAI API Key
3. Kiểm tra folder markdown có tồn tại
4. Xem log chi tiết với `--verbose`
5. Tạo issue với thông tin lỗi chi tiết

### 🚀 Advanced Usage

#### Tìm kiếm nâng cao
```bash
# Tìm kiếm với storage directory tùy chỉnh
python3 index_cli.py search --query "user authentication" --storage-dir "./custom_storage"

# Tìm kiếm với độ chính xác cao
python3 index_cli.py search --query "microservices architecture" --max-results 3
```

#### Test knowledge base
```bash
# Test với query cụ thể
python3 index_cli.py index --folder markdown_files --test-query "database design"

# Test với Makefile
make index-test FOLDER=markdown_files TEST_QUERY="API development"
```
