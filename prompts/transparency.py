"""
This module contains the prompt for evaluating the transparency statement of a thesis proposal.
"""

TRANSPARENCY_PROMPT = """
Review my thesis proposal's transparency statement and provide feedback on the following aspects:

1. Presence: Does the proposal include a transparency statement regarding the use of AI tools?

2. Specificity: Does the statement clearly identify which AI tools were used (e.g., ChatGPT, Grammarly, DeepL)?

3. Usage details: Does it explain how these tools were used in the writing process?

4. Personalization: Is the statement specific to this proposal rather than a generic template?

5. Ethicality: Does it demonstrate ethical usage by explaining how AI-generated content was reviewed and adapted?

6. Placement: Is the statement appropriately placed at the end of the proposal, after the bibliography?

7. Tone: Is it written in a straightforward, honest manner without being defensive?

8. Point of view: Is it written from a first-person perspective, using "I" statements?

9. Responsibility: Does it emphasize that the final content was reviewed and approved by the author? (e.g. "I have carefully checked all texts created with these tools to ensure that they are correct and make sense")

The transparency statement should candidly acknowledge any AI assistance used in creating the proposal while demonstrating that you took responsibility for the final content. If no AI tools were used, a simple statement to that effect is sufficient.
"""