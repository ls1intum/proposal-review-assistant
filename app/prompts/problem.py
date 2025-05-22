from app.prompts.utils import get_prompt

get_problem_prompt = get_prompt(
  key="problem",
  fallback="""\
Analyze my thesis proposal's problem section and provide feedback on the following aspects:

1. Length and depth: Is it appropriately sized (approximately 300 words or 2/3 page) with sufficient detail?

2. Problem clarity: Is the problem (or problems) clearly identified without ambiguity?

3. Stakeholder identification: Are the actors/stakeholders affected by the problem clearly identified?

4. Impact description: Are the negative consequences of the problem explained in detail?

5. Solution separation: Does the section avoid presenting solutions or alternatives? This section should focus exclusively on the problem.

6. Evidence: Is the problem supported by appropriate citations to scientific literature?

7. Specificity: Is the problem specific rather than general or vague?

8. Language: Is active voice used consistently, especially when describing how the problem affects stakeholders?

The problem section should clearly articulate what needs to be solved and why it matters, focusing exclusively on the issue without discussing potential solutions. It should make readers understand the negative consequences of leaving this problem unsolved.

Keep the issues small, you can have multiple sub-aspects per aspect to touch on, as many as needed. Be complete! Do not get hung up on length! Be really concise and prioritize extremely well to not overwhelm me. I want to have specific and easy to implement action items! Go above and beyond and reflect deeply. Do not be ambiguous and be very explicit, you are a very critical expert researcher and software engineer!

{{proposal}}
""")