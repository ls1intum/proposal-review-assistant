"""
This module contains the prompt for evaluating the diagrams and figures in a thesis proposal.
"""

DIAGRAMS_FIGURES_PROMPT = """
Review the diagrams and figures in my thesis proposal and provide feedback on the following aspects:

1. Quantity: Are there at least 2 diagrams/mockups as required?

2. UML requirement: Is at least one diagram a suitable UML diagram for your topic?

3. Caption quality: Do figures have descriptive, extensive captions that explain their significance rather than just labeling them?

4. In-text references: Are all figures directly referenced in the text (e.g., "Figure 1 shows...")?

5. Visual quality: Are all figures and diagrams clear, readable, and appropriately sized at 100% PDF zoom?

6. Display mode: Are screenshots presented in light mode rather than dark mode (for better readability on white paper)?

7. Diagram choice: If sequence diagrams are used, would activity or communication diagrams be more appropriate?

8. Technical quality: Are vector graphics (SVG, PDF) used where possible for better readability and smaller file size?

9. Simplicity: Are diagrams kept reasonably simple (7±2 elements) without excessive detail?

10. Placement: Are figures positioned close to where they are first mentioned in the text?

11. Consistency: Do all figures use consistent styles, formatting, and keys (legends) throughout the document?

12. Axis labels: For charts or graphs, are x and y axes properly labeled?

Figures and diagrams should enhance understanding, not just decorate the document. They should be integral to explaining concepts in your proposal and be properly integrated with the text.
"""