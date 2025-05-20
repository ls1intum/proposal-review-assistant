#!/usr/bin/env python3
"""
Command line interface for the proposal reviewer.
"""
import os
import sys
import json
import argparse
from pathlib import Path
import time

# Add project root to path
sys.path.append(str(Path(__file__).parent))

# Import from the simplified implementation
from proposal_reviewer import (
    review_proposal as simple_review_proposal,
)

def main():
    """Command-line interface for the proposal reviewer."""
    parser = argparse.ArgumentParser(description="Review thesis proposal PDFs with structured feedback.")
    parser.add_argument("pdf_path", help="Path to the proposal PDF file.")
    parser.add_argument("--output", "-o", help="Path to save the review results.", default="review_results.md")
    parser.add_argument("--json-output", help="Path to save structured feedback as JSON.", default="output/feedback.json")
    parser.add_argument("--flat-json-output", help="Path to save all feedback items as a flat list.", default="output/flat_feedback.json")
    parser.add_argument("--change-requests", help="Path to save simple change requests list (one per line).", default="output/change_requests.txt")
    parser.add_argument("--model", help="OpenAI model to use", default="o4-mini", 
                      choices=["o4-mini", "gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"])
    parser.add_argument("--verbose", "-v", action="store_true", help="Show detailed progress")
    
    args = parser.parse_args()
    
    # Check if the PDF file exists
    if not os.path.exists(args.pdf_path):
        print(f"Error: PDF file not found at {args.pdf_path}")
        sys.exit(1)
    
    print(f"Reviewing proposal at {args.pdf_path}...")
    
    try:
        # Start timing
        start_time = time.time()
        
        # Parse the proposal
        if args.verbose:
            print("Parsing proposal PDF...")
        
        # Review the proposal
        results = simple_review_proposal(args.pdf_path, args.model)
        
        # Save the results
        if args.verbose:
            print("Saving review results...")
        
        # Ensure output directory exists for Markdown output
        os.makedirs(os.path.dirname(os.path.abspath(args.output)) or ".", exist_ok=True)
        
        # Save structured JSON output
        if args.json_output or args.flat_json_output or args.change_requests:
            if args.verbose:
                print("Saving structured feedback as JSON...")
            
            feedback_data = {}
            all_feedback_items = []  # For flat list
            change_requests = []  # For simple change requests
            
            for section, feedback in results["section_feedbacks"].items():
                section_data = {"content_issues": [], "writing_issues": []}
                
                # Process content feedback
                content_feedback = feedback.get("content_feedback")
                if content_feedback and hasattr(content_feedback, "issues"):
                    content_issues = [{    
                        "section": section,
                        "category": issue.category,
                        "severity": issue.severity,
                        "quote": issue.quote,
                        "issue": issue.issue,
                        "suggestion": issue.suggestion,
                        "rule": issue.rule,
                        "feedback_type": "content"
                    } for issue in content_feedback.issues]
                    
                    section_data["content_issues"] = content_issues
                    all_feedback_items.extend(content_issues)
                    
                    # Create simple change requests for content issues
                    for issue in content_feedback.issues:
                        section_name = section
                        change_request = f"{section_name.capitalize()} > [{issue.severity}]"
                        if issue.rule:
                            change_request += f" {issue.rule} -"
                        if issue.quote:
                            change_request += f" \"{issue.quote}\" -"
                        change_request += f" {issue.issue} -> {issue.suggestion}"
                        change_requests.append(change_request)
                
                # Process writing feedback
                writing_feedback = feedback.get("writing_feedback")
                if writing_feedback and hasattr(writing_feedback, "issues"):
                    writing_issues = [{    
                        "section": section,
                        "category": issue.category,
                        "severity": issue.severity,
                        "quote": issue.quote,
                        "issue": issue.issue,
                        "suggestion": issue.suggestion,
                        "rule": issue.rule,
                        "feedback_type": "writing"
                    } for issue in writing_feedback.issues]
                    
                    section_data["writing_issues"] = writing_issues
                    all_feedback_items.extend(writing_issues)
                    
                    # Create simple change requests for writing issues
                    for issue in writing_feedback.issues:
                        section_name = section
                        change_request = f"{section_name.capitalize()} > [{issue.severity}]"
                        if issue.rule:
                            change_request += f" {issue.rule} -"
                        if issue.quote:
                            change_request += f" \"{issue.quote}\" -"
                        change_request += f" {issue.issue} -> {issue.suggestion}"
                        change_requests.append(change_request)
                
                feedback_data[section] = section_data
            
            # Sort change requests by section (abstract -> introduction -> problem -> motivation -> objective -> schedule -> bibliography -> transparency)
            change_requests.sort(key=lambda x: [
                "abstract", "introduction", "problem", "motivation", "objective", 
                "schedule", "bibliography", "transparency in the use of ai tools"
            ].index(x.split(" > ")[0].lower())
            )
            
            # Save structured feedback
            if args.json_output:
                # Ensure output directory exists for JSON
                os.makedirs(os.path.dirname(os.path.abspath(args.json_output)) or ".", exist_ok=True)
                
                with open(args.json_output, 'w', encoding='utf-8') as f:
                    json.dump(feedback_data, f, indent=2, ensure_ascii=False)
                
                if args.verbose:
                    print(f"Structured feedback saved to {args.json_output}")
            
            # Save flat list of all feedback items
            if args.flat_json_output:
                # Ensure output directory exists for flat JSON
                os.makedirs(os.path.dirname(os.path.abspath(args.flat_json_output)) or ".", exist_ok=True)
                
                with open(args.flat_json_output, 'w', encoding='utf-8') as f:
                    json.dump(all_feedback_items, f, indent=2, ensure_ascii=False)
                
                if args.verbose:
                    print(f"Flat feedback list saved to {args.flat_json_output}")
            
            # Save simple change requests (one per line)
            if args.change_requests:
                # Ensure output directory exists for change requests
                os.makedirs(os.path.dirname(os.path.abspath(args.change_requests)) or ".", exist_ok=True)
                
                with open(args.change_requests, 'w', encoding='utf-8') as f:
                    for request in change_requests:
                        f.write(f"{request}\n")
                
                if args.verbose:
                    print(f"Change requests saved to {args.change_requests}")
        
        # Print completion time
        end_time = time.time()
        if args.verbose:
            print(f"Review completed in {end_time - start_time:.2f} seconds")
        
        print(f"Review completed and saved to {args.output}")
        
    except KeyboardInterrupt:
        print("\nReview process interrupted.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main() 