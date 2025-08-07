# EST-Khobai - Document Processing & Estimation Tools

Dự án này bao gồm ba công cụ chính:

1. **Document Converter CLI** - Chuyển đổi tài liệu sang markdown
2. **EST CLI** - Estimation Tool cho ước tính thời gian phát triển phần mềm
3. **Index CLI** - dsRAG Indexing Tool cho tìm kiếm và quản lý knowledge base

## 🚀 Tính năng chính

### Document Converter CLI
- Chuyển đổi các file PDF, Word, Excel sang markdown
- Hỗ trợ nhiều định dạng đầu vào
- Tự động xử lý batch files
- Tạo output có cấu trúc

### EST CLI (Estimation Tool)
- Phân tích tài liệu markdown bằng AI
- Tạo cấu trúc task phân cấp (parent/children tasks)
- Ước tính thời gian thực hiện cho middle developer
- Xuất kết quả ra file Excel với nhiều sheet
- Giới hạn mỗi task không quá 14 giờ

### Index CLI (dsRAG Indexing Tool)
- Index documents vào dsRAG Knowledge Base
- Tìm kiếm semantic trong knowledge base
- Liệt kê và quản lý documents đã index
- Hỗ trợ Qdrant vector database
- Tích hợp với EST CLI để cải thiện ước tính

## 📦 Cài đặt

```bash
# Clone repository
git clone <repository-url>
cd est-khobai

# Cài đặt dependencies
pip install -r requirements.txt

# Thiết lập OpenAI API Key (cho EST CLI và Index CLI)
export OPENAI_API_KEY="your-openai-api-key-here"
```

## 🛠️ Sử dụng

### Document Converter CLI

```bash
# Chuyển đổi folder
python3 convert_docs.py /path/to/folder --output ./markdown_files

# Chuyển đổi với force mode
python3 convert_docs.py /path/to/folder --force-convert

# Dry run để xem trước
python3 convert_docs.py /path/to/folder --dry-run
```

### EST CLI

```bash
# Phân tích folder markdown
python3 est_cli.py --folder markdown_files --project-name "My Project"

# Chỉ định file output
python3 est_cli.py --folder markdown_files --output "analysis.xlsx"

# Sử dụng OpenAI key trực tiếp
python3 est_cli.py --folder markdown_files --openai-key "sk-..."
```

### Index CLI

```bash
# Index documents vào knowledge base
python3 index_cli.py index --folder markdown_files --project-name "My Project"

# Tìm kiếm trong knowledge base
python3 index_cli.py search --query "software development estimation" --max-results 5

# Liệt kê documents đã index
python3 index_cli.py index --folder markdown_files --list-docs

# Test knowledge base với query cụ thể
python3 index_cli.py index --folder markdown_files --test-query "database design"
```

## 📋 Makefile Commands

### Document Converter
```bash
make install          # Cài đặt dependencies
make test            # Test script
make demo            # Chạy demo
make convert         # Chuyển đổi documents
make clean           # Dọn dẹp files
```

### EST CLI
```bash
make est-help        # Hiển thị help cho EST CLI
make est-test        # Test EST CLI tool
make est-demo        # Chạy demo phân tích với markdown_files
make est-analyze     # Phân tích dự án với folder tùy chỉnh
```

### Index CLI
```bash
make index-help      # Hiển thị help cho Index CLI
make index-docs      # Index documents vào dsRAG Knowledge Base
make index-search    # Tìm kiếm trong Knowledge Base
make index-setup     # Setup Qdrant cho indexing
```

## 🔍 Index CLI - Search & List-Docs

### Tính năng Search

Index CLI cung cấp khả năng tìm kiếm semantic mạnh mẽ trong knowledge base:

#### Tìm kiếm cơ bản
```bash
# Tìm kiếm với query đơn giản
python3 index_cli.py search --query "software development estimation"

# Tìm kiếm với số kết quả tùy chỉnh
python3 index_cli.py search --query "database design" --max-results 10

# Tìm kiếm với OpenAI key trực tiếp
python3 index_cli.py search --query "API development" --openai-key "sk-..."
```

#### Tìm kiếm nâng cao
```bash
# Tìm kiếm với storage directory tùy chỉnh
python3 index_cli.py search --query "user authentication" --storage-dir "./custom_storage"

# Tìm kiếm với độ chính xác cao
python3 index_cli.py search --query "microservices architecture" --max-results 3
```

### Tính năng List-Docs

Liệt kê và quản lý documents đã được index:

#### Liệt kê documents
```bash
# Liệt kê tất cả documents đã index
python3 index_cli.py index --folder markdown_files --list-docs

# Liệt kê với project name cụ thể
python3 index_cli.py index --folder markdown_files --project-name "MyProject" --list-docs

# Liệt kê với storage directory tùy chỉnh
python3 index_cli.py index --folder markdown_files --storage-dir "./custom_storage" --list-docs
```

#### Thông tin hiển thị
Khi sử dụng `--list-docs`, hệ thống sẽ hiển thị:
- **Knowledge Base Info**: Tên, ID, mô tả
- **Document Count**: Số lượng documents đã index
- **Storage Location**: Đường dẫn lưu trữ
- **Query Status**: Khả năng query knowledge base

### Cấu hình Search Parameters

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

### Ví dụ kết quả Search

```
🔍 Đang tìm kiếm: 'software development estimation'

📚 Tìm thấy 3 kết quả:

1. Project_Requirements.md - MyProject
   Relevance: 0.892
   Content: The software development estimation process involves analyzing requirements, breaking down tasks, and estimating time for each component...

2. Technical_Specifications.md - MyProject
   Relevance: 0.845
   Content: Database design considerations include normalization, indexing strategies, and performance optimization...

3. API_Documentation.md - MyProject
   Relevance: 0.723
   Content: RESTful API endpoints for user management, authentication, and data retrieval...
```

### Tích hợp với EST CLI

Index CLI được thiết kế để tích hợp hoàn hảo với EST CLI:

```bash
# Bước 1: Index documents
python3 index_cli.py index --folder markdown_files --project-name "MyProject"

# Bước 2: Sử dụng EST CLI với semantic search
python3 est_cli.py --folder markdown_files --project-name "MyProject" --use-semantic-search
```

### Storage Structure

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

## 📊 Output Examples

### EST CLI Excel Output
File Excel sẽ có 4 sheet:

1. **Summary** - Tổng quan dự án
2. **Parent Tasks** - Các task chính
3. **Children Tasks** - Chi tiết từng task con
4. **Assumptions & Risks** - Giả định và rủi ro

### Ví dụ kết quả phân tích:
```
📊 KẾT QUẢ PHÂN TÍCH:
Tên dự án: Hệ thống quản lý vận tải
Tổng thời gian ước tính: 245.5 giờ
Số parent tasks: 8
Số children tasks: 32

📋 PARENT TASKS:
1. Hệ thống đăng nhập và phân quyền (12.5h)
   - Thiết kế database user (4.0h, Medium)
   - API đăng nhập/đăng xuất (3.5h, Medium)
   - Hệ thống phân quyền (5.0h, High)
```

## 🏗️ Kiến trúc

```
est-khobai/
├── convert_docs.py      # Document Converter CLI
├── est_cli.py          # EST CLI tool
├── index_cli.py        # Index CLI tool
├── context_provider.py # Context provider cho dsRAG
├── config/
│   ├── convert_md.py   # Cấu hình Document Converter
│   └── estimate.py     # Cấu hình EST CLI
├── dsrag_storage/      # Storage cho dsRAG
├── requirements.txt     # Dependencies
├── Makefile           # Build commands
├── README.md          # Documentation
├── markdown_files/     # Converted markdown files
└── source_files/       # Source documents
```

## 🔧 Cấu hình

### Biến môi trường
```bash
export OPENAI_API_KEY="your-openai-api-key"
export EST_DEFAULT_PROJECT="Software Project"
export EST_DEFAULT_OUTPUT="project_analysis.xlsx"
```

### Cấu hình EST CLI
- Model: GPT-4o-mini
- Max task hours: 14 giờ
- Min task hours: 0.5 giờ
- Complexity levels: Low, Medium, High

### Cấu hình Index CLI
- Embedding Model: text-embedding-3-small
- Reranker: CohereReranker
- LLM: GPT-4o-mini
- Storage: Qdrant vector database

## 🧪 Testing

```bash
# Test Document Converter
make test

# Test EST CLI
make est-test

# Test Index CLI
python3 index_cli.py index --folder markdown_files --test-query "test"
```

## 📝 Dependencies

### Core Dependencies
- `docling>=2.43.0` - Document processing
- `pandas>=1.5.0` - Data manipulation
- `openpyxl>=3.0.0` - Excel output
- `atomic-agents>=2.0.0` - AI agents framework
- `openai>=1.0.0` - OpenAI API
- `instructor>=1.0.0` - Structured output
- `click>=8.0.0` - CLI framework

### dsRAG Dependencies
- `dsrag>=1.0.0` - dsRAG framework
- `qdrant-client>=1.0.0` - Vector database
- `cohere>=4.0.0` - Reranking

## 🤝 Contributing

1. Fork repository
2. Tạo feature branch
3. Commit changes
4. Push to branch
5. Tạo Pull Request

## 📄 License

MIT License - Xem file LICENSE để biết thêm chi tiết.

## 🆘 Support

Nếu gặp vấn đề, vui lòng:
1. Kiểm tra documentation
2. Chạy test suite
3. Tạo issue với thông tin chi tiết

## 🔄 Changelog

### v1.1.0
- Thêm Index CLI với dsRAG integration
- Thêm tính năng search semantic
- Thêm tính năng list-docs
- Tích hợp với EST CLI để cải thiện ước tính

### v1.0.0
- Thêm Document Converter CLI
- Thêm EST CLI với AI estimation
- Hỗ trợ Excel output
- Tích hợp Makefile commands 