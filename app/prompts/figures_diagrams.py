from app.prompts.utils import get_prompt

get_figures_diagrams_prompt = get_prompt(
  key="figures-diagrams",
  fallback="""\
Review my thesis proposal's figures, diagrams, and tables and provide feedback on the following aspects:

1. Minimum requirements: Does the proposal contain at least 2 diagrams/mockups as required?

2. UML diagram requirement: Is at least one figure a suitable UML diagram (avoiding sequence diagrams in favor of activity or communication diagrams)?

3. Figure quality and readability: 
   - Are all figures readable when viewed at 100% zoom in PDF?
   - Do figures use vector graphics (SVG, PDF) when possible for better quality and smaller file size?
   - Are screenshots taken in light mode (avoiding dark mode which wastes ink and looks poor on paper)?

4. Caption quality: Do figures have long, informative, and descriptive captions rather than short, generic ones?

5. Text integration: Are all figures and tables properly referenced in the text (e.g., "Figure 1 shows...") and explained in detail?

6. Placement: Are figures and tables placed close to where they are first referenced for better readability?

7. Consistency: Do all figures maintain consistent styles, formats, keys (legends), and labeling throughout the proposal?

8. Diagram appropriateness: Are the diagrams high-level and problem-focused rather than implementation-detailed?

9. Axis labeling: For charts and graphs, are x and y axes properly labeled with consistent units?

10. Simplicity: Are figures kept simple without excessive detail that could overwhelm the reader?

11. Table usage: If tables are present, do they present structured, comparable data rather than serving as substitutes for narrative text?

12. Legend consistency: Do all figures use consistent keys/legends throughout the work?

13. Content appropriateness: Do figures and diagrams enhance understanding of the problem and objectives rather than focusing on implementation details?

Figures and diagrams are crucial for enhancing readability and helping readers understand complex concepts. They should be professional, clear, and directly support the proposal's narrative. Quality visual elements demonstrate attention to detail and improve the overall presentation of your research.

Keep the issues small, you can have multiple sub-aspects per aspect to touch on, as many as needed. Be complete! Be really concise and prioritize extremely well to not overwhelm me. I want to have specific and easy to implement action items! Go above and beyond and reflect deeply. Do not be ambiguous and be very explicit, you are a very critical expert researcher and software engineer!

{{proposal}}
""")
