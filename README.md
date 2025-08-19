# Document Converter CLI

Công cụ chuyển đổi tài liệu sử dụng Docling để chuyển đổi các file PDF, Excel (XLSX, XLSM, XLS) thành định dạng Markdown.

## 🚀 Tính năng chính

### Document Converter CLI
- Chuyển đổi các file PDF, Excel (XLSX, XLSM, XLS) sang markdown
- Hỗ trợ nhiều định dạng đầu vào
- Tự động xử lý batch files
- Tạo output có cấu trúc
- Xử lý đặc biệt cho file .xls (chuyển đổi sang .xlsx trước)
- Hỗ trợ OCR và trích xuất bảng
- Retry logic cho các file lỗi
- Bỏ qua các file đã được chuyển đổi (trừ khi dùng force mode)

## 📦 Cài đặt

```bash
# Clone repository
git clone <repository-url>
cd pn-read-doc-ai

# Cài đặt dependencies
pip install -r requirements.txt
```

## 🛠️ Sử dụng

### Document Converter CLI

```bash
# Chuyển đổi folder
python convert_docs.py /path/to/folder --output ./markdown_files

# Chuyển đổi với force mode (chuyển đổi lại tất cả file)
python convert_docs.py /path/to/folder --force-convert

# Dry run để xem trước danh sách file sẽ chuyển đổi
python convert_docs.py /path/to/folder --dry-run

# Chuyển đổi với thông tin chi tiết
python convert_docs.py /path/to/folder --verbose

# Chuyển đổi thư mục hiện tại
python convert_docs.py .
```

### Các tùy chọn command line

- `input_folder`: Thư mục chứa các file cần chuyển đổi (bắt buộc)
- `--output, -o`: Thư mục output (mặc định: ./markdown_output)
- `--verbose, -v`: Hiển thị thông tin chi tiết
- `--dry-run`: Chỉ hiển thị danh sách file sẽ chuyển đổi, không thực hiện
- `--force-convert`: Chuyển đổi tất cả file, kể cả những file đã tồn tại

## 📋 Makefile Commands

### Document Converter
```bash
make help             # Hiển thị tất cả commands có sẵn
make setup            # Tạo thư mục cần thiết
make convert          # Chuyển đổi documents với INPUT và OUTPUT
make convert-force    # Chuyển đổi với force mode
make convert-current  # Chuyển đổi thư mục hiện tại
```

### Ví dụ sử dụng Makefile
```bash
# Chuyển đổi folder cụ thể
make convert INPUT=/path/to/source OUTPUT=./markdown_files

# Chuyển đổi với force mode
make convert-force INPUT=/path/to/source OUTPUT=./markdown_files

# Chuyển đổi thư mục hiện tại
make convert-current
```

## 📁 Định dạng được hỗ trợ

- **PDF**: Các file PDF với text và hình ảnh
- **Excel**: .xlsx, .xlsm, .xls (tự động chuyển đổi .xls sang .xlsx)
- **OCR**: Tự động nhận dạng văn bản từ hình ảnh
- **Tables**: Trích xuất và chuyển đổi bảng sang markdown

## ⚙️ Cấu hình

Script sử dụng file cấu hình `config/convert_md.py` (tùy chọn) hoặc cấu hình mặc định:

```python
# Các định dạng được hỗ trợ
SUPPORTED_EXTENSIONS = {'.pdf', '.xlsx', '.xlsm', '.xls'}

# Định dạng đặc biệt cần xử lý
SPECIAL_FORMATS = {'.xls'}

# Cấu hình output
OUTPUT_CONFIG = {
    'default_output_dir': './markdown_output',
    'encoding': 'utf-8'
}

# Cấu hình Docling
DOCLING_CONFIG = {
    'enable_ocr': True,
    'enable_table_extraction': True
}

# Xử lý lỗi
ERROR_HANDLING = {
    'continue_on_error': True,
    'max_retries': 3,
    'retry_delay': 1
}

# Patterns và thư mục bỏ qua
IGNORE_PATTERNS = ['~$*', '*.tmp', '*.bak']
IGNORE_DIRECTORIES = ['.git', '__pycache__']
```

## 📊 Output Examples

### Markdown Output
Các file được chuyển đổi sẽ có cấu trúc như sau:

```
markdown_output/
├── document1.md
├── spreadsheet1.md
├── presentation1.md
└── report1.md
```

### Ví dụ log output:
```
🔍 Đang tìm kiếm các file trong: /path/to/documents
📁 Tìm thấy 5 file được hỗ trợ:
  - document.pdf
  - spreadsheet.xlsx
  - old_file.xls
  - report.pdf
  - data.xlsm

🔄 Sẽ chuyển đổi 4/5 file:
  - document.pdf
  - old_file.xls
  - report.pdf
  - data.xlsm

⏭️ Bỏ qua file đã tồn tại: spreadsheet.xlsx -> spreadsheet.md

🔧 Phát hiện file đặc biệt: old_file.xls
🔄 Đang chuyển đổi .xls thành .xlsx: old_file.xls
✅ Đã chuyển đổi thành công: old_file.xlsx
✅ Đã chuyển đổi thành công: ./markdown_output/old_file.md
🗑️ Đã xóa file tạm: old_file.xlsx

==================================================
📊 TỔNG KẾT:
  - Tổng số file: 4
  - Chuyển đổi thành công: 4
  - Thất bại: 0
  - Thư mục output: /path/to/markdown_output
🎉 Tất cả file đã được chuyển đổi thành công!
```

## 🏗️ Kiến trúc

```
pn-read-doc-ai/
├── convert_docs.py      # Document Converter CLI
├── config/
│   ├── convert_md.py   # Cấu hình Document Converter
│   └── estimate.py     # Cấu hình ước tính
├── docs/               # Tài liệu hướng dẫn
├── requirements.txt    # Dependencies
├── Makefile           # Build commands
├── README.md          # Documentation
├── markdown_output/    # Thư mục output mặc định
└── source_files/       # Source documents (example)
```

## 🔧 Tùy chỉnh nâng cao

### Tạo file cấu hình tùy chỉnh
Tạo file `config/convert_md.py` để tùy chỉnh:

```python
# Định dạng được hỗ trợ
SUPPORTED_EXTENSIONS = {'.pdf', '.xlsx', '.xlsm', '.xls', '.docx'}

# Cấu hình output
OUTPUT_CONFIG = {
    'default_output_dir': './my_markdown_output',
    'encoding': 'utf-8'
}

# Cấu hình Docling
DOCLING_CONFIG = {
    'enable_ocr': True,
    'enable_table_extraction': True
}

# Patterns bỏ qua
IGNORE_PATTERNS = ['~$*', '*.tmp', '*.bak', '.DS_Store']
IGNORE_DIRECTORIES = ['.git', '__pycache__', '.vscode']
```

## 🧪 Testing

```bash
# Test Document Converter với dry run
python convert_docs.py ./test_documents --dry-run

# Test với folder mẫu
make convert-current

# Test với verbose mode
python convert_docs.py ./test_documents --verbose
```

## 📝 Dependencies

### Core Dependencies
- `docling>=2.43.0` - Document processing và OCR
- `pandas>=1.5.0` - Xử lý data cho Excel files
- `openpyxl>=3.0.0` - Đọc/ghi Excel files
- `pathlib` - Xử lý đường dẫn file
- `argparse` - CLI argument parsing
- `logging` - Logging system

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

### v1.0.0
- Document Converter CLI với Docling
- Hỗ trợ PDF, Excel (XLSX, XLSM, XLS)
- Xử lý đặc biệt cho file .xls
- OCR và trích xuất bảng
- Retry logic và error handling
- Force convert mode
- Dry run mode
- Makefile integration