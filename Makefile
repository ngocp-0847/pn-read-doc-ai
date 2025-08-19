# Makefile cho Document Converter CLI

.PHONY: help setup convert convert-force convert-current clean

# Mặc định
help:
	@echo "📚 Document Converter CLI - Makefile"
	@echo ""
	@echo "=== DOCUMENT CONVERTER COMMANDS ==="
	@echo "  make help             - Hiển thị help này"
	@echo "  make setup            - Tạo thư mục cần thiết"
	@echo "  make convert          - Chuyển đổi documents (cần INPUT và OUTPUT)"
	@echo "  make convert-force    - Chuyển đổi tất cả file (force mode)"
	@echo "  make convert-current  - Chuyển đổi thư mục hiện tại"
	@echo "  make clean            - Xóa các file output"
	@echo ""
	@echo "=== VÍ DỤ SỬ DỤNG ==="
	@echo "  make convert INPUT=/path/to/folder OUTPUT=./markdown_files"
	@echo "  make convert-force INPUT=/path/to/folder OUTPUT=./markdown_files"
	@echo "  make convert-current"
	@echo "  make clean"
	@echo ""
	@echo "=== TÙY CHỌN ==="
	@echo "  INPUT                 - Thư mục chứa file nguồn"
	@echo "  OUTPUT                - Thư mục output (mặc định: markdown_output)"

# Tạo thư mục cần thiết
setup:
	@echo "⚙️ Thiết lập môi trường..."
	mkdir -p markdown_output
	mkdir -p source_files
	@echo "✅ Đã tạo thư mục markdown_output và source_files"

# Chuyển đổi documents
convert:
	@echo "🔄 Đang chuyển đổi documents..."
	@if [ -z "$(INPUT)" ]; then \
		echo "❌ Vui lòng chỉ định thư mục input: make convert INPUT=/path/to/folder"; \
		echo "💡 Hoặc sử dụng: make convert-current để chuyển đổi thư mục hiện tại"; \
		exit 1; \
	fi
	@if [ ! -d "$(INPUT)" ]; then \
		echo "❌ Thư mục không tồn tại: $(INPUT)"; \
		exit 1; \
	fi
	@if [ -z "$(OUTPUT)" ]; then \
		python convert_docs.py "$(INPUT)" --verbose; \
	else \
		python convert_docs.py "$(INPUT)" --output "$(OUTPUT)" --verbose; \
	fi
	@echo "✅ Hoàn thành chuyển đổi!"

# Chuyển đổi documents với force convert
convert-force:
	@echo "🔄 Đang chuyển đổi documents (force mode)..."
	@if [ -z "$(INPUT)" ]; then \
		echo "❌ Vui lòng chỉ định thư mục input: make convert-force INPUT=/path/to/folder"; \
		echo "💡 Hoặc sử dụng: make convert-current để chuyển đổi thư mục hiện tại"; \
		exit 1; \
	fi
	@if [ ! -d "$(INPUT)" ]; then \
		echo "❌ Thư mục không tồn tại: $(INPUT)"; \
		exit 1; \
	fi
	@if [ -z "$(OUTPUT)" ]; then \
		python convert_docs.py "$(INPUT)" --force-convert --verbose; \
	else \
		python convert_docs.py "$(INPUT)" --output "$(OUTPUT)" --force-convert --verbose; \
	fi
	@echo "✅ Hoàn thành chuyển đổi (force mode)!"

# Chuyển đổi tất cả file trong thư mục hiện tại
convert-current:
	@echo "🔄 Đang chuyển đổi tất cả file trong thư mục hiện tại..."
	@if [ ! -f convert_docs.py ]; then \
		echo "❌ Không tìm thấy convert_docs.py trong thư mục hiện tại"; \
		echo "💡 Vui lòng chạy lệnh từ thư mục gốc của project"; \
		exit 1; \
	fi
	python convert_docs.py . --verbose
	@echo "✅ Hoàn thành chuyển đổi thư mục hiện tại!"

# Dry run để kiểm tra
dry-run:
	@echo "🔍 Chế độ dry-run - kiểm tra file sẽ được chuyển đổi..."
	@if [ -z "$(INPUT)" ]; then \
		echo "❌ Vui lòng chỉ định thư mục input: make dry-run INPUT=/path/to/folder"; \
		exit 1; \
	fi
	@if [ ! -d "$(INPUT)" ]; then \
		echo "❌ Thư mục không tồn tại: $(INPUT)"; \
		exit 1; \
	fi
	python convert_docs.py "$(INPUT)" --dry-run --verbose

# Dọn dẹp files output
clean:
	@echo "🗑️ Đang dọn dẹp files output..."
	@if [ -d "markdown_output" ]; then \
		rm -rf markdown_output/*; \
		echo "✅ Đã xóa nội dung thư mục markdown_output"; \
	else \
		echo "ℹ️ Thư mục markdown_output không tồn tại"; \
	fi
	@# Xóa các file .xlsx tạm nếu có
	@find . -name "*.xlsx" -type f -newer convert_docs.py -delete 2>/dev/null || true
	@echo "✅ Hoàn thành dọn dẹp!"

# Test với requirements
test-requirements:
	@echo "🧪 Kiểm tra requirements..."
	@python -c "import docling; print('✅ Docling installed')" || echo "❌ Docling not installed"
	@python -c "import pandas; print('✅ Pandas installed')" || echo "❌ Pandas not installed"
	@python -c "import openpyxl; print('✅ Openpyxl installed')" || echo "❌ Openpyxl not installed"

# Hiển thị thông tin project
info:
	@echo "📋 Document Converter CLI Info"
	@echo ""
	@echo "📁 Project structure:"
	@ls -la | grep -E "(convert_docs|config|docs|requirements|README|Makefile)"
	@echo ""
	@echo "📦 Python packages:"
	@make test-requirements
	@echo ""
	@echo "📂 Output directories:"
	@ls -ld markdown_output 2>/dev/null || echo "   markdown_output: Chưa tạo"
	@ls -ld source_files 2>/dev/null || echo "   source_files: Chưa tạo"

# Install dependencies
install:
	@echo "📦 Đang cài đặt dependencies..."
	pip install -r requirements.txt
	@echo "✅ Đã cài đặt xong dependencies!"

# Lệnh nhanh để test
quick-test:
	@echo "⚡ Quick test - dry run thư mục hiện tại..."
	python convert_docs.py . --dry-run