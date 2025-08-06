# Document Converter CLI

Script CLI để chuyển đổi các file PDF, XLSX, XLSM thành Markdown sử dụng [Docling](https://github.com/docling-project/docling) cho hệ thống RAG LLM.

## Tính năng

- 🔍 **Tìm kiếm đệ quy**: Tự động tìm tất cả file PDF, XLSX, XLSM trong thư mục và các thư mục con
- 📄 **Hỗ trợ đa định dạng**: PDF, XLSX, XLSM
- 🎯 **Tối ưu cho RAG**: Xuất ra Markdown để dễ dàng tích hợp với hệ thống LLM
- 📊 **Báo cáo chi tiết**: Hiển thị tiến trình và kết quả chuyển đổi
- 🔧 **Tùy chọn linh hoạt**: Dry-run, verbose mode, custom output directory

## Cài đặt

1. **Cài đặt dependencies:**
```bash
pip install -r requirements.txt
```

2. **Hoặc cài đặt trực tiếp:**
```bash
pip install docling
```

## Sử dụng

### Cú pháp cơ bản
```bash
python convert_docs.py <input_folder>
```

### Ví dụ sử dụng

1. **Chuyển đổi tất cả file trong thư mục hiện tại:**
```bash
python convert_docs.py .
```

2. **Chỉ định thư mục output:**
```bash
python convert_docs.py /path/to/input --output /path/to/output
```

3. **Chế độ dry-run (chỉ xem danh sách file):**
```bash
python convert_docs.py /path/to/input --dry-run
```

4. **Hiển thị thông tin chi tiết:**
```bash
python convert_docs.py /path/to/input --verbose
```

5. **Kết hợp nhiều tùy chọn:**
```bash
python convert_docs.py /path/to/input --output ./markdown_files --verbose
```

### Tùy chọn

- `input_folder`: Thư mục chứa các file cần chuyển đổi (bắt buộc)
- `--output, -o`: Thư mục output (mặc định: `./markdown_output`)
- `--verbose, -v`: Hiển thị thông tin chi tiết
- `--dry-run`: Chỉ hiển thị danh sách file sẽ chuyển đổi, không thực hiện chuyển đổi

## Định dạng file được hỗ trợ

- **PDF** (`.pdf`)
- **Excel** (`.xlsx`, `.xlsm`, `.xls`) - File .xls sẽ được chuyển đổi thành .xlsx trước khi xử lý

## Cấu trúc output

Script sẽ tạo thư mục output với các file Markdown tương ứng:

```
markdown_output/
├── file1.md
├── file2.md
└── file3.md
```

## Lưu ý

- Script sử dụng [Docling](https://github.com/docling-project/docling) để chuyển đổi file
- Hỗ trợ Unicode và các ký tự đặc biệt
- Tự động tạo thư mục output nếu chưa tồn tại
- Hiển thị tiến trình và báo cáo kết quả chi tiết

## Troubleshooting

### Lỗi "Docling chưa được cài đặt"
```bash
pip install docling
```

### Lỗi encoding
Đảm bảo file có encoding UTF-8 hoặc tương thích.

### File không chuyển đổi được
- Kiểm tra file có bị hỏng không
- Thử chạy với `--verbose` để xem lỗi chi tiết
- Đảm bảo file có định dạng được hỗ trợ

## Ví dụ output

```
2024-01-15 10:30:15 - INFO - 🔍 Đang tìm kiếm các file trong: /path/to/input
2024-01-15 10:30:15 - INFO - 📁 Tìm thấy 3 file cần chuyển đổi:
2024-01-15 10:30:15 - INFO -   - /path/to/input/document1.pdf
2024-01-15 10:30:15 - INFO -   - /path/to/input/spreadsheet.xlsx
2024-01-15 10:30:15 - INFO -   - /path/to/input/presentation.pptx
2024-01-15 10:30:15 - INFO - 📂 Thư mục output: ./markdown_output
2024-01-15 10:30:15 - INFO - 🚀 Đã khởi tạo Docling converter
2024-01-15 10:30:16 - INFO - 🔄 Đang chuyển đổi: /path/to/input/document1.pdf
2024-01-15 10:30:18 - INFO - ✅ Đã chuyển đổi thành công: ./markdown_output/document1.md
...
==================================================
2024-01-15 10:30:25 - INFO - 📊 TỔNG KẾT:
2024-01-15 10:30:25 - INFO -   - Tổng số file: 3
2024-01-15 10:30:25 - INFO -   - Chuyển đổi thành công: 3
2024-01-15 10:30:25 - INFO -   - Thất bại: 0
2024-01-15 10:30:25 - INFO -   - Thư mục output: /absolute/path/to/markdown_output
2024-01-15 10:30:25 - INFO - 🎉 Tất cả file đã được chuyển đổi thành công!
``` 