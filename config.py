"""
Cấu hình cho Document Converter CLI
"""

# Các định dạng file được hỗ trợ
SUPPORTED_EXTENSIONS = {
    '.pdf',    # PDF files
    '.xlsx',   # Excel files (new format)
    '.xlsm',   # Excel files with macros
    '.xls',    # Excel files (old format) - cần xử lý đặc biệt
    '.docx',   # Word documents
    '.pptx',   # PowerPoint presentations
}

# Các định dạng cần xử lý đặc biệt (không được Docling hỗ trợ trực tiếp)
SPECIAL_FORMATS = {
    '.xls',    # Excel files (old format) - cần chuyển đổi trước
}

# Cấu hình logging
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(levelname)s - %(message)s',
    'date_format': '%Y-%m-%d %H:%M:%S'
}

# Cấu hình output
OUTPUT_CONFIG = {
    'default_output_dir': './markdown_output',
    'encoding': 'utf-8',
    'create_backup': False,
    'overwrite_existing': True
}

# Cấu hình Docling
DOCLING_CONFIG = {
    'enable_ocr': True,
    'enable_table_extraction': True,
    'enable_image_extraction': True,
    'language': 'auto'  # 'auto', 'ja', 'en', 'vi', etc.
}

# Cấu hình xử lý lỗi
ERROR_HANDLING = {
    'continue_on_error': True,
    'max_retries': 3,
    'retry_delay': 1,  # seconds
    'log_errors_to_file': True,
    'error_log_file': 'conversion_errors.log'
}

# Cấu hình hiệu suất
PERFORMANCE_CONFIG = {
    'max_workers': 4,  # Số luồng tối đa cho xử lý song song
    'chunk_size': 1024 * 1024,  # 1MB chunks
    'timeout': 300,  # 5 phút timeout cho mỗi file
}

# Cấu hình RAG optimization
RAG_CONFIG = {
    'include_metadata': True,
    'include_tables': True,
    'include_images': False,  # Tắt để giảm kích thước
    'include_footnotes': True,
    'include_headers': True,
    'markdown_format': 'standard',  # 'standard', 'github', 'gitlab'
}

# Cấu hình file patterns để bỏ qua
IGNORE_PATTERNS = [
    '~$*',           # Temporary files
    '*.tmp',
    '*.bak',
    'Thumbs.db',
    '.DS_Store',
    '*.log'
]

# Cấu hình thư mục bỏ qua
IGNORE_DIRECTORIES = [
    '.git',
    '.svn',
    '__pycache__',
    'node_modules',
    '.vscode',
    '.idea'
] 