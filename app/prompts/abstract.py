from app.prompts.utils import get_prompt

get_abstract_prompt = get_prompt(
  key="abstract",
  fallback="""\
Review my thesis proposal abstract and provide feedback on the following aspects:

1. Length and completeness: Is it appropriately sized (approximately 1/3-1/2 page or ~250 words)? Does it concisely summarize the entire proposal?

2. Content coverage: Does it include brief mentions of all key elements:
   - Problem context
   - Motivation for solving it
   - Proposed approach/solution
   - Expected outcomes or significance

3. Balance: Is it too technical or too vague? Does it provide a clear overview without unnecessary detail?

4. Accessibility: Would someone unfamiliar with my specific topic understand the general purpose and approach of my proposal?

5. Independence: Does it stand alone as a complete summary of the proposal that could be read separately?

6. Language: Is it written in clear, direct language with active voice and minimal jargon? 

7. Repetition: While it's acceptable to repeat key points from later sections, are there any unnecessary repetitions?

The abstract should function as a "mini-proposal" that gives readers a complete picture of what to expect in the full document. It should be the last section written but the first one read, making it crucial for creating a good first impression.

Keep the issues small, you can have multiple sub-aspects per aspect to touch on, as many as needed. Be complete! Do not get hung up on length! Be really concise and prioritize extremely well to not overwhelm me. I want to have specific and easy to implement action items! Go above and beyond and reflect deeply. Do not be ambiguous and be very explicit, you are a very critical expert researcher and software engineer!

{{proposal}}
""")
