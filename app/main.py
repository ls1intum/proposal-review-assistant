from typing import Optional, List
from pydantic import BaseModel, Field
import logging
import sys
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


def upload_file(file):
    proposal = convert_pdf_to_clean_markdown(file.name)
    print(f"Converted proposal: {proposal}")
    chain = RunnableParallel({
        "general_writing": get_general_writing_prompt() | issue_model,
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
            issues.append(feedback.model_dump_json())
    return issues

with gr.Blocks() as playground:
    file_output = gr.Textbox()
    upload_button = gr.UploadButton("Click to Upload a Proposal", file_types=[".pdf"])
    upload_button.upload(upload_file, upload_button, file_output)

playground_auth = (
    (settings.PLAYGROUND_USERNAME, settings.PLAYGROUND_PASSWORD)
    if settings.PLAYGROUND_PASSWORD
    else None
)

def app():
    """Main function to run the app."""
    # Run the Gradio app
    playground.launch(auth=playground_auth)