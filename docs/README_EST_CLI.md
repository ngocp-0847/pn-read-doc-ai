# EST CLI - Estimation Tool for Software Development Tasks

Công cụ CLI sử dụng Atomic Agents và OpenAI để phân tích tài liệu markdown và ước tính thời gian thực hiện dự án phần mềm.

## Tính năng

- 📁 Đọc và phân tích tất cả file markdown từ một folder
- 🤖 Sử dụng AI để phân tích yêu cầu và ước tính thời gian
- 📊 Tạo cấu trúc task phân cấp (parent tasks và children tasks)
- ⏱️ Ước tính thời gian cho từng task (không quá 14h/task)
- 📋 Xuất kết quả ra file Excel với nhiều sheet
- 🎯 Phân tích độ phức tạp, dependencies và kỹ năng cần thiết

## Cài đặt

1. Cài đặt dependencies:
```bash
pip install -r requirements.txt
```

2. Thiết lập OpenAI API Key:
```bash
export OPENAI_API_KEY="your-openai-api-key-here"
```

## Sử dụng

### Cú pháp cơ bản:
```bash
python est_cli.py --folder <đường-dẫn-folder> [options]
```

### Ví dụ:
```bash
# Phân tích folder markdown_files
python est_cli.py --folder markdown_files --project-name "Hệ thống quản lý vận tải"

# Chỉ định file output
python est_cli.py --folder markdown_files --output "analysis_result.xlsx"

# Sử dụng OpenAI key trực tiếp
python est_cli.py --folder markdown_files --openai-key "sk-..."
```

### Các options:

- `--folder, -f`: Đường dẫn đến folder chứa file markdown (bắt buộc)
- `--output, -o`: Tên file Excel output (mặc định: project_analysis.xlsx)
- `--project-name, -p`: Tên dự án (mặc định: Software Project)
- `--openai-key`: OpenAI API Key (có thể dùng biến môi trường OPENAI_API_KEY)

## Cấu trúc output Excel

File Excel sẽ có 4 sheet:

### 1. Summary
- Tên dự án
- Tổng thời gian ước tính
- Số lượng parent tasks và children tasks
- Ngày phân tích

### 2. Parent Tasks
- ID và tên parent task
- Mô tả tổng quan
- Tổng thời gian ước tính
- Số lượng children tasks

### 3. Children Tasks
- Thông tin chi tiết từng task con
- Độ phức tạp (Low/Medium/High)
- Thời gian ước tính
- Dependencies
- Độ ưu tiên
- Kỹ năng cần thiết

### 4. Assumptions & Risks
- Các giả định trong quá trình ước tính
- Các rủi ro tiềm ẩn

## Ví dụ output

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

2. Quản lý thông tin xe và tài xế (18.0h)
   - CRUD thông tin xe (6.0h, Medium)
   - CRUD thông tin tài xế (8.0h, Medium)
   - Upload ảnh xe/tài xế (4.0h, Low)
```

## Lưu ý

- Mỗi task con được giới hạn tối đa 14 giờ
- Ước tính dựa trên khả năng của một middle developer
- Kết quả có thể thay đổi tùy thuộc vào chất lượng tài liệu đầu vào
- Cần có OpenAI API Key hợp lệ để sử dụng

## Troubleshooting

### Lỗi OpenAI API:
- Kiểm tra API key có hợp lệ không
- Đảm bảo có đủ credit trong tài khoản OpenAI

### Lỗi đọc file:
- Kiểm tra đường dẫn folder có đúng không
- Đảm bảo file markdown có encoding UTF-8

### Lỗi xuất Excel:
- Kiểm tra quyền ghi file trong thư mục
- Đảm bảo không có file Excel nào đang mở 