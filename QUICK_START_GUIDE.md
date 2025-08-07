# 🚀 Quick Start Guide - Document Converter & EST CLI

## 📋 Tổng quan

Bộ công cụ này bao gồm 3 thành phần chính:

1. **Document Converter CLI** - Chuyển đổi PDF/XLSX thành Markdown
2. **EST CLI** - Phân tích và ước tính dự án từ Markdown
3. **Index CLI** - Tạo Knowledge Base với dsRAG

---

## ⚡ Cài đặt nhanh

```bash
# 1. Clone repository (nếu chưa có)
git clone <repository-url>
cd est-khobai

# 2. Cài đặt dependencies
make install

# 3. Thiết lập OpenAI API Key (cho EST và Index CLI)
export OPENAI_API_KEY='your-openai-api-key'
```

---

## 🔄 Document Converter CLI

### Chuyển đổi nhanh

```bash
# Chuyển đổi tất cả file trong thư mục
make convert INPUT=/path/to/your/documents

# Chuyển đổi với output tùy chỉnh
make convert INPUT=/path/to/your/documents OUTPUT=./my_output

# Chuyển đổi tất cả file (kể cả đã có)
make convert-force INPUT=/path/to/your/documents
```

### Sử dụng trực tiếp

```bash
# Chuyển đổi cơ bản
python3 convert_docs.py ./source_files --output ./markdown_files

# Với options
python3 convert_docs.py /path/to/documents --output ./output --verbose

# Chỉ xem danh sách file sẽ chuyển đổi
python3 convert_docs.py /path/to/documents --dry-run
```

### Định dạng hỗ trợ
- ✅ PDF
- ✅ XLSX
- ✅ XLSM  
- ✅ XLS (tự động chuyển thành XLSX)

---

## 🤖 EST CLI - Estimation Tool

### Phân tích dự án

```bash
# Phân tích với folder markdown
make est-analyze FOLDER=markdown_files

# Với tên dự án tùy chỉnh
make est-analyze FOLDER=markdown_files PROJECT="My Project"

# Sử dụng trực tiếp
python3 est_cli.py --folder markdown_files --project-name "My Project"
```

### Kết quả
- 📊 File Excel với phân tích chi tiết
- 📈 Biểu đồ và thống kê
- 💰 Ước tính chi phí và thời gian

---

## 📚 Index CLI - dsRAG Knowledge Base

### Thiết lập ban đầu

```bash
# Setup Qdrant storage
make index-setup

# Hoặc tạo thủ công
mkdir -p dsrag_storage/{chunk_storage,metadata,vector_storage}
```

### Index documents

```bash
# Index documents vào Knowledge Base
make index-docs FOLDER=markdown_files PROJECT=TestProject

# Sử dụng trực tiếp
python3 index_cli.py index --folder markdown_files --project-name TestProject
```

### Tìm kiếm

```bash
# Tìm kiếm trong Knowledge Base
make index-search QUERY="software development estimation"

# Với số kết quả tùy chỉnh
make index-search QUERY="test query" MAX_RESULTS=5
```

### Quản lý

```bash
# Liệt kê documents đã index
make index-list FOLDER=markdown_files

# Test knowledge base
make index-test FOLDER=markdown_files TEST_QUERY="test query"
```

---

## 🎯 Workflow điển hình

### 1. Chuyển đổi documents
```bash
# Chuyển đổi PDF/XLSX thành Markdown
make convert INPUT=./source_files OUTPUT=./markdown_files
```

### 2. Phân tích dự án
```bash
# Phân tích và ước tính
make est-analyze FOLDER=markdown_files PROJECT="Software Project"
```

### 3. Tạo Knowledge Base
```bash
# Index vào dsRAG
make index-docs FOLDER=markdown_files PROJECT="Software Project"

# Tìm kiếm thông tin
make index-search QUERY="development timeline"
```

---

## 🔧 Troubleshooting

### Lỗi thường gặp

**1. "Docling chưa được cài đặt"**
```bash
pip install -r requirements.txt
```

**2. "OpenAI API Key không hợp lệ"**
```bash
export OPENAI_API_KEY='your-actual-api-key'
```

**3. "Qdrant storage không tồn tại"**
```bash
make index-setup
```

### Kiểm tra dependencies

```bash
# Kiểm tra tất cả dependencies
python3 -c "import docling, pandas, openpyxl, openai, qdrant_client, sentence_transformers"
echo "✅ Tất cả dependencies đã sẵn sàng"
```

---

## 📖 Help commands

```bash
# Help tổng quan
make help

# Help cho từng tool
make est-help
make index-help
```

---

## 🎨 Tips & Tricks

### 1. Sử dụng dry-run trước khi chuyển đổi
```bash
python3 convert_docs.py /path/to/documents --dry-run
```

### 2. Chuyển đổi từng bước
```bash
# Bước 1: Chuyển đổi
make convert INPUT=./docs

# Bước 2: Kiểm tra kết quả
ls -la markdown_output/

# Bước 3: Phân tích
make est-analyze FOLDER=markdown_output
```

### 3. Tạo Knowledge Base cho nhiều dự án
```bash
# Dự án A
make index-docs FOLDER=project_a_docs PROJECT="Project A"

# Dự án B  
make index-docs FOLDER=project_b_docs PROJECT="Project B"

# Tìm kiếm chung
make index-search QUERY="common pattern"
```

---

## 📞 Hỗ trợ

- 📁 **Source files**: Thư mục chứa PDF/XLSX gốc
- 📄 **Markdown files**: Kết quả chuyển đổi từ source
- 📊 **Analysis**: File Excel với phân tích dự án
- 🧠 **Knowledge Base**: dsRAG storage cho tìm kiếm

---

*🎯 Mục tiêu: Tự động hóa quy trình phân tích tài liệu và ước tính dự án với AI*
