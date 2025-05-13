"""
This module contains the prompt for evaluating the bibliography section of a thesis proposal.
"""

BIBLIOGRAPHY_PROMPT = """
Analyze my thesis proposal's bibliography and provide feedback on the following aspects:

1. Quality: Does it include only scientific and peer-reviewed publications (conference papers, journal articles, scientific books)?

2. Quantity: Does it contain at least 6-8 citations as required?

3. Relevance: Are all cited sources relevant and contribute meaningfully to the proposal's argument or background?

4. Citation style: Is a consistent citation style used throughout the proposal (ideally alpha style with [ABC12])?

5. Internet sources: Are internet sources excluded from the bibliography and included as footnotes instead (if used at all)?

6. Citation quality: Are citations properly formatted (not simply copied and pasted from Google Scholar entries)?

7. Citation placement: Are in-text citations placed before periods rather than after them?

8. Cross-referencing: Do all citations in the text appear in the bibliography and vice versa?

9. Distribution: Are citations appropriately distributed throughout the proposal rather than clustered in one section?

10. Formatting: Are entries clean and free from duplicate or incorrect information (e.g., location details for ACM conferences)?

The bibliography should demonstrate your familiarity with relevant scientific literature and provide a solid foundation for your research. Quality and relevance of sources are more important than quantity beyond the minimum requirement.
"""