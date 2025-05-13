OBJECTIVE_PROMPT = """
Analyze my thesis proposal's objectives section and provide feedback on the following aspects:

1. Length: Is it sufficiently detailed (approximately 800-900 words or 2 pages total, excluding diagrams)?

2. Structure: Does it begin with a short overview listing enumerated goals (1., 2., 3., etc.)?

3. Goal expansion: Does each goal have its own subsection that repeats the bullet point and expands on it with at least two paragraphs?

4. Clarity: Are the goals clearly defined and measurable rather than vague?

5. Specificity: Are the objectives specific enough to guide the research but not so detailed that they prescribe exact implementation?

6. Visualization: Does the section include appropriate diagrams (contributing to the minimum requirement of 2 diagrams)?

7. Diagram quality: If diagrams are present:
   - Is at least one a UML diagram?
   - Do they have detailed, descriptive captions explaining their significance?
   - Are they directly referenced in the text (e.g., "Figure 1 shows...")?

8. Alignment: Do the objectives logically address the problem described earlier?

9. Feasibility: Do the objectives seem achievable within the scope of a thesis?

The objectives section should provide a clear roadmap for what you aim to accomplish, with enough detail to show how these goals will address the stated problem.
"""