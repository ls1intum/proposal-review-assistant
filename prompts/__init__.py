"""
This package contains prompts for evaluating different sections of a thesis proposal.
Each prompt is designed to help identify quality issues in the thesis writing process.
"""

from .general_writing import GENERAL_WRITING_PROMPT
from .abstract import ABSTRACT_PROMPT
from .introduction import INTRODUCTION_PROMPT
from .problem import PROBLEM_PROMPT
from .motivation import MOTIVATION_PROMPT
from .objectives import OBJECTIVE_PROMPT
from .schedule import SCHEDULE_PROMPT
from .bibliography import BIBLIOGRAPHY_PROMPT
from .diagrams_figures import DIAGRAMS_FIGURES_PROMPT
from .transparency import TRANSPARENCY_PROMPT

__all__ = [
    'GENERAL_WRITING_PROMPT',
    'ABSTRACT_PROMPT',
    'INTRODUCTION_PROMPT',
    'PROBLEM_PROMPT',
    'MOTIVATION_PROMPT',
    'OBJECTIVE_PROMPT',
    'SCHEDULE_PROMPT',
    'BIBLIOGRAPHY_PROMPT',
    'DIAGRAMS_FIGURES_PROMPT',
    'TRANSPARENCY_PROMPT',
]