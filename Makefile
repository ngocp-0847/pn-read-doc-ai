# Makefile cho Document Converter CLI

.PHONY: help install test demo convert clean

# Mặc định
help:
	@echo "📚 Document Converter CLI - Makefile"
	@echo ""
	@echo "Các lệnh có sẵn:"
	@echo "  make install      - Cài đặt dependencies"
	@echo "  make test         - Test script với dry-run"
	@echo "  make demo         - Chạy demo chuyển đổi"
	@echo "  make convert      - Chuyển đổi file chưa có ở output"
	@echo "  make convert-force - Chuyển đổi tất cả file (kể cả đã có)"
	@echo "  make clean        - Xóa các file output"
	@echo "  make help         - Hiển thị trợ giúp này"
	@echo ""
	@echo "Ví dụ sử dụng:"
	@echo "  make convert INPUT=/path/to/folder"
	@echo "  make convert INPUT=. OUTPUT=./markdown_files"
	@echo "  make convert-force INPUT=. OUTPUT=./markdown_files"

# Cài đặt dependencies
install:
	@echo "🔧 Đang cài đặt dependencies..."
	pip install -r requirements.txt
	@echo "✅ Cài đặt hoàn tất!"

# Cài đặt dependencies cho file .xls
install-xls:
	@echo "🔧 Đang cài đặt dependencies cho file .xls..."
	pip install pandas openpyxl xlrd
	@echo "✅ Cài đặt dependencies cho .xls hoàn tất!"

# Test script
test:
	@echo "🧪 Đang test script..."
	python3 convert_docs.py . --dry-run --verbose

# Chạy demo
demo:
	@echo "🎬 Đang chạy demo..."
	python3 demo.py

# Chuyển đổi documents
convert:
	@echo "🔄 Đang chuyển đổi documents..."
	@if [ -z "$(INPUT)" ]; then \
		echo "❌ Vui lòng chỉ định thư mục input: make convert INPUT=/path/to/folder"; \
		exit 1; \
	fi
	@if [ -z "$(OUTPUT)" ]; then \
		python3 convert_docs.py $(INPUT) --verbose; \
	else \
		python3 convert_docs.py $(INPUT) --output $(OUTPUT) --verbose; \
	fi

# Chuyển đổi documents với force convert
convert-force:
	@echo "🔄 Đang chuyển đổi documents (force mode)..."
	@if [ -z "$(INPUT)" ]; then \
		echo "❌ Vui lòng chỉ định thư mục input: make convert-force INPUT=/path/to/folder"; \
		exit 1; \
	fi
	@if [ -z "$(OUTPUT)" ]; then \
		python3 convert_docs.py $(INPUT) --force-convert --verbose; \
	else \
		python3 convert_docs.py $(INPUT) --output $(OUTPUT) --force-convert --verbose; \
	fi

# Chuyển đổi tất cả file trong thư mục hiện tại
convert-current:
	@echo "🔄 Đang chuyển đổi tất cả file trong thư mục hiện tại..."
	python3 convert_docs.py . --verbose

# Xóa các file output
clean:
	@echo "🧹 Đang dọn dẹp..."
	rm -rf markdown_output demo_output conversion_errors.log
	@echo "✅ Dọn dẹp hoàn tất!"

# Kiểm tra cài đặt
check:
	@echo "🔍 Kiểm tra cài đặt..."
	@python3 -c "import docling; print('✅ Docling đã được cài đặt')" || echo "❌ Docling chưa được cài đặt"
	@python3 -c "import pathlib; print('✅ Pathlib đã có sẵn')"
	@echo "✅ Kiểm tra hoàn tất!"

# Hiển thị thông tin
info:
	@echo "📊 Thông tin hệ thống:"
	@echo "  Python version: $(shell python3 --version)"
	@echo "  Current directory: $(shell pwd)"
	@echo "  Files in current directory:"
	@ls -la *.py *.md *.txt *.sh Makefile 2>/dev/null || echo "  (Không có file script)"

# Tạo thư mục cần thiết
setup:
	@echo "⚙️ Thiết lập môi trường..."
	mkdir -p markdown_output demo_output
	@echo "✅ Thiết lập hoàn tất!" 