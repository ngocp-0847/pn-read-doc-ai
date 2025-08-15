#!/usr/bin/env python3
"""
Script CLI để chuyển đổi các file PDF, XLSX, XLSM thành Markdown sử dụng Docling
Hỗ trợ RAG cho hệ thống LLM
"""

import argparse
import os
import sys
import time
import subprocess
from datetime import datetime
from pathlib import Path
from typing import List, Set, Union, Optional
import logging
from docling.document_converter import DocumentConverter


# Thiết lập logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import cấu hình
try:
    from config import (
        SUPPORTED_EXTENSIONS, SPECIAL_FORMATS, LOGGING_CONFIG, OUTPUT_CONFIG,
        DOCLING_CONFIG, ERROR_HANDLING, PERFORMANCE_CONFIG,
        RAG_CONFIG, IGNORE_PATTERNS, IGNORE_DIRECTORIES
    )
except ImportError:
    # Fallback nếu không có file config
    SUPPORTED_EXTENSIONS = {'.pdf', '.xlsx', '.xlsm', '.xls'}
    SPECIAL_FORMATS = {'.xls'}
    LOGGING_CONFIG = {'level': 'INFO', 'format': '%(asctime)s - %(levelname)s - %(message)s'}
    OUTPUT_CONFIG = {'default_output_dir': './markdown_output', 'encoding': 'utf-8'}
    DOCLING_CONFIG = {'enable_ocr': True, 'enable_table_extraction': True}
    ERROR_HANDLING = {'continue_on_error': True, 'max_retries': 3}
    PERFORMANCE_CONFIG = {'max_workers': 4, 'timeout': 300}
    RAG_CONFIG = {'include_metadata': True, 'include_tables': True}
    IGNORE_PATTERNS = ['~$*', '*.tmp', '*.bak']
    IGNORE_DIRECTORIES = ['.git', '__pycache__']

def should_ignore_path(path: Path) -> bool:
    """
    Kiểm tra xem path có nên bỏ qua không
    """
    path_str = str(path)
    
    # Kiểm tra thư mục bỏ qua
    for ignore_dir in IGNORE_DIRECTORIES:
        if ignore_dir in path_str:
            return True
    
    # Kiểm tra pattern bỏ qua
    for pattern in IGNORE_PATTERNS:
        if pattern in path_str:
            return True
    
    return False

def find_supported_files(input_paths: List[Union[str, Path]]) -> List[Path]:
    """
    Tìm tất cả các file được hỗ trợ từ danh sách input paths
    Hỗ trợ cả file đơn lẻ và thư mục
    """
    supported_files = []
    
    for input_path_str in input_paths:
        input_path = Path(input_path_str)
        
        if not input_path.exists():
            logger.warning(f"⚠️ Đường dẫn không tồn tại: {input_path}")
            continue
        
        if input_path.is_file():
            # Nếu là file đơn lẻ
            if input_path.suffix.lower() in SUPPORTED_EXTENSIONS:
                supported_files.append(input_path)
                logger.info(f"📄 Thêm file: {input_path}")
            else:
                logger.warning(f"⚠️ File không được hỗ trợ: {input_path}")
                logger.info(f"   Các định dạng được hỗ trợ: {', '.join(SUPPORTED_EXTENSIONS)}")
        
        elif input_path.is_dir():
            # Nếu là thư mục, tìm tất cả file được hỗ trợ
            logger.info(f"📁 Quét thư mục: {input_path}")
            for file_path in input_path.rglob('*'):
                # Bỏ qua các file/thư mục không mong muốn
                if should_ignore_path(file_path):
                    continue
                    
                if file_path.is_file() and file_path.suffix.lower() in SUPPORTED_EXTENSIONS:
                    supported_files.append(file_path)
                    logger.info(f"  📄 Tìm thấy: {file_path}")
        
        else:
            logger.warning(f"⚠️ Đường dẫn không phải file hoặc thư mục: {input_path}")
    
    return supported_files

def check_existing_output_files(input_files: List[Path], output_dir: Path) -> Set[str]:
    """
    Kiểm tra các file đã tồn tại ở output
    Trả về set các tên file markdown đã tồn tại
    """
    existing_files = set()
    
    if not output_dir.exists():
        return existing_files
    
    # Lấy danh sách các file markdown đã tồn tại
    for md_file in output_dir.glob('*.md'):
        existing_files.add(md_file.stem)
    
    return existing_files

def filter_files_to_convert(input_files: List[Path], output_dir: Path, force_convert: bool = False) -> List[Path]:
    """
    Lọc ra những file cần chuyển đổi
    Nếu force_convert=True, chuyển đổi tất cả
    Nếu force_convert=False, chỉ chuyển đổi file chưa có ở output
    """
    if force_convert:
        return input_files
    
    existing_files = check_existing_output_files(input_files, output_dir)
    files_to_convert = []
    
    for file_path in input_files:
        output_filename = file_path.stem + '.md'
        output_path = output_dir / output_filename
        
        # Kiểm tra xem file output đã tồn tại chưa
        if output_path.exists():
            logger.info(f"⏭️ Bỏ qua file đã tồn tại: {file_path} -> {output_path}")
        else:
            files_to_convert.append(file_path)
    
    return files_to_convert

def convert_xls_to_xlsx(file_path: Path) -> Path:
    """
    Chuyển đổi file .xls thành .xlsx sử dụng pandas
    """
    try:
        import pandas as pd
        import openpyxl
        
        logger.info(f"🔄 Đang chuyển đổi .xls thành .xlsx: {file_path}")
        
        # Đọc file .xls
        xls_file = pd.ExcelFile(file_path)
        
        # Tạo file .xlsx tạm thời
        temp_xlsx_path = file_path.with_suffix('.xlsx')
        
        # Ghi ra file .xlsx
        with pd.ExcelWriter(temp_xlsx_path, engine='openpyxl') as writer:
            for sheet_name in xls_file.sheet_names:
                df = pd.read_excel(file_path, sheet_name=sheet_name)
                df.to_excel(writer, sheet_name=sheet_name, index=False)
        
        logger.info(f"✅ Đã chuyển đổi thành công: {temp_xlsx_path}")
        return temp_xlsx_path
        
    except ImportError:
        logger.error("❌ Pandas hoặc openpyxl chưa được cài đặt. Vui lòng chạy: pip install pandas openpyxl")
        return None
    except Exception as e:
        logger.error(f"❌ Lỗi khi chuyển đổi .xls: {str(e)}")
        return None

def convert_file_to_markdown(file_path: Path, output_dir: Path, converter: DocumentConverter, max_pages: Optional[int] = None) -> bool:
    """
    Chuyển đổi một file thành Markdown với retry logic
    """
    max_retries = ERROR_HANDLING.get('max_retries', 3)
    retry_delay = ERROR_HANDLING.get('retry_delay', 1)
    
    # Kiểm tra nếu là file .xls cần xử lý đặc biệt
    temp_xlsx_path = None
    original_file_path = file_path
    
    if file_path.suffix.lower() in SPECIAL_FORMATS:
        logger.info(f"🔧 Phát hiện file đặc biệt: {file_path}")
        temp_xlsx_path = convert_xls_to_xlsx(file_path)
        if temp_xlsx_path:
            file_path = temp_xlsx_path
        else:
            logger.error(f"❌ Không thể chuyển đổi file .xls: {original_file_path}")
            return False
    
    for attempt in range(max_retries):
        try:
            logger.info(f"🔄 Đang chuyển đổi: {original_file_path} (lần thử {attempt + 1}/{max_retries})")
            
            # Chuyển đổi file với giới hạn số trang nếu được chỉ định
            if max_pages and file_path.suffix.lower() == '.pdf':
                logger.info(f"📄 Giới hạn chuyển đổi {max_pages} trang đầu tiên")
                # Sử dụng cấu hình đặc biệt cho PDF với giới hạn trang
                result = converter.convert(str(file_path), max_num_pages=max_pages)
            else:
                result = converter.convert(str(file_path))
            
            # Tạo tên file output
            output_filename = original_file_path.stem + '.md'
            output_path = output_dir / output_filename
            
            # Xuất ra Markdown
            markdown_content = result.document.export_to_markdown()
            
            # Ghi file với encoding được cấu hình
            encoding = OUTPUT_CONFIG.get('encoding', 'utf-8')
            with open(output_path, 'w', encoding=encoding) as f:
                f.write(markdown_content)
            
            logger.info(f"✅ Đã chuyển đổi thành công: {output_path}")
            
            # Xóa file tạm nếu có
            if temp_xlsx_path and temp_xlsx_path.exists():
                temp_xlsx_path.unlink()
                logger.info(f"🗑️ Đã xóa file tạm: {temp_xlsx_path}")
            
            return True
            
        except Exception as e:
            error_msg = f"❌ Lỗi khi chuyển đổi {original_file_path}: {str(e)}"
            logger.error(error_msg)
            
            # Ghi lỗi vào file log nếu được cấu hình
            if ERROR_HANDLING.get('log_errors_to_file', False):
                error_log_file = ERROR_HANDLING.get('error_log_file', 'conversion_errors.log')
                try:
                    with open(error_log_file, 'a', encoding='utf-8') as f:
                        f.write(f"{datetime.now().isoformat()} - {error_msg}\n")
                except:
                    pass
            
            # Nếu không phải lần thử cuối và được cấu hình tiếp tục
            if attempt < max_retries - 1 and ERROR_HANDLING.get('continue_on_error', True):
                logger.info(f"⏳ Chờ {retry_delay} giây trước khi thử lại...")
                time.sleep(retry_delay)
                continue
            else:
                break
    
    # Xóa file tạm nếu có lỗi
    if temp_xlsx_path and temp_xlsx_path.exists():
        temp_xlsx_path.unlink()
        logger.info(f"🗑️ Đã xóa file tạm sau lỗi: {temp_xlsx_path}")
    
    return False

def main():
    parser = argparse.ArgumentParser(
        description="Chuyển đổi các file PDF, XLSX, XLSM thành Markdown sử dụng Docling",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ví dụ sử dụng:
  # Chuyển đổi một file
  python convert_docs.py document.pdf
  
  # Chuyển đổi nhiều file
  python convert_docs.py file1.pdf file2.xlsx file3.xlsm
  
  # Chuyển đổi một thư mục
  python convert_docs.py /path/to/input/folder
  
  # Chuyển đổi kết hợp file và thư mục
  python convert_docs.py file1.pdf /path/to/folder file2.xlsx
  
  # Chỉ định thư mục output
  python convert_docs.py file1.pdf --output /path/to/output
  
  # Giới hạn số trang cho file PDF
  python convert_docs.py document.pdf --max-page 10
  
  # Chế độ verbose
  python convert_docs.py file1.pdf --verbose
  
  # Dry run để xem trước
  python convert_docs.py file1.pdf --dry-run
        """
    )
    
    parser.add_argument(
        'input_paths',
        nargs='+',
        type=str,
        help='File hoặc thư mục cần chuyển đổi (có thể chỉ định nhiều)'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        help='Thư mục output (mặc định: ./markdown_output)'
    )
    
    parser.add_argument(
        '--max-page',
        type=int,
        metavar='N',
        help='Giới hạn số trang đầu tiên cần chuyển đổi (chỉ áp dụng cho file PDF)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Hiển thị thông tin chi tiết'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Chỉ hiển thị danh sách file sẽ chuyển đổi, không thực hiện chuyển đổi'
    )
    
    parser.add_argument(
        '--force-convert',
        action='store_true',
        help='Chuyển đổi tất cả file, kể cả những file đã tồn tại ở output'
    )
    
    args = parser.parse_args()
    
    # Kiểm tra giá trị max_page
    if args.max_page is not None and args.max_page <= 0:
        logger.error("❌ Giá trị --max-page phải lớn hơn 0")
        sys.exit(1)
    
    # Thiết lập logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Tìm các file được hỗ trợ
    logger.info(f"🔍 Đang tìm kiếm các file từ {len(args.input_paths)} input path(s):")
    for path in args.input_paths:
        logger.info(f"  - {path}")
    
    supported_files = find_supported_files(args.input_paths)
    
    if not supported_files:
        logger.warning("⚠️ Không tìm thấy file nào được hỗ trợ")
        logger.info(f"Các định dạng được hỗ trợ: {', '.join(SUPPORTED_EXTENSIONS)}")
        sys.exit(0)
    
    logger.info(f"📁 Tìm thấy {len(supported_files)} file được hỗ trợ:")
    for file_path in supported_files:
        logger.info(f"  - {file_path}")
    
    # Hiển thị thông tin về giới hạn trang nếu được chỉ định
    if args.max_page:
        logger.info(f"📄 Giới hạn chuyển đổi: {args.max_page} trang đầu tiên (chỉ áp dụng cho file PDF)")
    
    if args.dry_run:
        logger.info("🔍 Chế độ dry-run: Chỉ hiển thị danh sách file")
        return
    
    # Tạo thư mục output
    default_output = OUTPUT_CONFIG.get('default_output_dir', './markdown_output')
    output_dir = Path(args.output) if args.output else Path(default_output)
    output_dir.mkdir(exist_ok=True)
    logger.info(f"📂 Thư mục output: {output_dir}")
    
    # Lọc ra những file cần chuyển đổi
    files_to_convert = filter_files_to_convert(supported_files, output_dir, args.force_convert)
    
    logger.info(f"🔄 Sẽ chuyển đổi {len(files_to_convert)}/{len(supported_files)} file:")
    for file_path in files_to_convert:
        logger.info(f"  - {file_path}")
    
    if len(files_to_convert) == 0:
        logger.info("✅ Tất cả file đã được chuyển đổi trước đó!")
        return
    
    # Khởi tạo converter
    try:
        converter = DocumentConverter()
        logger.info("🚀 Đã khởi tạo Docling converter")
    except Exception as e:
        logger.error(f"❌ Lỗi khi khởi tạo Docling converter: {str(e)}")
        sys.exit(1)
    
    # Chuyển đổi các file
    success_count = 0
    total_count = len(files_to_convert)
    
    for file_path in files_to_convert:
        if convert_file_to_markdown(file_path, output_dir, converter, args.max_page):
            success_count += 1
    
    # Tổng kết
    logger.info("=" * 50)
    logger.info("📊 TỔNG KẾT:")
    logger.info(f"  - Tổng số file: {total_count}")
    logger.info(f"  - Chuyển đổi thành công: {success_count}")
    logger.info(f"  - Thất bại: {total_count - success_count}")
    logger.info(f"  - Thư mục output: {output_dir.absolute()}")
    if args.max_page:
        logger.info(f"  - Giới hạn trang: {args.max_page} trang đầu tiên (chỉ PDF)")
    
    if success_count == total_count:
        logger.info("🎉 Tất cả file đã được chuyển đổi thành công!")
    else:
        logger.warning(f"⚠️ Có {total_count - success_count} file chuyển đổi thất bại")

if __name__ == "__main__":
    main() 