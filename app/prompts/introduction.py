from app.prompts.utils import get_prompt

get_introduction_prompt = get_prompt(
  key="introduction",
  fallback="""\
Evaluate my thesis proposal introduction and provide feedback on the following aspects:

1. Length: Is it appropriately sized (less than one page, approximately 300 words)?

2. Focus: Does it introduce the general setting without prematurely describing the problem or solution?

3. Context: Does it effectively establish the environment and tools in use without diving into solutions?

4. Background: Does it provide sufficient context for understanding the problem that will be described in the next section?

5. Clarity: Is it written clearly with appropriate citations to support contextual statements?

6. Structure: Does it lead logically into the problem section with a smooth transition?

7. Active voice: Is it written predominantly in active voice with clear identification of actors?

8. Citations: Are facts or claims properly supported by citations to scientific literature placed before periods?

The introduction should set the stage for the proposal without jumping ahead to problem statements or solution discussions. It should be concise yet informative, providing readers with the necessary background to understand the significance of the research.

Keep the issues small, you can have multiple sub-aspects per aspect to touch on, as many as needed. Be complete! Do not get hung up on length! Be really concise and prioritize extremely well to not overwhelm me. I want to have specific and easy to implement action items! Go above and beyond and reflect deeply. Do not be ambiguous and be very explicit, you are a very critical expert researcher and software engineer!

{{proposal}}
""")