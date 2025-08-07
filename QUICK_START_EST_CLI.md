# Quick Start Guide - EST CLI (Estimation Tool)

## 🚀 Bắt đầu nhanh với EST CLI - AI-Powered Project Estimation

### 📋 Tổng quan

EST CLI là công cụ ước tính thời gian phát triển phần mềm sử dụng AI (OpenAI) và Atomic Agents để phân tích tài liệu markdown và đưa ra ước tính chi tiết cho các dự án phần mềm.

### ✨ Tính năng chính

- 🤖 **AI-Powered Analysis**: Sử dụng OpenAI GPT để phân tích tài liệu
- 📊 **Structured Output**: Xuất kết quả ra file Excel với nhiều sheet
- 🔍 **Semantic Search**: Tích hợp dsRAG để cải thiện độ chính xác
- 📋 **Task Breakdown**: Tự động chia nhỏ dự án thành các task con
- ⏱️ **Time Estimation**: Ước tính thời gian chi tiết cho từng task
- 🎯 **Complexity Assessment**: Đánh giá độ phức tạp của từng task

---

## 🛠️ Cài đặt và Setup

### Bước 1: Cài đặt Dependencies

```bash
# Clone repository (nếu chưa có)
git clone <repository-url>
cd est-khobai

# Cài đặt dependencies
pip install -r requirements.txt

# Hoặc sử dụng Makefile
make install
```

### Bước 2: Thiết lập OpenAI API Key

```bash
# Thiết lập API key (bắt buộc)
export OPENAI_API_KEY="your-openai-api-key-here"

# Hoặc tạo file .env
echo "OPENAI_API_KEY=your-openai-api-key-here" > .env
```

### Bước 3: Setup Environment

```bash
# Setup environment cho EST CLI
make est-setup

# Hoặc tạo thư mục thủ công
mkdir -p markdown_files
mkdir -p output
```

---

## 🎯 Sử dụng cơ bản

### Phân tích dự án đơn giản

```bash
# Phân tích với folder markdown_files
python est_cli.py --folder markdown_files

# Phân tích với tên dự án tùy chỉnh
python est_cli.py --folder markdown_files --project-name "My Project"

# Phân tích với output file tùy chỉnh
python est_cli.py --folder markdown_files --output "my_analysis.xlsx"
```

### Sử dụng Makefile

```bash
# Demo với markdown_files
make est-demo

# Test với demo data
make est-test

# Phân tích dự án tùy chỉnh
make est-analyze FOLDER=markdown_files PROJECT="MyProject"
```

---

## 📊 Cấu trúc Output

EST CLI tạo ra file Excel với 4 sheet chính:

### 1. Summary Sheet
- Tên dự án
- Tổng thời gian ước tính
- Số lượng parent tasks
- Số lượng children tasks
- Thời gian tạo báo cáo

### 2. Parent Tasks Sheet
- ID parent task
- Tên parent task
- Mô tả
- Tổng thời gian ước tính
- Số lượng children tasks

### 3. Children Tasks Sheet
- ID parent task
- Tên parent task
- ID children task
- Tên children task
- Mô tả chi tiết
- Độ phức tạp
- Thời gian ước tính
- Dependencies
- Độ ưu tiên
- Kỹ năng cần thiết

### 4. Assumptions & Risks Sheet
- Danh sách các giả định
- Danh sách các rủi ro

---

## 🔧 Các tùy chọn nâng cao

### Semantic Search với dsRAG

```bash
# Bật semantic search (mặc định)
python est_cli.py --folder markdown_files --use-semantic-search

# Tắt semantic search
python est_cli.py --folder markdown_files --use-semantic-search false
```

### Greedy Mode cho ước tính chi tiết

```bash
# Bật greedy mode (mặc định)
python est_cli.py --folder markdown_files --greedy-mode

# Tắt greedy mode
python est_cli.py --folder markdown_files --greedy-mode false
```

### Kết hợp các tùy chọn

```bash
# Phân tích với tất cả tính năng
python est_cli.py \
  --folder markdown_files \
  --project-name "E-commerce Platform" \
  --output "ecommerce_analysis.xlsx" \
  --use-semantic-search \
  --greedy-mode
```

---

## 📁 Cấu trúc tài liệu đầu vào

### Định dạng Markdown được hỗ trợ

EST CLI hỗ trợ các file markdown với các extension:
- `.md`
- `.markdown`
- `.txt`

### Ví dụ tài liệu đầu vào

```markdown
# E-commerce Platform Requirements

## User Management System
- User registration with email verification
- Login/logout functionality
- Password reset via email
- User profile management

## Product Management
- Product catalog with categories
- Product search and filtering
- Product details with images
- Inventory management

## Order Processing
- Shopping cart functionality
- Checkout process
- Payment integration
- Order tracking

## Admin Panel
- Dashboard with analytics
- User management interface
- Product management interface
- Order management interface
```

---

## 🎯 Ví dụ Workflow hoàn chỉnh

### Workflow 1: Phân tích dự án mới

```bash
# 1. Setup environment
export OPENAI_API_KEY="your-api-key"
make est-setup

# 2. Tạo tài liệu requirements
mkdir -p my_project
# Tạo các file markdown trong my_project/

# 3. Phân tích dự án
python est_cli.py --folder my_project --project-name "My New Project"

# 4. Kiểm tra kết quả
open project_analysis.xlsx
```

### Workflow 2: Demo với dữ liệu có sẵn

```bash
# 1. Setup và test
make est-setup
make est-test

# 2. Demo với markdown_files
make est-demo

# 3. Phân tích dự án thực tế
make est-analyze FOLDER=markdown_files PROJECT="Real Project"
```

### Workflow 3: Phân tích với semantic search

```bash
# 1. Setup dsRAG (nếu chưa có)
make index-setup

# 2. Index documents vào knowledge base
make index-docs FOLDER=markdown_files PROJECT="Knowledge Base"

# 3. Phân tích với semantic search
python est_cli.py \
  --folder markdown_files \
  --project-name "Enhanced Analysis" \
  --use-semantic-search \
  --greedy-mode
```

---

## 🚨 Troubleshooting

### Lỗi thường gặp

#### 1. OpenAI API Key không hợp lệ
```bash
❌ Error: Invalid API key
✅ Giải pháp: Kiểm tra lại OPENAI_API_KEY
export OPENAI_API_KEY="your-valid-api-key"
```

#### 2. Folder không tồn tại
```bash
❌ Error: Folder not found
✅ Giải pháp: Tạo folder hoặc kiểm tra đường dẫn
mkdir -p markdown_files
```

#### 3. Không tìm thấy file markdown
```bash
❌ Error: No markdown files found
✅ Giải pháp: Tạo file markdown hoặc kiểm tra extension
# Tạo file demo
echo "# Demo Project" > markdown_files/demo.md
```

#### 4. Dependencies chưa được cài đặt
```bash
❌ Error: Module not found
✅ Giải pháp: Cài đặt dependencies
pip install -r requirements.txt
```

### Debug Mode

```bash
# Chạy với verbose output
python est_cli.py --folder markdown_files --verbose

# Kiểm tra dependencies
python -c "import pandas, openpyxl, openai, atomic_agents; print('All dependencies OK')"
```

---

## 📋 Các lệnh Makefile hữu ích

```bash
# Setup và cài đặt
make install          # Cài đặt dependencies
make est-setup        # Setup environment cho EST CLI

# Test và demo
make est-test         # Test với demo data
make est-demo         # Demo với markdown_files

# Phân tích dự án
make est-analyze FOLDER=markdown_files PROJECT="MyProject"

# Quản lý
make est-help         # Hiển thị help
make est-clean        # Xóa output files

# Index CLI (cho semantic search)
make index-setup      # Setup dsRAG
make index-docs FOLDER=markdown_files PROJECT="KB"
```

---

## 🔧 Cấu hình nâng cao

### Tùy chỉnh cấu hình

EST CLI sử dụng cấu hình từ `config/estimate.py`:

```python
# Các mức độ phức tạp
COMPLEXITY_LEVELS = ['Low', 'Medium', 'High', 'Very High']

# Các mức độ ưu tiên
PRIORITY_LEVELS = ['Low', 'Medium', 'High', 'Critical']

# Khoảng thời gian task
MIN_TASK_HOURS = 0.5
MAX_TASK_HOURS = 80.0
```

### Environment Variables

```bash
# OpenAI API Key
export OPENAI_API_KEY="your-api-key"

# Model configuration
export OPENAI_MODEL="gpt-4-turbo-preview"

# Output configuration
export DEFAULT_OUTPUT="project_analysis.xlsx"
export DEFAULT_PROJECT_NAME="Software Project"
```

---

## 📚 Tài liệu tham khảo

- [EST CLI Source Code](est_cli.py)
- [Configuration Files](config/)
- [Index CLI Guide](QUICK_START_INDEX_CLI.md)
- [Document Converter Guide](QUICK_START_DOCUMENT_CONVERTER.md)

---

## 🤝 Hỗ trợ

Nếu gặp vấn đề, hãy kiểm tra:

1. ✅ OpenAI API Key đã được thiết lập
2. ✅ Dependencies đã được cài đặt
3. ✅ Folder chứa file markdown tồn tại
4. ✅ File markdown có định dạng đúng

### Liên hệ hỗ trợ

- 📧 Email: support@example.com
- 📖 Documentation: [Wiki](https://github.com/example/est-khobai/wiki)
- 🐛 Issues: [GitHub Issues](https://github.com/example/est-khobai/issues)
