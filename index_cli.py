#!/usr/bin/env python3
"""
Index CLI - Tool để index dữ liệu vào dsRAG Knowledge Base
Sử dụng Qdrant để lưu trữ vector embeddings
"""

import os
import glob
import click
import openai
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

# Import dsRAG components
from dsrag.knowledge_base import KnowledgeBase
from dsrag.database.vector import BasicVectorDB
from dsrag.database.chunk import BasicChunkDB
from dsrag.embedding import OpenAIEmbedding
from dsrag.reranker import CohereReranker
from dsrag.llm import OpenAIChatAPI
from dsrag.dsparse.file_parsing.file_system import LocalFileSystem

# Import context provider
from context_provider import EstimationContextManager

# Import config
from config.estimate import ESTConfig


def read_markdown_files(folder_path: str) -> List[Dict[str, str]]:
    """Đọc tất cả file markdown từ folder và trả về với metadata"""
    documents = []
    
    # Sử dụng cấu hình extensions
    for ext in ESTConfig.MARKDOWN_EXTENSIONS:
        pattern = os.path.join(folder_path, f"*{ext}")
        markdown_files = glob.glob(pattern)
        
        for file_path in markdown_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    documents.append({
                        'file_path': file_path,
                        'file_name': os.path.basename(file_path),
                        'content': content,
                        'size': len(content),
                        'modified': datetime.fromtimestamp(os.path.getmtime(file_path))
                    })
            except Exception as e:
                print(f"Lỗi khi đọc file {file_path}: {e}")
    
    return documents


def create_knowledge_base(storage_directory: str = "./dsrag_storage") -> KnowledgeBase:
    """Tạo dsRAG KnowledgeBase với các components mặc định"""
    # Create storage directory
    os.makedirs(storage_directory, exist_ok=True)
    
    # Initialize components
    embedding = OpenAIEmbedding(
        model="text-embedding-3-small"
    )
    
    reranker = CohereReranker()  # Sử dụng CohereReranker thay vì NoReranker
    
    llm = OpenAIChatAPI(
        model="gpt-4o-mini"
    )
    
    # Create KnowledgeBase với API mới
    knowledge_base = KnowledgeBase(
        kb_id="project_documents",
        title="Project Documents Knowledge Base",
        description="Knowledge base for software project estimation",
        storage_directory=storage_directory,
        embedding_model=embedding,
        reranker=reranker,
        auto_context_model=llm,
        exists_ok=True
    )
    
    return knowledge_base


def index_documents_to_kb(knowledge_base: KnowledgeBase, documents: List[Dict[str, str]], project_name: str):
    """Index documents vào knowledge base"""
    indexed_count = 0
    total_size = 0
    
    for doc in documents:
        try:
            # Tạo doc_id duy nhất
            doc_id = f"{project_name}_{doc['file_name'].replace('.', '_')}"
            
            # Thêm document vào knowledge base với API mới
            knowledge_base.add_document(
                doc_id=doc_id,
                text=doc['content'],
                document_title=f"{doc['file_name']} - {project_name}",
                metadata={
                    'project_name': project_name,
                    'file_name': doc['file_name'],
                    'file_path': doc['file_path'],
                    'size': doc['size']
                }
            )
            
            indexed_count += 1
            total_size += doc['size']
            
            print(f"✅ Đã index: {doc['file_name']} ({doc['size']} chars)")
            
        except Exception as e:
            print(f"❌ Lỗi khi index {doc['file_name']}: {e}")
    
    return indexed_count, total_size


def test_knowledge_base(knowledge_base: KnowledgeBase, test_query: str = "software development estimation"):
    """Test knowledge base với query mẫu"""
    try:
        print(f"\n🔍 Testing knowledge base với query: '{test_query}'")
        
        results = knowledge_base.query(
            search_queries=[test_query],
            rse_params={
                "max_length": 5,
                "overall_max_length": 10,
                "minimum_value": 0.7,
                "irrelevant_chunk_penalty": 0.3
            }
        )
        
        print(f"✅ Tìm thấy {len(results)} kết quả:")
        for i, result in enumerate(results, 1):
            print(f"  {i}. {result.get('title', 'Unknown')} (relevance: {result.get('relevance', 0):.3f})")
            print(f"     Content: {result.get('content', '')[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Lỗi khi test knowledge base: {e}")
        return False


def list_indexed_documents(knowledge_base: KnowledgeBase):
    """Liệt kê các documents đã được index"""
    try:
        # Lấy thông tin từ knowledge base metadata
        kb_metadata = knowledge_base.kb_metadata
        print(f"📚 Knowledge Base: {kb_metadata.get('title', 'Unknown')}")
        print(f"   ID: {knowledge_base.kb_id}")
        print(f"   Description: {kb_metadata.get('description', 'No description')}")
        
        # Thử query để xem có documents nào không
        try:
            results = knowledge_base.query(
                search_queries=["test"],
                rse_params={"max_length": 1}
            )
            if results:
                print(f"✅ Knowledge base có dữ liệu và sẵn sàng query")
            else:
                print("📭 Chưa có documents nào được index hoặc query trả về rỗng")
        except Exception as e:
            print(f"⚠️  Không thể query knowledge base: {e}")
            
    except Exception as e:
        print(f"❌ Lỗi khi liệt kê documents: {e}")


@click.command()
@click.option('--folder', '-f', required=True, help='Đường dẫn đến folder chứa file markdown')
@click.option('--project-name', '-p', default='default_project', help='Tên dự án cho indexing')
@click.option('--openai-key', envvar='OPENAI_API_KEY', help='OpenAI API Key')
@click.option('--storage-dir', '-s', default='./dsrag_storage', help='Thư mục lưu trữ dsRAG')
@click.option('--test-query', '-t', help='Query để test knowledge base sau khi index')
@click.option('--list-docs', is_flag=True, help='Liệt kê documents đã index')
@click.option('--force-reindex', is_flag=True, help='Force reindex tất cả documents')
def index_documents(folder: str, project_name: str, openai_key: str, storage_dir: str, 
                   test_query: str, list_docs: bool, force_reindex: bool):
    """Index documents markdown vào dsRAG Knowledge Base"""
    
    if not openai_key:
        click.echo("❌ Lỗi: Cần cung cấp OpenAI API Key qua --openai-key hoặc biến môi trường OPENAI_API_KEY")
        return
    
    if not os.path.exists(folder):
        click.echo(f"❌ Lỗi: Folder {folder} không tồn tại")
        return
    
    click.echo(f"📁 Đang đọc tài liệu từ folder: {folder}")
    documents = read_markdown_files(folder)
    
    if not documents:
        click.echo("❌ Lỗi: Không tìm thấy file markdown nào trong folder")
        return
    
    click.echo(f"📄 Đã tìm thấy {len(documents)} tài liệu")
    
    # Tạo knowledge base
    click.echo("🔧 Đang khởi tạo dsRAG Knowledge Base...")
    try:
        knowledge_base = create_knowledge_base(storage_dir)
        click.echo("✅ Knowledge Base đã được khởi tạo")
    except Exception as e:
        click.echo(f"❌ Lỗi khi khởi tạo Knowledge Base: {e}")
        return
    
    # Index documents
    click.echo(f"📚 Đang index {len(documents)} documents cho project: {project_name}")
    indexed_count, total_size = index_documents_to_kb(knowledge_base, documents, project_name)
    
    click.echo(f"\n📊 KẾT QUẢ INDEXING:")
    click.echo(f"  - Documents đã index: {indexed_count}/{len(documents)}")
    click.echo(f"  - Tổng kích thước: {total_size:,} characters")
    click.echo(f"  - Storage directory: {storage_dir}")
    
    # Test knowledge base nếu có query
    if test_query:
        test_knowledge_base(knowledge_base, test_query)
    
    # Liệt kê documents nếu được yêu cầu
    if list_docs:
        list_indexed_documents(knowledge_base)
    
    click.echo(f"\n✅ Hoàn thành indexing! Knowledge Base đã sẵn sàng cho EST CLI")


@click.command()
@click.option('--openai-key', envvar='OPENAI_API_KEY', help='OpenAI API Key')
@click.option('--storage-dir', '-s', default='./dsrag_storage', help='Thư mục lưu trữ dsRAG')
@click.option('--query', '-q', required=True, help='Query để tìm kiếm')
@click.option('--max-results', '-m', default=5, help='Số kết quả tối đa')
def search_documents(openai_key: str, storage_dir: str, query: str, max_results: int):
    """Tìm kiếm trong dsRAG Knowledge Base"""
    
    if not openai_key:
        click.echo("❌ Lỗi: Cần cung cấp OpenAI API Key")
        return
    
    click.echo(f"🔍 Đang tìm kiếm: '{query}'")
    
    try:
        knowledge_base = create_knowledge_base(storage_dir)
        
        results = knowledge_base.query(
            search_queries=[query],
            rse_params={
                "max_length": max_results,
                "overall_max_length": max_results * 2,
                "minimum_value": 0.7,
                "irrelevant_chunk_penalty": 0.3
            }
        )
        print("results", query, results)
        if not results:
            click.echo("❌ Không tìm thấy kết quả nào")
            return
        
        click.echo(f"\n📚 Tìm thấy {len(results)} kết quả:")
        for i, result in enumerate(results, 1):
            click.echo(f"\n{i}. {result.get('title', 'Unknown')}")
            click.echo(f"   Relevance: {result.get('relevance', 0):.3f}")
            click.echo(f"   Content: {result.get('content', '')[:200]}...")
            
    except Exception as e:
        click.echo(f"❌ Lỗi khi tìm kiếm: {e}")


@click.group()
def cli():
    """Index CLI - Tool để index và tìm kiếm dữ liệu với dsRAG"""
    pass


cli.add_command(index_documents, name='index')
cli.add_command(search_documents, name='search')


if __name__ == '__main__':
    cli() 