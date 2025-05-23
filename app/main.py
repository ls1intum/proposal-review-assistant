from typing import Optional, List
from pydantic import BaseModel, Field
import logging
import sys
import json
import gradio as gr
from langfuse.callback import CallbackHandler
from langchain_core.runnables import RunnableParallel

from app.prompts.abstract import get_abstract_prompt
from app.prompts.introduction import get_introduction_prompt
from app.prompts.problem import get_problem_prompt
from app.prompts.motivation import get_motivation_prompt
from app.prompts.objectives import get_objectives_prompt
from app.prompts.bibliography import get_bibliography_prompt
from app.prompts.schedule import get_schedule_prompt
from app.prompts.transparency import get_transparency_prompt
from app.prompts.general_writing import get_general_writing_prompt
from app.prompts.figures_diagrams import get_figures_diagrams_prompt

from app.models import get_model
from app.pdf_converter import convert_pdf_to_clean_markdown
from app.settings import settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s]: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

callbacks = []
if settings.langfuse_enabled:
    langfuse_handler = CallbackHandler()
    langfuse_handler.auth_check()
    callbacks.append(langfuse_handler)


class FeedbackIssue(BaseModel):
    """A specific feedback issue in a proposal section."""
    section: str = Field(default=None, description="The section this feedback relates to")
    category: str = Field(description="Category of the issue (e.g., 'Clarity', 'Structure', 'Content', 'Grammar', 'Citations')")
    priority: str = Field(description="Priority of the issue: 'Very Low', 'Low', 'Medium', 'High', 'Very High'")
    quote: Optional[str] = Field(default=None, description="A direct quote from the text illustrating the issue, if applicable")
    issue: str = Field(description="Description of the issue identified")
    suggestion: str = Field(description="Specific suggestion for addressing the issue")
    rule: Optional[str] = Field(default=None, description="The academic writing rule or guideline being applied, if relevant")

class FeedbackIssueList(BaseModel):
    """A list of feedback issues."""
    issues: List[FeedbackIssue] = Field(description="List of feedback issues identified in the section")


ChatModel = get_model(settings.MODEL_NAME)
issue_model = ChatModel().with_structured_output(FeedbackIssueList)


def format_feedback_for_display(issues):
    """Format the feedback issues for nice display in Gradio."""
    if not issues:
        return "No issues found in the proposal. Great work!"

    # Group issues by section and priority
    sections = {}
    for issue in issues:
        section = issue.get('section', 'General')
        if section not in sections:
            sections[section] = {'Very High': [], 'High': [], 'Medium': [], 'Low': [], 'Very Low': []}
        priority = issue.get('priority', 'Medium')
        sections[section][priority].append(issue)
    
    # Create formatted markdown output
    markdown_output = "# 📝 Proposal Feedback Report\n\n"
    
    priority_order = ['Very High', 'High', 'Medium', 'Low', 'Very Low']
    priority_emojis = {'Very High': '🔴', 'High': '🟠', 'Medium': '🟡', 'Low': '🔵', 'Very Low': '⚪'}
    
    for section, section_issues in sections.items():
        has_issues = any(section_issues[p] for p in priority_order)
        if not has_issues:
            continue
            
        markdown_output += f"## 📂 {section}\n\n"
        
        for priority in priority_order:
            if section_issues[priority]:
                markdown_output += f"### {priority_emojis[priority]} {priority} Priority\n\n"
                
                for i, issue in enumerate(section_issues[priority], 1):
                    markdown_output += f"**{i}. {issue['category']}**\n\n"
                    
                    if issue.get('quote'):
                        markdown_output += f"> *\"{issue['quote']}\"*\n\n"
                    
                    markdown_output += f"**📋 Issue:** {issue['issue']}\n\n"
                    markdown_output += f"**💡 Suggestion:** {issue['suggestion']}\n\n"
                    
                    if issue.get('rule'):
                        markdown_output += f"**📖 Rule:** {issue['rule']}\n\n"
                    
                    markdown_output += "---\n\n"
    
    return markdown_output


def format_feedback_for_text(issues):
    """Format the feedback issues for human-readable text download."""
    if not issues:
        return "PROPOSAL FEEDBACK REPORT\n" + "="*50 + "\n\nNo issues found in the proposal. Great work!"

    # Group issues by section and priority
    sections = {}
    for issue in issues:
        section = issue.get('section', 'General')
        if section not in sections:
            sections[section] = {'Very High': [], 'High': [], 'Medium': [], 'Low': [], 'Very Low': []}
        priority = issue.get('priority', 'Medium')
        sections[section][priority].append(issue)
    
    # Create formatted text output
    text_output = "PROPOSAL FEEDBACK REPORT\n"
    text_output += "="*50 + "\n\n"
    
    priority_order = ['Very High', 'High', 'Medium', 'Low', 'Very Low']
    priority_symbols = {'Very High': '!!!', 'High': '!!', 'Medium': '!', 'Low': '-', 'Very Low': '.'}
    
    total_issues = sum(len(issues) for section_issues in sections.values() for issues in section_issues.values())
    text_output += f"Total Issues Found: {total_issues}\n\n"
    
    for section, section_issues in sections.items():
        has_issues = any(section_issues[p] for p in priority_order)
        if not has_issues:
            continue
            
        text_output += f"SECTION: {section.upper()}\n"
        text_output += "-" * (len(section) + 9) + "\n\n"
        
        for priority in priority_order:
            if section_issues[priority]:
                text_output += f"{priority_symbols[priority]} {priority.upper()} PRIORITY\n\n"
                
                for i, issue in enumerate(section_issues[priority], 1):
                    text_output += f"{i}. {issue['category'].upper()}\n"
                    text_output += "   " + "="*len(issue['category']) + "\n\n"
                    
                    if issue.get('quote'):
                        text_output += "   QUOTE:\n"
                        text_output += f'   "{issue["quote"]}"\n\n'
                    
                    text_output += "   ISSUE:\n"
                    text_output += f"   {issue['issue']}\n\n"
                    
                    text_output += "   SUGGESTION:\n"
                    text_output += f"   {issue['suggestion']}\n\n"
                    
                    if issue.get('rule'):
                        text_output += "   WRITING RULE:\n"
                        text_output += f"   {issue['rule']}\n\n"
                    
                    text_output += "   " + "-"*60 + "\n\n"
                
                text_output += "\n"
        
        text_output += "\n"
    
    return text_output


def upload_file(file):
    proposal = convert_pdf_to_clean_markdown(file.name)
    print(f"Converted proposal: {proposal}")
    chain = RunnableParallel({
        "general_writing": get_general_writing_prompt() | issue_model,
        "figures_diagrams": get_figures_diagrams_prompt() | issue_model,
        "abstract": get_abstract_prompt() | issue_model,
        "introduction": get_introduction_prompt() | issue_model,
        "problem": get_problem_prompt() | issue_model,
        "motivation": get_motivation_prompt() | issue_model,
        "objectives": get_objectives_prompt() | issue_model,
        "bibliography": get_bibliography_prompt() | issue_model,
        "schedule": get_schedule_prompt() | issue_model,
        "transparency": get_transparency_prompt() | issue_model,
    }).with_config(callbacks=callbacks)
    result = chain.invoke({ "proposal": proposal })

    issues = []
    for feedback_list in result.values():
        for feedback in feedback_list.issues:
            issues.append(feedback.model_dump())
    
    # Format for display and downloads
    formatted_output = format_feedback_for_display(issues)
    json_content = json.dumps(issues, indent=2)
    text_content = format_feedback_for_text(issues)
    
    return formatted_output, json_content, text_content

with gr.Blocks(title="Proposal Assistance Tool", theme=gr.themes.Soft()) as playground:
    gr.Markdown("# 🎓 Proposal Assistance Tool")
    gr.Markdown("Upload your research proposal PDF to get detailed feedback and suggestions for improvement.")
    
    with gr.Row():
        with gr.Column(scale=1):
            upload_button = gr.UploadButton(
                "📄 Click to Upload a Proposal", 
                file_types=[".pdf"],
                size="lg"
            )
        
    with gr.Row():
        with gr.Column():
            feedback_output = gr.Markdown(
                label="Feedback Report",
                value="Upload a proposal to see feedback here...",
                show_copy_button=True
            )
    
    with gr.Row():
        with gr.Column(scale=1):
            download_json_button = gr.DownloadButton(
                "💾 Download JSON Report",
                visible=False,
                size="sm",
                variant="secondary"
            )
        with gr.Column(scale=1):
            download_text_button = gr.DownloadButton(
                "📄 Download Text Report",
                visible=False,
                size="sm",
                variant="secondary"
            )
    
    def process_upload(file):
        if file is None:
            return (
                "Please upload a file first.", 
                None, None,
                gr.update(visible=False), 
                gr.update(visible=False)
            )
        
        try:
            formatted_feedback, json_content, text_content = upload_file(file)
            
            # Save files to temporary locations for download
            import tempfile
            import os
            
            # Create JSON file
            json_temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
            json_temp_file.write(json_content)
            json_temp_file.close()
            
            # Create text file
            text_temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False)
            text_temp_file.write(text_content)
            text_temp_file.close()
            
            return (
                formatted_feedback, 
                json_temp_file.name,
                text_temp_file.name,
                gr.update(visible=True),
                gr.update(visible=True)
            )
        except Exception as e:
            return (
                f"Error processing file: {str(e)}", 
                None, None,
                gr.update(visible=False), 
                gr.update(visible=False)
            )
    
    upload_button.upload(
        process_upload, 
        inputs=[upload_button], 
        outputs=[
            feedback_output, 
            download_json_button, 
            download_text_button,
            download_json_button,
            download_text_button
        ]
    )

playground_auth = (
    (settings.PLAYGROUND_USERNAME, settings.PLAYGROUND_PASSWORD)
    if settings.PLAYGROUND_PASSWORD
    else None
)

def app():
    """Main function to run the app."""
    # Run the Gradio app
    playground.launch(auth=playground_auth)