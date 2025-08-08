#!/usr/bin/env python3
"""
EST TRY 2 CLI - Index with fast-graphrag and generate detailed project estimation

This CLI:
- Reads markdown files from a folder
- Indexes all content into a fast-graphrag working directory
- Generates a hierarchical task breakdown (categories -> parent -> child tasks)
- Ensures each child task estimate is <= 20 hours (splits if needed)
- Aggregates effort for BE, FE, QA, and Infra
- Exports a customer-ready Markdown estimate

Reference: fast-graphrag usage and quickstart documented at
https://github.com/circlemind-ai/fast-graphrag
"""

import os
import glob
import json
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

import click
from pydantic import BaseModel, Field

from dotenv import load_dotenv

# Load environment variables early
load_dotenv()


# -------------------------------
# Models
# -------------------------------

ALLOWED_DISCIPLINES = ["BE", "FE", "QA", "Infra"]
ALLOWED_COMPLEXITY = ["Low", "Medium", "High"]
ALLOWED_PRIORITY = ["Low", "Medium", "High", "Critical"]


class ChildTask(BaseModel):
    task_id: str = Field(..., description="Unique child task id")
    task_name: str = Field(..., description="Task name")
    description: str = Field(..., description="Detailed description")
    discipline: str = Field(..., description=f"One of {ALLOWED_DISCIPLINES}")
    complexity: str = Field(..., description=f"One of {ALLOWED_COMPLEXITY}")
    priority: str = Field(..., description=f"One of {ALLOWED_PRIORITY}")
    estimated_hours: float = Field(..., description="Estimated effort in hours (<= 20h)")
    dependencies: List[str] = Field(default_factory=list, description="Dependent task ids")
    skills_required: List[str] = Field(default_factory=list, description="Required skills")


class ParentTask(BaseModel):
    parent_id: str
    category: str = Field(..., description="High-level category (e.g., Backend, Frontend, QA, Infra)")
    parent_name: str
    description: str = ""
    children_tasks: List[ChildTask] = Field(default_factory=list)

    @property
    def total_estimated_hours(self) -> float:
        return sum(t.estimated_hours for t in self.children_tasks)


class Estimate(BaseModel):
    project_name: str
    summary: str
    assumptions: List[str] = Field(default_factory=list)
    risks: List[str] = Field(default_factory=list)
    parent_tasks: List[ParentTask] = Field(default_factory=list)

    @property
    def total_estimated_hours(self) -> float:
        return sum(p.total_estimated_hours for p in self.parent_tasks)

    def hours_by_discipline(self) -> Dict[str, float]:
        agg: Dict[str, float] = {k: 0.0 for k in ALLOWED_DISCIPLINES}
        for p in self.parent_tasks:
            for t in p.children_tasks:
                if t.discipline in agg:
                    agg[t.discipline] += float(t.estimated_hours)
        return agg


# -------------------------------
# Utilities
# -------------------------------


def read_markdown_folder(folder: str, exts: Optional[List[str]] = None) -> List[Tuple[str, str]]:
    if exts is None:
        exts = [".md", ".markdown", ".mdx"]
    docs: List[Tuple[str, str]] = []
    for ext in exts:
        for file_path in glob.glob(os.path.join(folder, f"*{ext}")):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    docs.append((os.path.basename(file_path), f.read()))
            except Exception as e:
                click.echo(f"⚠️  Lỗi khi đọc file {file_path}: {e}")
    return docs


def enforce_child_task_hour_limit(children: List[ChildTask], max_hours: float = 20.0) -> List[ChildTask]:
    """Ensure each child task has estimated_hours <= max_hours by splitting if necessary."""
    adjusted: List[ChildTask] = []
    for task in children:
        if task.estimated_hours <= max_hours:
            adjusted.append(task)
            continue
        # Split into n parts of <= max_hours
        remaining = float(task.estimated_hours)
        part_index = 1
        while remaining > 0:
            part_hours = min(max_hours, remaining)
            adjusted.append(
                ChildTask(
                    task_id=f"{task.task_id}-p{part_index}",
                    task_name=f"{task.task_name} - Part {part_index}",
                    description=task.description,
                    discipline=task.discipline,
                    complexity=task.complexity,
                    priority=task.priority,
                    estimated_hours=part_hours,
                    dependencies=task.dependencies,
                    skills_required=task.skills_required,
                )
            )
            remaining -= part_hours
            part_index += 1
    return adjusted


def export_estimate_to_markdown(estimate: Estimate, output_path: str) -> str:
    lines: List[str] = []
    lines.append(f"# Project Estimate: {estimate.project_name}")
    lines.append("")
    lines.append(f"- Total estimated hours: **{estimate.total_estimated_hours:.1f}h**")
    by_role = estimate.hours_by_discipline()
    lines.append(
        "- Hours by discipline: "
        + ", ".join([f"{k}: {v:.1f}h" for k, v in by_role.items() if v > 0])
    )
    lines.append("")
    if estimate.summary:
        lines.append("## Summary")
        lines.append(estimate.summary)
        lines.append("")
    if estimate.assumptions:
        lines.append("## Assumptions")
        lines.extend([f"- {a}" for a in estimate.assumptions])
        lines.append("")
    if estimate.risks:
        lines.append("## Risks")
        lines.extend([f"- {r}" for r in estimate.risks])
        lines.append("")

    lines.append("## Work Breakdown")
    # Group parent tasks by category
    category_to_parents: Dict[str, List[ParentTask]] = {}
    for p in estimate.parent_tasks:
        category_to_parents.setdefault(p.category, []).append(p)

    for category, parents in category_to_parents.items():
        lines.append(f"### {category}")
        for idx, parent in enumerate(parents, 1):
            lines.append(f"#### {idx}. {parent.parent_name} ({parent.total_estimated_hours:.1f}h)")
            if parent.description:
                lines.append(parent.description)
            if parent.children_tasks:
                lines.append("")
                lines.append(
                    "| Task ID | Name | Discipline | Complexity | Priority | Est. Hours | Dependencies | Skills | Description |"
                )
                lines.append("|---|---|---|---|---|---:|---|---|---|")
                for t in parent.children_tasks:
                    deps = ", ".join(t.dependencies) if t.dependencies else "-"
                    skills = ", ".join(t.skills_required) if t.skills_required else "-"
                    lines.append(
                        f"| {t.task_id} | {t.task_name} | {t.discipline} | {t.complexity} | {t.priority} | {t.estimated_hours:.1f} | {deps} | {skills} | {t.description} |"
                    )
            lines.append("")

    out = Path(output_path)
    if out.suffix.lower() != ".md":
        out = out.with_suffix(".md")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")
    return str(out)


# -------------------------------
# Estimation logic using fast-graphrag + OpenAI
# -------------------------------


def build_graphrag(working_dir: str, domain_prompt: str, example_queries: List[str], entity_types: List[str]):
    try:
        from fast_graphrag import GraphRAG
    except Exception as e:
        raise RuntimeError(
            "fast-graphrag is not installed. Please 'pip install fast-graphrag'"
        ) from e

    grag = GraphRAG(
        working_dir=working_dir,
        domain=domain_prompt,
        example_queries="\n".join(example_queries),
        entity_types=entity_types,
    )
    return grag


def grag_insert_all_text(grag, documents: List[Tuple[str, str]]):
    if not documents:
        return 0
    # Concatenate with headers to preserve file boundaries
    combined: List[str] = []
    for name, content in documents:
        combined.append(f"\n\n# FILE: {name}\n\n{content}\n")
    text = "\n".join(combined)
    grag.insert(text)
    return len(documents)


def get_context_from_grag(grag, project_name: str) -> str:
    """Ask GraphRAG to surface an actionable context for estimation."""
    query = (
        "You are assisting in creating a project estimate. "
        f"Project: {project_name}. "
        "Extract the key features, components, user flows, APIs, data entities, and infrastructure aspects. "
        "Return a concise, well-structured summary that will be used to create a detailed work breakdown."
    )
    try:
        result = grag.query(query)
        # result.chunks , merge content lại, cấu trúc chunks=[(TChunk(id=np.int64(8840167882252271784), content='.\n\n### Yêu cầu dữ liệu\n- Lưu đầy đủ lịch
        chunks = [chunk[0].content for chunk in result.context.chunks]
        print("result: ", chunks)
        # GraphRAG returns an object with .response
        return "\n".join(chunks)
    except Exception as e:
        print("error: ", e)
        return ""


def generate_estimate_with_llm(openai_api_key: str, project_name: str, context: str) -> Estimate:
    """Use OpenAI to produce a structured estimate given a context string."""
    from openai import OpenAI
    client = OpenAI(api_key=openai_api_key)

    system = (
        "You are a senior software delivery manager. Create a detailed work breakdown and estimates. "
        "Requirements: Break into categories (Backend, Frontend, QA, Infra). Each category has parent features, "
        "and each parent has multiple child tasks. Each child task must be <= 20 hours. Assign each child task a discipline "
        "(BE|FE|QA|Infra), a complexity (Low|Medium|High), a priority (Low|Medium|High|Critical), and estimated_hours. "
        "Be exhaustive and granular. Include assumptions and risks."
    )
    user = (
        f"Project: {project_name}\n\nContext for estimation (from GraphRAG):\n{context}\n\n"
        "Return strict JSON with keys: project_name, summary, assumptions, risks, parent_tasks. "
        "parent_tasks: array of {parent_id, category, parent_name, description, children_tasks}. "
        "children_tasks: array of {task_id, task_name, description, discipline, complexity, priority, estimated_hours, dependencies, skills_required}. "
        "Categories must be one of: Backend, Frontend, QA, Infra. Discipline must be one of: BE, FE, QA, Infra."
    )

    completion = client.chat.completions.create(
        model=os.getenv("EST_MODEL", "gpt-4o-mini"),
        temperature=0.2,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        response_format={"type": "json_object"},
    )
    raw = completion.choices[0].message.content or "{}"
    data = json.loads(raw)

    # Map JSON to Pydantic models with safety and hour limit enforcement
    parent_tasks: List[ParentTask] = []
    for p in data.get("parent_tasks", []) or []:
        children: List[ChildTask] = []
        for c in p.get("children_tasks", []) or []:
            # Sanitize discipline
            disc = c.get("discipline", "").strip()
            if disc not in ALLOWED_DISCIPLINES:
                disc = "BE" if p.get("category", "").lower() == "backend" else (
                    "FE" if p.get("category", "").lower() == "frontend" else (
                        "QA" if p.get("category", "").lower() == "qa" else "Infra"
                    )
                )
            child = ChildTask(
                task_id=str(c.get("task_id")),
                task_name=str(c.get("task_name")),
                description=str(c.get("description", "")),
                discipline=disc,
                complexity=c.get("complexity", "Medium"),
                priority=c.get("priority", "Medium"),
                estimated_hours=float(c.get("estimated_hours", 2.0)),
                dependencies=[str(x) for x in (c.get("dependencies") or [])],
                skills_required=[str(x) for x in (c.get("skills_required") or [])],
            )
            children.append(child)
        children = enforce_child_task_hour_limit(children, max_hours=20.0)
        parent_tasks.append(
            ParentTask(
                parent_id=str(p.get("parent_id")),
                category=str(p.get("category", "Backend")),
                parent_name=str(p.get("parent_name")),
                description=str(p.get("description", "")),
                children_tasks=children,
            )
        )

    estimate = Estimate(
        project_name=str(data.get("project_name", project_name)),
        summary=str(data.get("summary", "")),
        assumptions=[str(x) for x in (data.get("assumptions") or [])],
        risks=[str(x) for x in (data.get("risks") or [])],
        parent_tasks=parent_tasks,
    )
    return estimate


# -------------------------------
# CLI
# -------------------------------


@click.command()
@click.option("--folder", "folder", required=True, help="Folder chứa tài liệu markdown để index")
@click.option("--project-name", "project_name", default="Software Project", help="Tên dự án")
@click.option("--working-dir", "working_dir", default="./grag_workdir", help="Thư mục làm việc cho fast-graphrag")
@click.option("--output", "output", default="project_estimate.md", help="Đường dẫn file Markdown output")
@click.option("--openai-key", "openai_key", envvar="OPENAI_API_KEY", help="OpenAI API Key")
@click.option("--entity-types", "entity_types_opt", default="Character,Place,Object,Activity,Event", help="Danh sách entity types, phân tách bởi dấu phẩy")
@click.option("--query-only", "query_only", is_flag=True, help="Chỉ truy vấn trên dữ liệu đã index trước đó (không index lại)")
def run(folder: str, project_name: str, working_dir: str, output: str, openai_key: Optional[str], entity_types_opt: str, query_only: bool):
    """Index tài liệu với fast-graphrag và sinh ước tính chi tiết (BE/FE/QA/Infra)."""
    if not openai_key:
        click.echo("❌ Thiếu OpenAI API Key. Truyền --openai-key hoặc thiết lập OPENAI_API_KEY trong môi trường.")
        raise SystemExit(1)

    if not os.path.isdir(folder):
        click.echo(f"❌ Folder không tồn tại: {folder}")
        raise SystemExit(1)

    docs = read_markdown_folder(folder)
    if not docs:
        click.echo("❌ Không tìm thấy file markdown trong folder đã chỉ định.")
        raise SystemExit(1)

    click.echo(f"📁 Đã đọc {len(docs)} tài liệu từ '{folder}'")

    # Configure GraphRAG
    entity_types = [x.strip() for x in entity_types_opt.split(",") if x.strip()]
    domain_prompt = (
        "Analyze project requirements, identify components, APIs, data entities, UI flows, and infra needs. "
        "Focus on producing estimation-ready knowledge."
    )
    example_queries = [
        "List all main features and their sub-features",
        "Identify backend services, APIs, and data models",
        "Identify frontend pages, components, and states",
        "Identify QA scope and testing types",
        "Identify infrastructure and deployment needs",
    ]

    click.echo("🔧 Khởi tạo fast-graphrag...")
    grag = build_graphrag(working_dir=working_dir, domain_prompt=domain_prompt, example_queries=example_queries, entity_types=entity_types)

    # Index all text
    if not query_only:
        click.echo("📚 Đang index tất cả nội dung vào fast-graphrag...")
        count = grag_insert_all_text(grag, docs)
        click.echo(f"✅ Đã index {count} tài liệu vào '{working_dir}'")
    else:
        click.echo("🔎 Chỉ truy vấn trên dữ liệu đã index trước đó (không index lại)")

    # Build estimation context
    click.echo("🔍 Truy vấn GraphRAG để lấy ngữ cảnh ước tính...")
    context = get_context_from_grag(grag, project_name)

    # Generate estimate via OpenAI
    click.echo("🤖 Sinh ước tính chi tiết (BE/FE/QA/Infra)...")
    estimate = generate_estimate_with_llm(openai_key, project_name, context)

    # Export markdown
    click.echo("📝 Xuất Markdown đề xuất cho khách hàng...")
    output_file = export_estimate_to_markdown(estimate, output)
    click.echo(f"✅ Hoàn tất! File: {output_file}")


if __name__ == "__main__":
    run()


