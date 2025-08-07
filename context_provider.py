#!/usr/bin/env python3
"""
Context Provider cho EST CLI sử dụng dsRAG với Qdrant
"""

import os
import json
import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime
from pathlib import Path

from dsrag.knowledge_base import KnowledgeBase
from dsrag.database.vector import BasicVectorDB
from dsrag.database.chunk import BasicChunkDB
from dsrag.embedding import OpenAIEmbedding
from dsrag.reranker import CohereReranker
from dsrag.llm import OpenAIChatAPI
from dsrag.dsparse.file_parsing.file_system import LocalFileSystem
from atomic_agents.context import BaseDynamicContextProvider

from config.estimate import ESTConfig


class ProjectEstimateContextProvider(BaseDynamicContextProvider):
    """Context provider cho project estimation sử dụng dsRAG với Qdrant"""
    
    def __init__(self, 
                 openai_api_key: str,
                 storage_directory: str = "./dsrag_storage",
                 collection_name: str = "project_estimates"):
        super().__init__(title="Project Estimation Context")
        self.openai_api_key = openai_api_key
        self.storage_directory = storage_directory
        self.collection_name = collection_name
        
        # Initialize dsRAG KnowledgeBase
        self.knowledge_base = self._init_knowledge_base()
        
        # Load estimation guidelines
        self._load_estimation_guidelines()
    
    def _init_knowledge_base(self) -> KnowledgeBase:
        """Khởi tạo dsRAG KnowledgeBase với các components mặc định"""
        # Create storage directory
        os.makedirs(self.storage_directory, exist_ok=True)
        
        # Initialize components
        embedding = OpenAIEmbedding(
            api_key=self.openai_api_key,
            model="text-embedding-3-small"
        )
        
        reranker = CohereReranker()  # Sử dụng CohereReranker thay vì NoReranker
        
        llm = OpenAIChatAPI(
            api_key=self.openai_api_key,
            model="gpt-4o-mini"
        )
        
        # Create KnowledgeBase với API mới
        knowledge_base = KnowledgeBase(
            kb_id=self.collection_name,
            title="Project Estimation Knowledge Base",
            description="Knowledge base for software project estimation",
            storage_directory=self.storage_directory,
            embedding_model=embedding,
            reranker=reranker,
            auto_context_model=llm,
            exists_ok=True
        )
        
        return knowledge_base
    
    def _load_estimation_guidelines(self):
        """Load estimation guidelines vào knowledge base"""
        guidelines_content = """
# Software Development Estimation Guidelines

## 1. COMPLEXITY LEVELS

### Low Complexity (0.5-4 hours)
- Simple UI changes and updates
- Basic CRUD operations
- Simple integrations with existing APIs
- Minor bug fixes
- Documentation updates
- Simple configuration changes

### Medium Complexity (2-8 hours)
- Complex UI components
- API development and integration
- Database design and optimization
- Authentication and authorization
- Form validation and processing
- Data transformation and processing
- Unit testing implementation

### High Complexity (6-14 hours)
- Complex algorithms and business logic
- Third-party integrations
- Security features and encryption
- Performance optimization
- Advanced UI/UX features
- Complex data modeling
- Integration testing
- System architecture design

## 2. TASK BREAKDOWN PRINCIPLES

### General Rules
- Each task should be completable by one developer in 1-2 days maximum
- Break large features into smaller, manageable tasks
- Consider dependencies between tasks
- Account for testing and documentation time
- Include time for code review and feedback

### Task Sizing Guidelines
- Small tasks: 0.5-2 hours
- Medium tasks: 2-6 hours
- Large tasks: 6-14 hours
- Avoid tasks larger than 14 hours

## 3. COMMON ESTIMATION PATTERNS

### Authentication & Security
- User registration: 4-6 hours
- Login/logout: 2-4 hours
- Password reset: 3-5 hours
- 2FA implementation: 6-10 hours
- Role-based access control: 8-12 hours
- OAuth integration: 6-12 hours

### Database & Backend
- Database design: 6-12 hours
- CRUD operations per entity: 4-8 hours
- API endpoints per resource: 2-6 hours
- Data validation: 2-4 hours
- Error handling: 2-4 hours
- Logging implementation: 2-4 hours

### Frontend Development
- UI components: 2-8 hours depending on complexity
- Form implementation: 3-6 hours
- Data visualization: 4-10 hours
- Responsive design: 2-6 hours
- State management: 4-8 hours
- API integration: 2-6 hours

### Testing & Quality Assurance
- Unit testing: 20-30% of development time
- Integration testing: 15-25% of development time
- UI testing: 10-20% of development time
- Performance testing: 4-8 hours
- Security testing: 4-8 hours

### Documentation & Deployment
- Technical documentation: 10-15% of development time
- User documentation: 5-10% of development time
- Deployment setup: 4-8 hours
- CI/CD pipeline: 8-16 hours
- Environment configuration: 2-4 hours

## 4. FACTORS TO CONSIDER

### Team Experience
- Junior developer: Add 20-30% to estimates
- Senior developer: Standard estimates apply
- Expert developer: Reduce estimates by 10-20%

### Technology Stack
- Familiar technologies: Standard estimates
- New technologies: Add 30-50% to estimates
- Legacy system integration: Add 20-40% to estimates

### Project Complexity
- Simple projects: Standard estimates
- Complex business logic: Add 25-40% to estimates
- High-performance requirements: Add 20-30% to estimates
- Security requirements: Add 15-25% to estimates

### External Dependencies
- Third-party APIs: Add 4-8 hours per integration
- External services: Add 6-12 hours per service
- Payment gateways: Add 8-16 hours per gateway
- Social media integration: Add 4-8 hours per platform

## 5. RISK FACTORS

### Technical Risks
- New technologies or frameworks: +30-50%
- Complex algorithms: +25-40%
- Performance requirements: +20-30%
- Security requirements: +15-25%
- Scalability needs: +20-35%

### Business Risks
- Unclear requirements: +25-40%
- Changing requirements: +20-30%
- Integration with legacy systems: +20-40%
- Compliance requirements: +15-25%

### Team Risks
- New team members: +20-30%
- Remote team coordination: +10-20%
- Multiple time zones: +15-25%

## 6. ESTIMATION TECHNIQUES

### Top-Down Estimation
- Start with overall project scope
- Break down into major components
- Estimate each component
- Add buffer for unknowns

### Bottom-Up Estimation
- Identify all individual tasks
- Estimate each task separately
- Sum up all estimates
- Add integration and testing time

### Comparative Estimation
- Compare with similar past projects
- Adjust for differences in scope
- Consider team experience changes
- Factor in technology changes

## 7. BUFFER AND CONTINGENCY

### Recommended Buffers
- Small projects (< 100 hours): 15-20%
- Medium projects (100-500 hours): 20-25%
- Large projects (> 500 hours): 25-30%

### Contingency Planning
- Technical risks: 10-15%
- Business risks: 10-20%
- Team risks: 5-10%
- External dependencies: 10-15%
        """
        
        # Add guidelines to knowledge base
        self.knowledge_base.add_document(
            content=guidelines_content,
            title="Software Development Estimation Guidelines",
            doc_id="estimation_guidelines"
        )
    
    def add_markdown_documents(self, documents: List[str], project_name: str):
        """Thêm markdown documents vào knowledge base"""
        for i, doc_content in enumerate(documents):
            doc_id = f"{project_name}_doc_{i}"
            title = f"Project Document {i+1} - {project_name}"
            
            self.knowledge_base.add_document(
                doc_id=doc_id,
                text=doc_content,
                document_title=title,
                metadata={
                    'project_name': project_name,
                    'document_type': 'markdown',
                    'index': i
                }
            )
    
    def get_context_for_project(self, project_description: str, documents: List[str] = None) -> str:
        """Get context for project estimation using RAG"""
        # Add project documents if provided
        if documents:
            self.add_markdown_documents(documents, "current_project")
        
        # Query the knowledge base for relevant information
        query = f"""
        Based on the project description: "{project_description}"
        
        Please provide:
        1. Relevant estimation guidelines and patterns
        2. Similar project examples and their task breakdowns
        3. Complexity assessment guidelines
        4. Risk factors to consider
        5. Recommended task breakdown approach
        
        Focus on providing practical, actionable estimation guidance.
        """
        
        # Perform RAG query
        try:
            results = self.knowledge_base.query(
                search_queries=[query],
                rse_params={
                    "max_length": 10,
                    "overall_max_length": 20,
                    "minimum_value": 0.7,
                    "irrelevant_chunk_penalty": 0.3
                }
            )
            
            # Extract relevant context from results
            context = "ESTIMATION CONTEXT FROM RAG:\n\n"
            
            for i, result in enumerate(results, 1):
                context += f"RELEVANT INFORMATION {i}:\n"
                context += f"Source: {result.get('title', 'Unknown')}\n"
                context += f"Relevance: {result.get('relevance', 0):.3f}\n"
                context += f"Content: {result.get('content', '')}\n"
                context += "-" * 50 + "\n\n"
            
            return context
            
        except Exception as e:
            # Fallback to general guidelines
            return self.get_info()
    
    def get_info(self) -> str:
        """Get general context information"""
        return """
ESTIMATION CONTEXT - Guidelines for Project Estimation:

1. COMPLEXITY LEVELS:
   - Low: 0.5-4 hours (Simple UI changes, basic CRUD, simple integrations)
   - Medium: 2-8 hours (Complex UI components, API development, database design)
   - High: 6-14 hours (Complex algorithms, third-party integrations, security features)

2. TASK BREAKDOWN PRINCIPLES:
   - Each task should be completable by one developer in 1-2 days max
   - Break large features into smaller, manageable tasks
   - Consider dependencies between tasks
   - Account for testing and documentation time

3. COMMON ESTIMATION PATTERNS:
   - Authentication system: 8-12 hours
   - CRUD operations: 4-8 hours per entity
   - API endpoints: 2-6 hours per endpoint
   - Database design: 6-12 hours
   - UI components: 2-8 hours depending on complexity
   - Testing: 20-30% of development time
   - Documentation: 10-15% of development time

4. FACTORS TO CONSIDER:
   - Team experience level
   - Technology stack familiarity
   - Integration complexity
   - Security requirements
   - Performance requirements
   - Third-party dependencies

5. RISK FACTORS:
   - New technologies or frameworks
   - Complex business logic
   - Integration with legacy systems
   - Performance requirements
   - Security requirements
   - Scalability needs
        """


class EstimationContextManager:
    """Manager cho estimation context sử dụng dsRAG"""
    
    def __init__(self, openai_api_key: str):
        self.context_provider = ProjectEstimateContextProvider(openai_api_key)
    
    def get_context_for_documents(self, documents: List[str], project_name: str) -> str:
        """Get context for estimation based on documents using RAG"""
        # Combine all documents into a single description
        combined_text = "\n".join(documents)
        
        # Create project description
        project_description = f"Project: {project_name}\n\n{combined_text[:1000]}..."  # Limit to first 1000 chars
        
        # Get context from provider using RAG
        return self.context_provider.get_context_for_project(project_description, documents)
    
    def add_custom_estimate(self, project_data: Dict[str, Any]):
        """Add custom project estimate to the knowledge base"""
        # Convert project data to document format
        doc_content = f"""
Project: {project_data['project_name']}
Description: {project_data['description']}
Total Hours: {project_data['total_hours']}
Technologies: {', '.join(project_data['technologies'])}
Team Size: {project_data['team_size']}
Duration: {project_data['duration_weeks']} weeks

Parent Tasks:
{chr(10).join(f"- {task['name']}: {task['description']} ({task['hours']}h, {task['complexity']})" for task in project_data['parent_tasks'])}
        """.strip()
        
        self.context_provider.knowledge_base.add_document(
            content=doc_content,
            title=f"Project Estimate - {project_data['project_name']}",
            doc_id=f"estimate_{project_data['project_name'].lower().replace(' ', '_')}"
        ) 