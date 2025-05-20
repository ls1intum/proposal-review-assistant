"""
Simple proposal reviewer without LangGraph dependencies.
"""
import os
import re
import json
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import ChatOpenAI

# Import section-specific prompts
from prompts import (
    ABSTRACT_PROMPT, INTRODUCTION_PROMPT, PROBLEM_PROMPT, 
    MOTIVATION_PROMPT, OBJECTIVE_PROMPT, SCHEDULE_PROMPT, 
    BIBLIOGRAPHY_PROMPT, TRANSPARENCY_PROMPT, GENERAL_WRITING_PROMPT,
    DIAGRAMS_FIGURES_PROMPT
)

class FeedbackIssue(BaseModel):
    """A specific feedback issue in a proposal section."""
    section: str = Field(default=None, description="The section this feedback relates to")
    category: str = Field(description="Category of the issue (e.g., 'Clarity', 'Structure', 'Content', 'Grammar', 'Citations')")
    severity: str = Field(description="Severity of the issue: 'Minor', 'Moderate', or 'Major'")
    quote: Optional[str] = Field(default=None, description="A direct quote from the text illustrating the issue, if applicable")
    issue: str = Field(description="Description of the issue identified")
    suggestion: str = Field(description="Specific suggestion for addressing the issue")
    rule: Optional[str] = Field(default=None, description="The academic writing rule or guideline being applied, if relevant")

class FeedbackIssueList(BaseModel):
    """A list of feedback issues."""
    issues: List[FeedbackIssue] = Field(description="List of feedback issues identified in the section")

class SimpleProposal:
    """A simple class to handle proposal extraction."""
    
    def __init__(self, sections: Dict[str, str], full_text: str = ""):
        """Initialize with sections and full text."""
        self.sections = sections
        self.full_text = full_text
    
    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary."""
        result = self.sections.copy()
        result["full_text"] = self.full_text
        return result
    
    @classmethod
    def from_pdf(cls, pdf_path: str) -> 'SimpleProposal':
        """Extract sections from a PDF."""
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        # Load the PDF using PyPDFLoader
        loader = PyPDFLoader(pdf_path)
        pages = loader.load()
        
        # Extract the full text
        full_text = "\n".join(page.page_content for page in pages)
        
        # Extract sections using simple pattern matching
        sections = cls._extract_sections(full_text)
        
        return cls(sections, full_text)
    
    @staticmethod
    def _extract_sections(text: str) -> Dict[str, str]:
        """Extract sections from text using patterns."""
        # Define patterns for common section headings
        section_patterns = {
            "abstract": r"(?i)\b(?:abstract|summary)\b",
            "introduction": r"(?i)\b(?:1\.?\s*introduction|introduction)\b",
            "problem": r"(?i)\b(?:2\.?\s*problem|problem statement|research problem)\b",
            "motivation": r"(?i)\b(?:3\.?\s*motivation|motivation|relevance)\b",
            "objective": r"(?i)\b(?:4\.?\s*objective|research objective|goals|aims)\b",
            "schedule": r"(?i)\b(?:5\.?\s*schedule|timeline|work plan)\b",
            "bibliography": r"(?i)\b(?:6\.?\s*bibliography|references|works cited)\b",
            "transparency": r"(?i)\b(?:7\.?\s*transparency|ethics|ethical considerations)\b"
        }
        
        # Find the positions of each section heading
        positions = {}
        for section, pattern in section_patterns.items():
            matches = list(re.finditer(pattern, text))
            if matches:
                # Use the last match if multiple exist (in case the term appears in content)
                positions[section] = matches[-1].start()
        
        # Sort sections by position
        sorted_sections = sorted(positions.items(), key=lambda x: x[1])
        
        # Extract content between headings
        sections = {}
        for i, (section, pos) in enumerate(sorted_sections):
            # Start from the position of the heading
            start = pos
            # Find the end of the section heading
            heading_end = text.find("\n", start)
            if heading_end == -1:  # If no newline, use the whole string
                heading_end = len(text)
            
            # Skip the heading
            start = heading_end + 1
            
            # End at the next section or the end of the text
            if i < len(sorted_sections) - 1:
                end = sorted_sections[i + 1][1]
            else:
                end = len(text)
            
            # Extract the content
            sections[section] = text[start:end].strip()
        
        # Handle missing sections
        for section in section_patterns:
            if section not in sections:
                sections[section] = ""
        
        return sections

def get_section_feedback(section_name: str, section_content: str, full_text: str, model: ChatOpenAI) -> Dict[str, Any]:
    """
    Generate feedback for a specific section using structured output.
    
    Args:
        section_name: Name of the section
        section_content: Content of the section to focus on
        full_text: Full text of the entire proposal for context
        model: LLM model to use
        
    Returns:
        Dictionary with content and writing quality feedback
    """
    if not section_content.strip():
        return {
            "content_feedback": FeedbackIssueList(issues=[]),
            "writing_feedback": FeedbackIssueList(issues=[])
        }
    
    # Get the appropriate prompt for the section
    section_prompts = {
        "abstract": ABSTRACT_PROMPT,
        "introduction": INTRODUCTION_PROMPT,
        "problem": PROBLEM_PROMPT,
        "motivation": MOTIVATION_PROMPT,
        "objective": OBJECTIVE_PROMPT,
        "schedule": SCHEDULE_PROMPT,
        "bibliography": BIBLIOGRAPHY_PROMPT,
        "transparency": TRANSPARENCY_PROMPT,
        "writing_quality": GENERAL_WRITING_PROMPT,
        "diagrams_figures": DIAGRAMS_FIGURES_PROMPT
    }
    
    # Select proper prompt or use generic if not found
    prompt_content = section_prompts.get(
        section_name.lower(),
        f"Review the following {section_name} section and provide detailed feedback."
    )
    
    # Create a model that returns structured output
    structured_model = model.with_structured_output(FeedbackIssueList)
    
    # 1. Generate content feedback using the full proposal context
    system_prompt_content = """You are an academic writing assistant analyzing a thesis proposal section.
Please provide your feedback as structured issues focusing on CONTENT, STRUCTURE, and COHERENCE.
Consider how this section connects with the rest of the proposal.
Focus on identifying specific problems and providing actionable suggestions.
"""
    
    human_prompt_content = f"""
{prompt_content}

I want you to focus on the {section_name.upper()} section, but consider the context of the entire proposal when giving feedback.

Here is the FULL PROPOSAL for context:
{full_text}

Here is the specific {section_name.upper()} section to focus on:
{section_content}
"""
    
    # Generate content feedback with full context
    content_feedback = structured_model.invoke([
        {"role": "system", "content": system_prompt_content},
        {"role": "user", "content": human_prompt_content}
    ])
    
    # 2. Generate writing quality feedback (grammar, style, clarity) using only the section
    system_prompt_writing = """You are an academic writing assistant analyzing the writing quality of a thesis proposal section.
Please provide your feedback as structured issues focusing ONLY on WRITING STYLE, GRAMMAR, and CLARITY.
Do not analyze content or structure - focus exclusively on the writing mechanics.
"""
    
    human_prompt_writing = f"""
{GENERAL_WRITING_PROMPT}

Here is the {section_name.upper()} section to evaluate for writing quality:
{section_content}
"""
    
    # Generate writing quality feedback with section content only
    writing_feedback = structured_model.invoke([
        {"role": "system", "content": system_prompt_writing},
        {"role": "user", "content": human_prompt_writing}
    ])
    
    return {
        "content_feedback": content_feedback,
        "writing_feedback": writing_feedback
    }

def review_proposal(pdf_path: str, model_name: str = "o4-mini") -> Dict[str, Any]:
    """
    Review a proposal PDF and generate feedback.
    
    Args:
        pdf_path: Path to the proposal PDF file
        model_name: Name of the OpenAI model to use
        
    Returns:
        Dictionary with section feedbacks
    """
    # Initialize the model
    model = ChatOpenAI(model=model_name)
    
    # Load the proposal
    proposal = SimpleProposal.from_pdf(pdf_path)
    proposal_dict = proposal.to_dict()
    full_text = proposal_dict.get("full_text", "")
    
    # Define the sections to review
    section_order = ["abstract", "introduction", "problem", "motivation", 
                     "objective", "schedule", "bibliography", "transparency"]
    
    # Generate feedback for each section
    section_feedbacks = {}
    for section in section_order:
        section_content = proposal_dict.get(section, "")
        if section_content:
            print(f"Generating feedback for {section} section...")
            feedback = get_section_feedback(section, section_content, full_text, model)
            section_feedbacks[section] = feedback
    
    # Don't generate summary as requested
    empty_summary = "No summary generated as requested."
    
    return {
        "section_feedbacks": section_feedbacks,
        "summary": empty_summary
    } 