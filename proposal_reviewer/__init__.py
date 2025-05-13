"""Proposal reviewer package for evaluating thesis proposals."""

from .simple_reviewer import SimpleProposal, review_proposal, FeedbackIssue, FeedbackIssueList

__all__ = ["SimpleProposal", "review_proposal", "FeedbackIssue", "FeedbackIssueList"]
