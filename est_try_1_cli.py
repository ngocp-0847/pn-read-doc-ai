#!/usr/bin/env python3
"""
EST CLI - Estimation Tool for Software Development Tasks
Sử dụng Atomic Agents và OpenAI để phân tích tài liệu và ước tính thời gian thực hiện
"""

import os
import glob
import click
import openai
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field
from openai import OpenAI
import instructor
from atomic_agents import AtomicAgent, AgentConfig, BasicChatInputSchema, BaseIOSchema
from atomic_agents.context import SystemPromptGenerator, ChatHistory
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import config
from config.estimate import ESTConfig

# Import context provider
from context_provider import ProjectEstimateContextProvider


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


class ProjectEstimateOutputSchema(BaseIOSchema):
    """
    Schema cho output của agent phân tích dự án
    """
    analysis: ProjectAnalysis = Field(..., description="Kết quả phân tích dự án")
    confidence_score: float = Field(..., description="Độ tin cậy của ước tính (0-1)")
    reasoning: str = Field(..., description="Lý do cho các ước tính")


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


def create_analysis_agent(openai_api_key: str, context_provider: ProjectEstimateContextProvider = None):
    """Tạo AtomicAgent để phân tích tài liệu với SystemPromptGenerator"""
    
    # Set up the system prompt using SystemPromptGenerator
    system_prompt_generator = SystemPromptGenerator(
        background=[
            "Bạn là một chuyên gia phân tích yêu cầu phần mềm và ước tính thời gian phát triển.",
            "Bạn có kinh nghiệm sâu rộng trong việc phân tích tài liệu kỹ thuật và đưa ra ước tính chính xác.",
            "Bạn hiểu rõ các phương pháp ước tính phần mềm như Planning Poker, Expert Judgment, và Analogous Estimation."
        ],
        steps=[
            "Phân tích tài liệu markdown để hiểu yêu cầu và phạm vi dự án.",
            "Chia nhỏ dự án thành các parent tasks chính và children tasks chi tiết.",
            "Ước tính thời gian cho từng task dựa trên độ phức tạp và kinh nghiệm.",
            "Đánh giá độ ưu tiên và dependencies giữa các tasks.",
            "Xác định các rủi ro và giả định quan trọng.",
            "Tạo tóm tắt tổng quan về dự án và kết quả phân tích."
        ],
        output_instructions=[
            "Trả về kết quả theo format ProjectAnalysis với đầy đủ thông tin.",
            "Đảm bảo thời gian ước tính nằm trong khoảng hợp lệ.",
            "Cung cấp lý do chi tiết cho các ước tính.",
            "Đánh giá độ tin cậy của ước tính."
        ]
    )

    # Initialize OpenAI client with instructor
    client = instructor.from_openai(OpenAI(api_key=openai_api_key))

    # Initialize the agent
    agent = AtomicAgent[BasicChatInputSchema, ProjectEstimateOutputSchema](
        config=AgentConfig(
            client=client,
            model=ESTConfig.DEFAULT_MODEL,
            system_prompt_generator=system_prompt_generator,
            history=ChatHistory(),
        )
    )
    agent.register_context_provider("spectification", context_provider)
    return agent


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

def export_to_markdown(analysis: ProjectAnalysis, output_file: str):
    """Xuất kết quả phân tích ra file Markdown"""
    lines = []
    lines.append(f"# KẾT QUẢ PHÂN TÍCH DỰ ÁN: {analysis.project_name}")
    lines.append("")
    lines.append(f"- Tổng thời gian ước tính: **{analysis.total_estimated_hours:.1f} giờ**")
    lines.append(f"- Số parent tasks: **{len(analysis.parent_tasks)}**")
    total_children = sum(len(parent.children_tasks) for parent in analysis.parent_tasks)
    lines.append(f"- Số children tasks: **{total_children}**")
    lines.append("")
    if getattr(analysis, 'summary', None):
        lines.append("## Tóm tắt")
        lines.append(analysis.summary)
        lines.append("")
    lines.append("## Parent Tasks")
    for idx, parent in enumerate(analysis.parent_tasks, 1):
        lines.append(f"### {idx}. {parent.parent_name} ({parent.total_estimated_hours:.1f}h)")
        if parent.description:
            lines.append(parent.description)
        lines.append("")
        if parent.children_tasks:
            lines.append("| Task ID | Tên Task | Mô tả | Độ phức tạp | Ước tính (giờ) | Phụ thuộc | Ưu tiên | Kỹ năng |")
            lines.append("|---|---|---|---|---:|---|---|---|")
            for child in parent.children_tasks:
                dependencies = ", ".join(child.dependencies) if child.dependencies else "None"
                skills = ", ".join(child.skills_required) if child.skills_required else "None"
                lines.append(
                    f"| {child.task_id} | {child.task_name} | {child.description} | {child.complexity} | {child.estimated_hours:.1f} | {dependencies} | {child.priority} | {skills} |"
                )
            lines.append("")
    if analysis.assumptions:
        lines.append("## Assumptions")
        for a in analysis.assumptions:
            lines.append(f"- {a}")
        lines.append("")
    if analysis.risks:
        lines.append("## Risks")
        for r in analysis.risks:
            lines.append(f"- {r}")
        lines.append("")

    output_path = Path(output_file)
    if output_path.suffix.lower() != ".md":
        # Đảm bảo xuất ra đuôi .md
        output_path = output_path.with_suffix('.md')

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))

    print(f"✅ Đã xuất kết quả ra file: {str(output_path)}")


@click.command()
@click.option('--folder', '-f', required=True, help='Đường dẫn đến folder chứa file markdown')
@click.option('--output', '-o', default=ESTConfig.get_environment_config()['default_output'], help='Tên file Markdown output (.md)')
@click.option('--project-name', '-p', default=ESTConfig.get_environment_config()['default_project_name'], help='Tên dự án')
@click.option('--openai-key', envvar='OPENAI_API_KEY', help='OpenAI API Key')
@click.option('--use-semantic-search', is_flag=True, default=True, help='Sử dụng dsRAG semantic search để cải thiện ước tính')
@click.option('--greedy-mode', is_flag=True, default=True, help='Sử dụng greedy mode cho ước tính chi tiết')
@click.option('--index', is_flag=True, default=False, help='Index toàn bộ tài liệu vào dsRAG trước khi phân tích')
def analyze_project(folder: str, output: str, project_name: str, openai_key: str, use_semantic_search: bool, greedy_mode: bool, index: bool):
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
    
    # Khởi tạo context provider với dsRAG
    context_provider = None
    if use_semantic_search:
        click.echo("🔍 Đang khởi tạo dsRAG context provider...")
        context_provider = ProjectEstimateContextProvider(openai_key)
        click.echo("✅ dsRAG semantic search đã được kích hoạt")
    else:
        click.echo("⚠️  Semantic search đã bị tắt")
    
    # Index tài liệu vào dsRAG trước khi phân tích nếu được yêu cầu
    if index:
        if not context_provider:
            click.echo("❌ Không thể index khi semantic search bị tắt. Hãy bật --use-semantic-search.")
        else:
            click.echo("📚 Đang index tài liệu vào dsRAG (get_context_for_project)...")
            try:
                context_provider.get_context_for_project(f"Project: {project_name}", documents)
                click.echo("✅ Index hoàn tất.")
            except Exception as e:
                click.echo(f"⚠️ Lỗi khi index tài liệu: {e}")
    
    # Tạo agent phân tích với SystemPromptGenerator
    click.echo("🤖 Đang tạo AI agent với SystemPromptGenerator...")
    agent = create_analysis_agent(openai_key, context_provider)
    
    if greedy_mode:
        click.echo("🎯 Greedy mode đã được kích hoạt - ước tính chi tiết hơn")
    
    # Chuẩn bị input cho agent
    user_message = f"""Phân tích các tài liệu sau và ước tính thời gian thực hiện dự án '{project_name}':

{chr(10).join(documents)}

Hãy phân tích chi tiết và tạo ra:
1. Danh sách các parent tasks chính
2. Mỗi parent task có các children tasks cụ thể
3. Ước tính thời gian cho từng task
4. Đánh giá độ phức tạp và ưu tiên
5. Xác định các rủi ro và giả định

Trả về kết quả theo format JSON với schema ProjectAnalysis."""
    
    # Chạy phân tích với AtomicAgent
    click.echo("🔍 Đang phân tích tài liệu và ước tính thời gian...")
    analysis = None
    
    try:
        # Use AtomicAgent to get response
        response = agent.run(BasicChatInputSchema(chat_message=user_message))
        
        # Extract analysis from response
        if hasattr(response, 'analysis'):
            analysis = response.analysis
        elif isinstance(response, ProjectAnalysis):
            analysis = response
        print("analysis: ", analysis)
        # Validate that analysis has all required fields
        if not hasattr(analysis, 'summary') or not analysis.summary:
            # Generate a default summary if missing
            analysis.summary = f"Phân tích dự án {analysis.project_name} với tổng thời gian ước tính {analysis.total_estimated_hours:.1f} giờ, bao gồm {len(analysis.parent_tasks)} parent tasks và {sum(len(parent.children_tasks) for parent in analysis.parent_tasks)} children tasks."
        
        # Display confidence score if available
        if hasattr(response, 'confidence_score'):
            click.echo(f"🎯 Độ tin cậy ước tính: {response.confidence_score:.2f}")
        
        # Display reasoning if available
        if hasattr(response, 'reasoning'):
            click.echo(f"💭 Lý do ước tính: {response.reasoning}")
        
    except Exception as e:
        click.echo(f"❌ Lỗi trong quá trình phân tích: {e}")
    
    # Display results
    if analysis:
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
        
        # Xuất ra Markdown
        export_to_markdown(analysis, output)
        
        click.echo(f"\n✅ Hoàn thành! Kết quả đã được lưu vào: {output}")
    else:
        click.echo("❌ Không thể tạo phân tích dự án.")


if __name__ == '__main__':
    analyze_project()
