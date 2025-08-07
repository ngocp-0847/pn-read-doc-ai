# Makefile cho Document Converter CLI và EST CLI

.PHONY: help install test demo convert clean est-help est-test est-demo est-analyze

# Mặc định
help:
	@echo "📚 Document Converter CLI & EST CLI & Index CLI - Makefile"
	@echo ""
	@echo "=== DOCUMENT CONVERTER ==="
	@echo "  make install      - Cài đặt dependencies"
	@echo "  make test         - Test script với dry-run"
	@echo "  make demo         - Chạy demo chuyển đổi"
	@echo "  make convert      - Chuyển đổi file chưa có ở output"
	@echo "  make convert-force - Chuyển đổi tất cả file (kể cả đã có)"
	@echo "  make clean        - Xóa các file output"
	@echo ""
	@echo "=== EST CLI (ESTIMATION TOOL) ==="
	@echo "  make est-help     - Hiển thị help cho EST CLI"
	@echo "  make est-test     - Test EST CLI tool"
	@echo "  make est-demo     - Chạy demo phân tích với markdown_files"
	@echo "  make est-analyze  - Phân tích dự án với folder tùy chỉnh"
	@echo "  make est-setup    - Setup Qdrant cho dsRAG"
	@echo ""
	@echo "=== INDEX CLI (dsRAG INDEXING) ==="
	@echo "  make index-help   - Hiển thị help cho Index CLI"
	@echo "  make index-docs   - Index documents vào dsRAG Knowledge Base"
	@echo "  make index-search - Tìm kiếm trong Knowledge Base"
	@echo "  make index-list   - Liệt kê documents đã index"
	@echo "  make index-setup  - Setup Qdrant cho indexing"
	@echo ""
	@echo "Ví dụ sử dụng:"
	@echo "  make convert INPUT=/path/to/folder"
	@echo "  make convert INPUT=. OUTPUT=./markdown_files"
	@echo "  make est-analyze FOLDER=markdown_files PROJECT=TestProject"
	@echo "  make index-docs FOLDER=markdown_files PROJECT=TestProject"
	@echo "  make index-search QUERY='software development'"
	@echo "  make index-list FOLDER=markdown_files"

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

# Tạo thư mục cần thiết
setup:
	@echo "⚙️ Thiết lập môi trường..."
	mkdir -p markdown_output demo_output

# === EST CLI COMMANDS ===

# Hiển thị help cho EST CLI
est-help:
	@echo "🤖 EST CLI - Estimation Tool Help"
	@echo ""
	@echo "Cú pháp:"
	@echo "  python3 est_cli.py --folder <folder> [options]"
	@echo ""
	@echo "Options:"
	@echo "  --folder, -f        Đường dẫn đến folder chứa file markdown (bắt buộc)"
	@echo "  --output, -o        Tên file Excel output (mặc định: project_analysis.xlsx)"
	@echo "  --project-name, -p  Tên dự án (mặc định: Software Project)"
	@echo "  --openai-key        OpenAI API Key (có thể dùng biến môi trường OPENAI_API_KEY)"
	@echo ""
	@echo "Ví dụ:"
	@echo "  python3 est_cli.py --folder markdown_files"
	@echo "  python3 est_cli.py --folder markdown_files --project-name 'Test Project'"
	@echo "  python3 est_cli.py --folder markdown_files --output 'my_analysis.xlsx'"

# === INDEX CLI COMMANDS ===

# Hiển thị help cho Index CLI
index-help:
	@echo "📚 Index CLI - dsRAG Indexing Tool Help"
	@echo ""
	@echo "Commands:"
	@echo "  make index-docs      - Index documents vào dsRAG Knowledge Base"
	@echo "  make index-search    - Tìm kiếm trong Knowledge Base"
	@echo "  make index-list      - Liệt kê documents đã index"
	@echo "  make index-test      - Test knowledge base với query"
	@echo "  make index-setup     - Setup Qdrant cho indexing"
	@echo ""
	@echo "Setup:"
	@echo "  export OPENAI_API_KEY='your-openai-api-key'"
	@echo ""
	@echo "Ví dụ:"
	@echo "  make index-docs FOLDER=markdown_files PROJECT=TestProject"
	@echo "  make index-search QUERY='software development estimation'"
	@echo "  make index-list FOLDER=markdown_files"
	@echo "  make index-test FOLDER=markdown_files TEST_QUERY='test'"
	@echo "  make index-setup"

# Phân tích dự án với folder tùy chỉnh
est-analyze:
	@echo "🔍 Đang phân tích dự án..."
	@if [ -z "$(FOLDER)" ]; then \
		echo "❌ Vui lòng chỉ định folder: make est-analyze FOLDER=markdown_files"; \
		exit 1; \
	fi
	@if [ -z "$(PROJECT)" ]; then \
		python3 est_cli.py --folder $(FOLDER); \
	else \
		python3 est_cli.py --folder $(FOLDER) --project-name $(PROJECT); \
	fi

# Index documents vào dsRAG Knowledge Base
index-docs:
	@echo "📚 Đang index documents vào dsRAG Knowledge Base..."
	@if [ -z "$(FOLDER)" ]; then \
		echo "❌ Vui lòng chỉ định folder: make index-docs FOLDER=markdown_files"; \
		exit 1; \
	fi
	@if [ -z "$(OPENAI_API_KEY)" ]; then \
		echo "❌ Vui lòng thiết lập OPENAI_API_KEY: export OPENAI_API_KEY='your-api-key'"; \
		exit 1; \
	fi
	@if [ -z "$(PROJECT)" ]; then \
		python3 index_cli.py index --folder $(FOLDER); \
	else \
		python3 index_cli.py index --folder $(FOLDER) --project-name $(PROJECT); \
	fi

# Tìm kiếm trong Knowledge Base
index-search:
	@echo "🔍 Đang tìm kiếm trong Knowledge Base..."
	@if [ -z "$(QUERY)" ]; then \
		echo "❌ Vui lòng chỉ định query: make index-search QUERY='software development'"; \
		exit 1; \
	fi
	@if [ -z "$(OPENAI_API_KEY)" ]; then \
		echo "❌ Vui lòng thiết lập OPENAI_API_KEY: export OPENAI_API_KEY='your-api-key'"; \
		exit 1; \
	fi
	@if [ -z "$(MAX_RESULTS)" ]; then \
		python3 index_cli.py search --query "$(QUERY)"; \
	else \
		python3 index_cli.py search --query "$(QUERY)" --max-results $(MAX_RESULTS); \
	fi

# Liệt kê documents đã index
index-list:
	@echo "📚 Đang liệt kê documents đã index..."
	@if [ -z "$(FOLDER)" ]; then \
		echo "❌ Vui lòng chỉ định folder: make index-list FOLDER=markdown_files"; \
		exit 1; \
	fi
	@if [ -z "$(OPENAI_API_KEY)" ]; then \
		echo "❌ Vui lòng thiết lập OPENAI_API_KEY: export OPENAI_API_KEY='your-api-key'"; \
		exit 1; \
	fi
	@if [ -z "$(PROJECT)" ]; then \
		python3 index_cli.py index --folder $(FOLDER) --list-docs; \
	else \
		python3 index_cli.py index --folder $(FOLDER) --project-name $(PROJECT) --list-docs; \
	fi

# Test knowledge base với query cụ thể
index-test:
	@echo "🧪 Đang test knowledge base..."
	@if [ -z "$(FOLDER)" ]; then \
		echo "❌ Vui lòng chỉ định folder: make index-test FOLDER=markdown_files"; \
		exit 1; \
	fi
	@if [ -z "$(OPENAI_API_KEY)" ]; then \
		echo "❌ Vui lòng thiết lập OPENAI_API_KEY: export OPENAI_API_KEY='your-api-key'"; \
		exit 1; \
	fi
	@if [ -z "$(TEST_QUERY)" ]; then \
		python3 index_cli.py index --folder $(FOLDER) --test-query "software development"; \
	else \
		python3 index_cli.py index --folder $(FOLDER) --test-query "$(TEST_QUERY)"; \
	fi

# Setup Qdrant cho indexing
index-setup:
	@echo "⚙️ Đang setup Qdrant cho dsRAG indexing..."
	@if [ -z "$(OPENAI_API_KEY)" ]; then \
		echo "❌ Vui lòng thiết lập OPENAI_API_KEY: export OPENAI_API_KEY='your-api-key'"; \
		exit 1; \
	fi
	@echo "🔧 Tạo storage directory..."
	mkdir -p dsrag_storage/chunk_storage
	mkdir -p dsrag_storage/metadata
	mkdir -p dsrag_storage/vector_storage
	@echo "✅ Qdrant storage đã được thiết lập"
	@echo "📝 Bây giờ bạn có thể index documents:"
	@echo "   make index-docs FOLDER=markdown_files PROJECT=TestProject"
