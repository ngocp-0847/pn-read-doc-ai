#!/usr/bin/env python3
"""
Cấu hình cho EST CLI tool
"""

import os
from typing import Dict, Any


class ESTConfig:
    """Cấu hình cho EST CLI tool"""
    
    # OpenAI settings
    DEFAULT_MODEL = "gpt-4o-mini"
    MAX_TOKENS = 4000
    TEMPERATURE = 0.1
    
    # Task constraints
    MAX_TASK_HOURS = 14.0
    MIN_TASK_HOURS = 0.5
    
    # Complexity levels
    COMPLEXITY_LEVELS = ["Low", "Medium", "High"]
    COMPLEXITY_HOURS = {
        "Low": (0.5, 4.0),
        "Medium": (2.0, 8.0),
        "High": (6.0, 14.0)
    }
    
    # Priority levels
    PRIORITY_LEVELS = ["Low", "Medium", "High"]
    
    # Common skills
    COMMON_SKILLS = [
        "JavaScript/TypeScript",
        "React/Vue/Angular",
        "Node.js/Python/Java",
        "SQL Database",
        "RESTful API",
        "Git",
        "Docker",
        "Testing",
        "UI/UX Design",
        "DevOps",
        "Cloud Services",
        "Security"
    ]
    
    # Excel output settings
    EXCEL_SHEETS = {
        "summary": "Summary",
        "parent_tasks": "Parent Tasks", 
        "children_tasks": "Children Tasks",
        "assumptions_risks": "Assumptions & Risks"
    }
    
    # File extensions
    MARKDOWN_EXTENSIONS = [".md", ".markdown"]
    
    @classmethod
    def get_openai_config(cls) -> Dict[str, Any]:
        """Lấy cấu hình OpenAI"""
        return {
            "model": cls.DEFAULT_MODEL,
            "max_tokens": cls.MAX_TOKENS,
            "temperature": cls.TEMPERATURE
        }
    
    @classmethod
    def validate_task_hours(cls, hours: float) -> bool:
        """Kiểm tra thời gian task có hợp lệ không"""
        return cls.MIN_TASK_HOURS <= hours <= cls.MAX_TASK_HOURS
    
    @classmethod
    def get_complexity_hours(cls, complexity: str) -> tuple:
        """Lấy khoảng thời gian cho độ phức tạp"""
        return cls.COMPLEXITY_HOURS.get(complexity, (1.0, 4.0))
    
    @classmethod
    def get_environment_config(cls) -> Dict[str, str]:
        """Lấy cấu hình từ biến môi trường"""
        return {
            "openai_api_key": os.getenv("OPENAI_API_KEY", ""),
            "default_project_name": os.getenv("EST_DEFAULT_PROJECT", "Software Project"),
            "default_output": os.getenv("EST_DEFAULT_OUTPUT", "project_analysis.xlsx")
        }


# Cấu hình mặc định cho system prompt
SYSTEM_PROMPT_CONFIG = {
    "background": [
        "Bạn là một chuyên gia phân tích yêu cầu phần mềm và ước tính thời gian phát triển.",
        "Bạn có kinh nghiệm sâu rộng trong việc phân tích tài liệu kỹ thuật và ước tính effort cho các dự án phần mềm.",
        "Bạn hiểu rõ về quy trình phát triển phần mềm, các công nghệ phổ biến, và khả năng của một middle developer.",
        "Bạn có khả năng phân tích chi tiết và tạo ra các ước tính chính xác dựa trên độ phức tạp thực tế của từng task."
    ],
    "steps": [
        "Đọc và phân tích tất cả tài liệu markdown được cung cấp",
        "Xác định các tính năng chính và yêu cầu kỹ thuật",
        "Phân tích thành các parent task (tính năng lớn) và children task (tính năng nhỏ)",
        "Ước tính thời gian cho từng task dựa trên độ phức tạp và kinh nghiệm middle developer",
        "Đảm bảo mỗi task không quá 14 giờ và không ít hơn 0.5 giờ",
        "Xác định dependencies giữa các task",
        "Đánh giá độ ưu tiên và kỹ năng cần thiết",
        "Phân tích rủi ro và đưa ra các giả định"
    ],
    "output_instructions": [
        "Tạo cấu trúc task phân cấp rõ ràng với parent và children tasks",
        "Ước tính thời gian chính xác dựa trên độ phức tạp thực tế",
        "Đảm bảo tổng thời gian hợp lý cho dự án",
        "Cung cấp mô tả chi tiết cho mỗi task",
        "Xác định rõ dependencies và kỹ năng cần thiết",
        "Đánh giá độ ưu tiên dựa trên tầm quan trọng của task",
        "Đưa ra các giả định và rủi ro tiềm ẩn"
    ]
}


# Cấu hình cho Excel output
EXCEL_CONFIG = {
    "summary_columns": [
        "Project Name",
        "Total Estimated Hours", 
        "Total Parent Tasks",
        "Total Children Tasks",
        "Analysis Date"
    ],
    "parent_columns": [
        "Parent Task ID",
        "Parent Task Name", 
        "Description",
        "Total Hours",
        "Children Count"
    ],
    "children_columns": [
        "Parent Task ID",
        "Parent Task Name",
        "Task ID", 
        "Task Name",
        "Description",
        "Complexity",
        "Estimated Hours",
        "Dependencies",
        "Priority",
        "Skills Required"
    ],
    "assumptions_risks_columns": [
        "Type",
        "Description"
    ]
} 