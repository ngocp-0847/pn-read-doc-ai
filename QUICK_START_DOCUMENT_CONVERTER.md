# Quick Start Guide - Document Converter & EST CLI

## 🚀 Bắt đầu nhanh với Document Converter và EST CLI

### Bước 1: Cài đặt và Setup

```bash
# Clone repository (nếu chưa có)
git clone <repository-url>
cd est-khobai

# Cài đặt dependencies
pip install -r requirements.txt

# Thiết lập OpenAI API Key
export OPENAI_API_KEY="your-openai-api-key-here"
```

### Bước 2: Chuyển đổi Documents

#### Chuyển đổi folder chứa documents
```bash
# Chuyển đổi folder với output mặc định
python3 convert_docs.py /path/to/your/documents

# Chuyển đổi với output tùy chỉnh
python3 convert_docs.py /path/to/your/documents --output ./markdown_files

# Force convert (chuyển đổi lại tất cả)
python3 convert_docs.py /path/to/your/documents --force-convert
```

#### Sử dụng Makefile
```bash
# Chuyển đổi với Makefile
make convert INPUT=/path/to/your/documents
make convert INPUT=/path/to/your/documents OUTPUT=./markdown_files

# Force convert với Makefile
make convert-force INPUT=/path/to/your/documents
```

### Bước 3: Phân tích với EST CLI

#### Phân tích cơ bản
```bash
# Phân tích folder markdown đã chuyển đổi
python3 est_cli.py --folder markdown_files --project-name "My Project"

# Chỉ định file output
python3 est_cli.py --folder markdown_files --output "my_analysis.xlsx"
```

#### Sử dụng Makefile
```bash
# Phân tích với Makefile
make est-analyze FOLDER=markdown_files PROJECT="My Project"

# Demo phân tích
make est-demo
```

### 📋 Ví dụ Workflow hoàn chỉnh

```bash
# 1. Chuyển đổi documents từ folder source_files
python3 convert_docs.py source_files --output markdown_files

# 2. Phân tích với EST CLI
python3 est_cli.py --folder markdown_files --project-name "Transport Management System"

# 3. Kết quả sẽ được lưu trong file Excel với 4 sheets:
# - Summary: Tổng quan dự án
# - Parent Tasks: Các task chính
# - Children Tasks: Chi tiết từng task con
# - Assumptions & Risks: Giả định và rủi ro
```

### 🎯 Các lệnh Makefile hữu ích

```bash
# Setup và test
make install          # Cài đặt dependencies
make test            # Test script với dry-run
make demo            # Chạy demo chuyển đổi

# Document Converter
make convert INPUT=/path/to/folder
make convert-force INPUT=/path/to/folder

# EST CLI
make est-help        # Hiển thị help
make est-test        # Test EST CLI
make est-demo        # Chạy demo phân tích
make est-analyze FOLDER=markdown_files PROJECT="My Project"

# Dọn dẹp
make clean           # Xóa các file output
```

### 📊 Kết quả mong đợi

#### File Excel Output sẽ có:
1. **Summary Sheet**: Tổng quan dự án
   - Tên dự án
   - Tổng thời gian ước tính
   - Số lượng tasks
   - Phân bố theo độ phức tạp

2. **Parent Tasks Sheet**: Các task chính
   - Tên task
   - Thời gian ước tính
   - Độ phức tạp (Low/Medium/High)
   - Mô tả

3. **Children Tasks Sheet**: Chi tiết từng task con
   - Task cha
   - Tên task con
   - Thời gian ước tính
   - Độ phức tạp
   - Mô tả chi tiết

4. **Assumptions & Risks Sheet**: Giả định và rủi ro
   - Các giả định về dự án
   - Rủi ro tiềm ẩn
   - Khuyến nghị

### ⚠️ Lưu ý quan trọng

1. **OpenAI API Key**: Bắt buộc phải có để EST CLI hoạt động
2. **File formats**: Hỗ trợ PDF, Word, Excel, PowerPoint
3. **Task limits**: Mỗi task không quá 14 giờ
4. **Output**: File Excel sẽ được tạo trong thư mục hiện tại

### 🔧 Troubleshooting

#### Lỗi thường gặp:
```bash
# Lỗi OpenAI API Key
❌ Vui lòng thiết lập OPENAI_API_KEY: export OPENAI_API_KEY='your-api-key'

# Lỗi folder không tồn tại
❌ Folder không tồn tại: /path/to/folder

# Lỗi không có file markdown
❌ Không tìm thấy file markdown trong folder
```

#### Giải pháp:
```bash
# Kiểm tra OpenAI API Key
echo $OPENAI_API_KEY

# Kiểm tra folder tồn tại
ls -la /path/to/folder

# Test với dry-run
python3 convert_docs.py /path/to/folder --dry-run
```

### 📞 Hỗ trợ

Nếu gặp vấn đề:
1. Chạy `make test` để kiểm tra setup
2. Kiểm tra OpenAI API Key
3. Xem log chi tiết với `--verbose`
4. Tạo issue với thông tin lỗi chi tiết
