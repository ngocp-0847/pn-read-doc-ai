#!/usr/bin/env python3
"""
EST CLI - Estimation Tool for Software Development Tasks
Sử dụng Atomic Agents và OpenAI để phân tích tài liệu và ước tính thời gian thực hiện
"""

import os
import glob
import click
import openai
import pandas as pd
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field
from atomic_agents import AtomicAgent, AgentConfig
import instructor

# Import config
from config.estimate import ESTConfig, SYSTEM_PROMPT_CONFIG, EXCEL_CONFIG

# Import context provider
from context_provider import EstimationContextManager


class Task(BaseModel):
    """Mô hình cho một task con"""
    task_id: str = Field(..., description="ID duy nhất của task")
    task_name: str = Field(..., description="Tên task")
    description: str = Field(..., description="Mô tả chi tiết task")
    complexity: str = Field(..., description=f"Độ phức tạp: {', '.join(ESTConfig.COMPLEXITY_LEVELS)}")
    estimated_hours: float = Field(..., description=f"Thời gian ước tính (giờ, {ESTConfig.MIN_TASK_HOURS}-{ESTConfig.MAX_TASK_HOURS})")
    dependencies: List[str] = Field(default=[], description="Danh sách task ID phụ thuộc")
    priority: str = Field(..., description=f"Độ ưu tiên: {', '.join(ESTConfig.PRIORITY_LEVELS)}")
    skills_required: List[str] = Field(default=[], description="Kỹ năng cần thiết")


class ParentTask(BaseModel):
    """Mô hình cho parent task"""
    parent_id: str = Field(..., description="ID duy nhất của parent task")
    parent_name: str = Field(..., description="Tên parent task")
    description: str = Field(..., description="Mô tả tổng quan")
    total_estimated_hours: float = Field(..., description="Tổng thời gian ước tính")
    children_tasks: List[Task] = Field(..., description="Danh sách các task con")


class ProjectAnalysis(BaseModel):
    """Mô hình cho phân tích dự án"""
    project_name: str = Field(..., description="Tên dự án")
    total_estimated_hours: float = Field(..., description="Tổng thời gian ước tính")
    parent_tasks: List[ParentTask] = Field(..., description="Danh sách parent tasks")
    summary: str = Field(..., description="Tóm tắt dự án")
    assumptions: List[str] = Field(default=[], description="Các giả định")
    risks: List[str] = Field(default=[], description="Các rủi ro")


class DocumentAnalysisInput(BaseModel):
    """Input schema cho việc phân tích tài liệu"""
    documents: List[str] = Field(..., description="Nội dung các tài liệu markdown")
    project_name: str = Field(..., description="Tên dự án")


class DocumentAnalysisOutput(BaseModel):
    """Output schema cho việc phân tích tài liệu"""
    analysis: ProjectAnalysis = Field(..., description="Kết quả phân tích dự án")


def read_markdown_files(folder_path: str) -> List[str]:
    """Đọc tất cả file markdown từ folder"""
    documents = []
    
    # Sử dụng cấu hình extensions
    for ext in ESTConfig.MARKDOWN_EXTENSIONS:
        pattern = os.path.join(folder_path, f"*{ext}")
        markdown_files = glob.glob(pattern)
        
        for file_path in markdown_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    documents.append(f"File: {os.path.basename(file_path)}\n{content}")
            except Exception as e:
                print(f"Lỗi khi đọc file {file_path}: {e}")
    
    return documents


def create_analysis_agent(openai_api_key: str, context_manager: EstimationContextManager = None) -> AtomicAgent:
    """Tạo agent để phân tích tài liệu với context provider"""
    client = instructor.from_openai(openai.OpenAI(api_key=openai_api_key))
    
    # Sử dụng cấu hình system prompt
    system_prompt = f"""Bạn là một chuyên gia phân tích yêu cầu phần mềm và ước tính thời gian phát triển.

{chr(10).join(SYSTEM_PROMPT_CONFIG['background'])}

Nhiệm vụ của bạn:
{chr(10).join(f"{i+1}. {step}" for i, step in enumerate(SYSTEM_PROMPT_CONFIG['steps']))}

Yêu cầu output:
{chr(10).join(f"- {instruction}" for instruction in SYSTEM_PROMPT_CONFIG['output_instructions'])}

IMPORTANT: Sử dụng thông tin từ context provider để đưa ra ước tính chính xác hơn dựa trên các dự án tương tự."""
    
    # Sử dụng cấu hình OpenAI với greedy mode
    openai_config = ESTConfig.get_openai_config()
    
    # Tạo agent config với context provider
    agent_config = AgentConfig(
        client=client,
        model=openai_config["model"],
        system_prompt=system_prompt,
        temperature=0.1,  # Low temperature for more consistent results
        max_tokens=4000   # Higher token limit for detailed analysis
    )
    
    # Add context provider if available
    if context_manager:
        agent_config.context_providers = [context_manager.context_provider]
    
    return AtomicAgent[DocumentAnalysisInput, DocumentAnalysisOutput](config=agent_config)


def validate_task_hours(analysis: ProjectAnalysis) -> List[str]:
    """Kiểm tra và báo cáo các task có thời gian không hợp lệ"""
    warnings = []
    
    for parent in analysis.parent_tasks:
        for child in parent.children_tasks:
            if not ESTConfig.validate_task_hours(child.estimated_hours):
                warnings.append(
                    f"Task '{child.task_name}' có thời gian {child.estimated_hours}h "
                    f"(nằm ngoài khoảng {ESTConfig.MIN_TASK_HOURS}-{ESTConfig.MAX_TASK_HOURS}h)"
                )
    
    return warnings


def export_to_excel(analysis: ProjectAnalysis, output_file: str):
    """Xuất kết quả phân tích ra file Excel"""
    # Tạo DataFrame cho parent tasks
    parent_data = []
    for parent in analysis.parent_tasks:
        parent_data.append({
            EXCEL_CONFIG['parent_columns'][0]: parent.parent_id,
            EXCEL_CONFIG['parent_columns'][1]: parent.parent_name,
            EXCEL_CONFIG['parent_columns'][2]: parent.description,
            EXCEL_CONFIG['parent_columns'][3]: parent.total_estimated_hours,
            EXCEL_CONFIG['parent_columns'][4]: len(parent.children_tasks)
        })
    
    # Tạo DataFrame cho children tasks
    children_data = []
    for parent in analysis.parent_tasks:
        for child in parent.children_tasks:
            children_data.append({
                EXCEL_CONFIG['children_columns'][0]: parent.parent_id,
                EXCEL_CONFIG['children_columns'][1]: parent.parent_name,
                EXCEL_CONFIG['children_columns'][2]: child.task_id,
                EXCEL_CONFIG['children_columns'][3]: child.task_name,
                EXCEL_CONFIG['children_columns'][4]: child.description,
                EXCEL_CONFIG['children_columns'][5]: child.complexity,
                EXCEL_CONFIG['children_columns'][6]: child.estimated_hours,
                EXCEL_CONFIG['children_columns'][7]: ', '.join(child.dependencies) if child.dependencies else 'None',
                EXCEL_CONFIG['children_columns'][8]: child.priority,
                EXCEL_CONFIG['children_columns'][9]: ', '.join(child.skills_required) if child.skills_required else 'None'
            })
    
    # Tạo DataFrame cho summary
    summary_data = [{
        EXCEL_CONFIG['summary_columns'][0]: analysis.project_name,
        EXCEL_CONFIG['summary_columns'][1]: analysis.total_estimated_hours,
        EXCEL_CONFIG['summary_columns'][2]: len(analysis.parent_tasks),
        EXCEL_CONFIG['summary_columns'][3]: sum(len(parent.children_tasks) for parent in analysis.parent_tasks),
        EXCEL_CONFIG['summary_columns'][4]: datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }]
    
    # Tạo Excel writer
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        # Sheet 1: Summary
        pd.DataFrame(summary_data).to_excel(writer, sheet_name=ESTConfig.EXCEL_SHEETS['summary'], index=False)
        
        # Sheet 2: Parent Tasks
        pd.DataFrame(parent_data).to_excel(writer, sheet_name=ESTConfig.EXCEL_SHEETS['parent_tasks'], index=False)
        
        # Sheet 3: Children Tasks
        pd.DataFrame(children_data).to_excel(writer, sheet_name=ESTConfig.EXCEL_SHEETS['children_tasks'], index=False)
        
        # Sheet 4: Assumptions & Risks
        assumptions_risks_data = []
        for assumption in analysis.assumptions:
            assumptions_risks_data.append({
                EXCEL_CONFIG['assumptions_risks_columns'][0]: 'Assumption', 
                EXCEL_CONFIG['assumptions_risks_columns'][1]: assumption
            })
        for risk in analysis.risks:
            assumptions_risks_data.append({
                EXCEL_CONFIG['assumptions_risks_columns'][0]: 'Risk', 
                EXCEL_CONFIG['assumptions_risks_columns'][1]: risk
            })
        
        if assumptions_risks_data:
            pd.DataFrame(assumptions_risks_data).to_excel(writer, sheet_name=ESTConfig.EXCEL_SHEETS['assumptions_risks'], index=False)
    
    print(f"✅ Đã xuất kết quả ra file: {output_file}")


@click.command()
@click.option('--folder', '-f', required=True, help='Đường dẫn đến folder chứa file markdown')
@click.option('--output', '-o', default=ESTConfig.get_environment_config()['default_output'], help='Tên file Excel output')
@click.option('--project-name', '-p', default=ESTConfig.get_environment_config()['default_project_name'], help='Tên dự án')
@click.option('--openai-key', envvar='OPENAI_API_KEY', help='OpenAI API Key')
@click.option('--use-semantic-search', is_flag=True, default=True, help='Sử dụng dsRAG semantic search để cải thiện ước tính')
@click.option('--greedy-mode', is_flag=True, default=True, help='Sử dụng greedy mode cho ước tính chi tiết')
def analyze_project(folder: str, output: str, project_name: str, openai_key: str, use_semantic_search: bool, greedy_mode: bool):
    """Phân tích tài liệu markdown và ước tính thời gian thực hiện dự án"""
    
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
    
    # Khởi tạo context manager với dsRAG
    context_manager = None
    if use_semantic_search:
        click.echo("🔍 Đang khởi tạo dsRAG context provider...")
        context_manager = EstimationContextManager(openai_key)
        click.echo("✅ dsRAG semantic search đã được kích hoạt")
    else:
        click.echo("⚠️  Semantic search đã bị tắt")
    
    # Tạo agent phân tích với context provider
    click.echo("🤖 Đang tạo AI agent với RAG context...")
    agent = create_analysis_agent(openai_key, context_manager)
    
    if greedy_mode:
        click.echo("🎯 Greedy mode đã được kích hoạt - ước tính chi tiết hơn")
    
    # Chuẩn bị input
    input_data = DocumentAnalysisInput(
        documents=documents,
        project_name=project_name
    )
    
    # Chạy phân tích
    click.echo("🔍 Đang phân tích tài liệu và ước tính thời gian...")
    try:
        result = agent.run(input_data)
        analysis = result.analysis
        
        # Hiển thị kết quả tóm tắt
        click.echo(f"\n📊 KẾT QUẢ PHÂN TÍCH:")
        click.echo(f"Tên dự án: {analysis.project_name}")
        click.echo(f"Tổng thời gian ước tính: {analysis.total_estimated_hours:.1f} giờ")
        click.echo(f"Số parent tasks: {len(analysis.parent_tasks)}")
        total_children = sum(len(parent.children_tasks) for parent in analysis.parent_tasks)
        click.echo(f"Số children tasks: {total_children}")
        
        # Kiểm tra validation
        warnings = validate_task_hours(analysis)
        if warnings:
            click.echo(f"\n⚠️  CẢNH BÁO - Các task có thời gian không hợp lệ:")
            for warning in warnings:
                click.echo(f"   {warning}")
        
        # Hiển thị chi tiết parent tasks
        click.echo(f"\n📋 PARENT TASKS:")
        for i, parent in enumerate(analysis.parent_tasks, 1):
            click.echo(f"{i}. {parent.parent_name} ({parent.total_estimated_hours:.1f}h)")
            for child in parent.children_tasks:
                click.echo(f"   - {child.task_name} ({child.estimated_hours:.1f}h, {child.complexity})")
        
        # Xuất ra Excel
        export_to_excel(analysis, output)
        
        click.echo(f"\n✅ Hoàn thành! Kết quả đã được lưu vào: {output}")
        
    except Exception as e:
        click.echo(f"❌ Lỗi trong quá trình phân tích: {e}")


if __name__ == '__main__':
    analyze_project()
