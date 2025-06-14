from app.prompts.utils import get_prompt

get_motivation_prompt = get_prompt(
  key="motivation",
  fallback="""\
Review my thesis proposal's motivation section and provide feedback on the following aspects:

1. Length: Is it appropriately sized (approximately 300 words or 2/3 page)?

2. Scientific importance: Does it clearly outline why solving this problem is scientifically important?

3. Stakeholder benefits: Does it use actors/stakeholders to present the solution benefits without being too specific about implementation?

4. Forward focus: Does it focus on positive aspects when the solution is available rather than repeating the problem description?

5. Vision: Does it present a compelling and forward-looking vision?

6. Scientific grounding: Does it appropriately reference existing research and previous work?

7. Citations: Does it include sufficient citations to scientific literature (helping toward the 6-8 publication minimum)?

8. Language: Is it written in active voice with minimal filler words or superlatives?

9. Distinction: Does it avoid repeating content from the problem section and instead focus on why solving the problem matters?

The motivation section should inspire interest in the solution without being a rehash of the problem section. It should emphasize why this research matters in a broader scientific context and how it will benefit stakeholders. This section should be visionary while remaining academically grounded.

Keep the issues small, you can have multiple sub-aspects per aspect to touch on, as many as needed. Be complete! Do not get hung up on length! Be really concise and prioritize extremely well to not overwhelm me. I want to have specific and easy to implement action items! Go above and beyond and reflect deeply. Do not be ambiguous and be very explicit, you are a very critical expert researcher and software engineer!

{{proposal}}
""")