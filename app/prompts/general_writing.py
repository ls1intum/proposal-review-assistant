from app.prompts.utils import get_prompt

get_general_writing_prompt = get_prompt(
  key="general-writing",
  fallback="""\
Analyze the general writing quality of my thesis proposal and provide feedback on the following aspects:

1. Active vs. passive voice: Identify passages where passive voice is used and suggest active alternatives with clear actors. Scientific writing requires identifying actors and powerful subjects for all sentences.

2. Sentence structure: Flag sentences starting with "As...", "Since...", "To...", "In order to...", or "Because..." and suggest alternatives that follow academic writing standards.

3. Word choice: Highlight instances of:
   - Filler words (e.g., "actually", "clearly", "obviously", "furthermore", "moreover", "also")
   - Strong statements/superlatives (e.g., "very", "wide", "optimal", "best", "perfect", "extremely")
   - Contractions (e.g., "don't" instead of "do not")
   - Excessive abbreviations without definition

4. Paragraph structure: 
   - Check if paragraphs are balanced (5-10 lines) 
   - Verify sections have at least two paragraphs (ideally half a page)
   - Ensure proper transitions between sections and paragraphs

5. Language precision: 
   - Flag vague terminology or unexplained jargon
   - Identify inconsistent terminology usage (repetitions are encouraged for consistency)
   - Highlight ambiguous statements

6. Citation placement: Verify citations are placed before periods rather than after them, following the alpha style [ABC12].

7. Writing style: Assess if the writing is concise, direct, and academic without excessive elaboration or complexity. Watch for German essay style sentences.

8. Pronoun usage: Check for inappropriate use of "I," "one," or "our" (use "we" sparingly, only when referring to the thesis approach).

Remember that scientific writing should use clear, direct language with active formulations and consistent terminology. Help me improve the overall quality and readability of my thesis proposal.

Keep the issues small, you can have multiple sub-aspects per aspect to touch on, as many as needed. Be complete! Be really concise and prioritize extremely well to not overwhelm me. I want to have specific and easy to implement action items! Go above and beyond and reflect deeply. Do not be ambiguous and be very explicit, you are a very critical expert researcher and software engineer!

{{proposal}}
""")