"""
This module contains the prompt for evaluating the schedule section of a thesis proposal.
"""

SCHEDULE_PROMPT = """
Review my thesis proposal's schedule section and provide feedback on the following aspects:

1. Length: Is it appropriately sized (approximately 300-400 words or 3/4-1 page)?

2. Start date: Is there a clear thesis start date specified?

3. Iteration structure: Is the schedule divided into iterations of appropriate length (2-4 weeks)?

4. Work items: Does each iteration contain several smaller, specific work items?

5. Measurability: Are the work items measurable and deliverable, describing features that are vertically integrated?

6. Appropriate content: Does it avoid including thesis writing or presentation tasks?

7. Agile principles: Does it follow agile principles, avoiding phases like "requirements gathering" in favor of feature-focused iterations?

8. Reference to objectives: Does it reference the high-level goals from the objectives section?

9. Realism: Does the schedule seem realistic and achievable?

10. Clarity: Are iterations and tasks described clearly and consistently?

The schedule should demonstrate planning ability and project feasibility by breaking down the work into manageable iterations with clear deliverables that align with the stated objectives.
"""