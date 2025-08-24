# ltx_automation_app/data/readme_templates.py

# ============ README TEMPLATES ============
# Templates from your ReadMes.xlsm file
README_TEMPLATES = {
    "example_1": {
        "display_name": "Example 1 - Standard MT Evaluation",
        "context": "Machine Translation",
        "lines": [
            "1. Please read through READ ME tab before you kick off the Evaluation Task:",
            "   A. Check out the Metrics and their corresponding Definitions & Notes to understand what aspects of the language performance you are evaluating against;",
            "   B. Check out the Scoring Definition section to understand how you should be scoring each segment from a range of 1 to 5;",
            "   C. The Weights/Percentage section is for your reference as to how much each metric is valued for this specific project.",
            "2. Once you are done reading through the READ ME tab, please move on to the Part 1 tabs to start the actual evaluation task.",
            "3. Pre-Eval: Before you start evaluating a segment, please take a quick look at both the SOURCE and TARGET columns, and:",
            "   A. If you find the source quality of a segment in SOURCE Column too terrible to understand, please choose Incomprehensible Input from the dropdown list of Pre-Eval column and skip the evaluation of this segment;",
            "   B. If you find that the content in TARGET Column is not the translation of source, please choose Irrelevant Output from the dropdown list and score 0.9 under every metric for this segment.",
            "4. If you don't see a big issue with either the SOURCE or TARGET, please start evaluating the segment from TARGET column:",
            "   A. First give an overall score (1 to 5) for the whole segment under the \"Overall\" Column;",
            "   B. Then evaluate per metric with a scoring range from 1 to 5;",
            "   C. Metrics are divided into \"Evergreen\" and \"Customized\", so please make sure to score all of them;",
            "   D. Please score each metric based on the overall performance in this aspect according to the scoring definition;",
            "   E. If a translation issue has an impact on more than one metric, please penalize it accordingly in multiple metrics as needed.",
            "5. Overall Rating will be automatically calculated with pre-filled formulas in both non-weighted and weighted forms, so please don't touch any of the RATING Columns.",
            "6. If you have any comments for the segment, you could leave them under the Additional Notes Column.",
            "7. After completing the rating work for Part 1, please review the entire section again to check for any cells with a yellow background. If a cell has a yellow background, it's possible that you have either forgotten to add a rating or entered an invalid rating value.",
            "8. With the evaluation done, all relevant data will be automatically pulled to Part 2 - Data Analysis tab for data analysis in both numbers and visuals formats, and comparison will be available if evaluation is done on multiple tools.",
            "9. Based on data displayed in Part 2 - Data Analysis tab, please provide your take on the performance of each tool included in the Data Analysis Summary at the top of the tab, and make sure to answer all questions listed to be thorough.",
            "10. In Part 3 - Criteria Based Assess tab, please provide comments to questions regarding criteria specific to the project and your overall summary for you locale, so that the Project Lead can incorporate your opinions into the final Report.",
            "11. Once you are done with the whole process, please rename your file by adding the Completion Date and Your name."
        ],
        "formatting": {
            "colored_terms": {
                "Evergreen": "green",
                "Customized": "orange",
                "Incomprehensible Input": "blue",
                "Irrelevant Output": "blue"
            },
            "bold_terms": ["SOURCE", "TARGET", "Overall", "Part 1", "Part 2 - Data Analysis", "Part 3 - Criteria Based Assess", "Additional Notes", "RATING", "Data Analysis Summary"]
        },
        "terminology": {
            "source_issue": "Incomprehensible Input",
            "target_issue": "Irrelevant Output",
            "scoring_instruction": "score 0.9 under every metric"
        },
        "includes_yellow_warning": True
    },
    
    # Add more examples as they appear in other columns of your Excel file
    "example_2": {
        "display_name": "Example 2",
        "context": "To be determined",
        "lines": [
            # Would be populated from column C of your Excel
        ],
        "terminology": {
            "source_issue": "Incomprehensible Source",
            "target_issue": "Irrelevant Target",
            "scoring_instruction": "score 0.9 under every metric"
        },
        "includes_yellow_warning": False
    }
}

# ============ EDITABLE SECTIONS ============
# Define which sections can be edited independently
EDITABLE_SECTIONS = {
    "intro": [1],  # Line 1 with sub-points
    "start_evaluation": [2],  # Line 2
    "pre_eval": [3],  # Line 3 with sub-points
    "evaluation_process": [4],  # Line 4 with sub-points
    "rating_calculation": [5],  # Line 5
    "comments": [6],  # Line 6
    "yellow_warning": [7],  # Line 7 (optional)
    "data_analysis": [8, 9],  # Lines 8-9
    "final_steps": [10, 11]  # Lines 10-11
}

# ============ FORMATTING HELPERS ============
class InstructionFormatter:
    """Helper to maintain formatting when editing instructions"""
    
    @staticmethod
    def apply_formatting(text: str, formatting_rules: dict) -> str:
        """Apply bold, colors, etc. to instruction text"""
        # This would handle the formatting preservation
        # For now, we'll implement this in the Excel builder
        return text
    
    @staticmethod
    def parse_section(lines: list, section_name: str) -> dict:
        """Parse a section of instructions for editing"""
        section_lines = EDITABLE_SECTIONS.get(section_name, [])
        return {
            "section_name": section_name,
            "lines": [lines[i-1] for i in section_lines if i <= len(lines)],
            "editable": True
        }# ltx_automation_app/data/readme_templates.py

# ============ README TEMPLATES ============
# All templates from your ReadMes.xlsm file
README_TEMPLATES = {
    "standard_mt": {
        "display_name": "Standard MT Evaluation",
        "context": "Machine Translation",
        "lines": [
            "1. Please read through READ ME tab before you kick off the Evaluation Task:",
            "   A. Check out the Metrics and their corresponding Definitions & Notes to understand what aspects of the language performance you are evaluating against;",
            "   B. Check out the Scoring Definition section to understand how you should be scoring each segment from a range of 1 to 5;",
            "   C. The Weights/Percentage section is for your reference as to how much each metric is valued for this specific project.",
            "2. Once you are done reading through the READ ME tab, please move on to the Part 1 tabs to start the actual evaluation task.",
            "3. Pre-Eval: Before you start evaluating a segment, please take a quick look at both the SOURCE and TARGET columns, and:",
            "   A. If you find the source quality of a segment in SOURCE Column too terrible to understand, please choose Incomprehensible Input from the dropdown list of Pre-Eval column and skip the evaluation of this segment.",
            "   B. If you find that the content in TARGET Column is not the translation of source, please choose Irrelevant Output from the dropdown list and score 0.9 under every metric for this segment.",
            "4. If you don't see a big issue with either the SOURCE or TARGET, please start evaluating the segment from TARGET column:",
            "   A. First give an overall score (1 to 5) for the whole segment under the \"Overall\" Column;",
            "   B. Then evaluate per metric with a scoring range from 1 to 5;",
            "   C. Metrics are divided into \"Evergreen\" and \"Customized\", so please make sure to score all of them;",
            "   D. Please score each metric based on the overall performance in this aspect according to the scoring definition;",
            "   E. If a translation issue has an impact on more than one metric, please penalize it accordingly in multiple metrics as needed.",
            "5. Overall Rating will be automatically calculated with pre-filled formulas in both non-weighted and weighted forms, so please don't touch any of the RATING Columns.",
            "6. If you have any comments for the segment, you could leave them under the Additional Notes Column.",
            "7. After completing the rating work for Part 1, please review the entire section again to check for any cells with a yellow background. If a cell has a yellow background, it's possible that you have either forgotten to add a rating or entered an invalid rating value.",
            "8. With the evaluation done, all relevant data will be automatically pulled to Part 2 - Data Analysis tab for data analysis in both numbers and visuals formats, and comparison will be available if evaluation is done on multiple tools.",
            "9. Based on data displayed in Part 2 - Data Analysis tab, please provide your take on the performance of each tool included in the Data Analysis Summary at the top of the tab, and make sure to answer all questions listed to be thorough.",
            "10. In Part 3 - Criteria Based Assess tab, please provide comments to questions regarding criteria specific to the project and your overall summary for you locale, so that the Project Lead can incorporate your opinions into the final Report.",
            "11. Once you are done with the whole process, please rename your file by adding the Completion Date and Your name."
        ],
        "terminology": {
            "source_issue": "Incomprehensible Input",
            "target_issue": "Irrelevant Output",
            "scoring_instruction": "score 0.9 under every metric"
        },
        "includes_yellow_warning": True
    },
    
    "llm_evaluation": {
        "display_name": "LLM Evaluation Template",
        "context": "Large Language Model",
        "lines": [
            "1. Please read through READ ME tab before starting the LLM Evaluation:",
            "   A. Review the evaluation criteria and metrics specific to LLM output quality;",
            "   B. Understand the 1-5 scoring scale for each metric;",
            "   C. Note the weight distribution for this LLM evaluation project.",
            "2. Proceed to Part 1 tabs to evaluate each LLM's output.",
            "3. Pre-Evaluation Check:",
            "   A. If the input prompt is incomprehensible, select 'Incomprehensible Input' and skip;",
            "   B. If the LLM output is completely irrelevant to the prompt, select 'Irrelevant Output' and score 0.9 for all metrics.",
            "4. For valid outputs, evaluate against each metric:",
            "   A. Start with an Overall score (1-5);",
            "   B. Score each individual metric;",
            "   C. Consider both functional and quality aspects;",
            "   D. Apply penalties across multiple metrics when issues overlap.",
            "5. Ratings are auto-calculated - do not modify RATING columns.",
            "6. Add specific feedback in Additional Notes as needed.",
            "7. Check for yellow-highlighted cells indicating missing scores.",
            "8. Part 2 will aggregate your evaluations for analysis.",
            "9. Complete the Data Analysis Summary with your insights.",
            "10. Part 3 captures your overall assessment and recommendations.",
            "11. Save file with completion date and evaluator name."
        ],
        "terminology": {
            "source_issue": "Incomprehensible Input",
            "target_issue": "Irrelevant Output",
            "scoring_instruction": "score 0.9 for all metrics"
        },
        "includes_yellow_warning": True
    },
    
    "genai_content": {
        "display_name": "GenAI Content Evaluation",
        "context": "Generative AI",
        "lines": [
            "1. Review this README before evaluating GenAI content:",
            "   A. Familiarize yourself with GenAI-specific metrics;",
            "   B. Understand the 1-5 quality scale;",
            "   C. Note metric weights for this project type.",
            "2. Navigate to Part 1 to begin content evaluation.",
            "3. Initial Quality Check:",
            "   A. Skip if source prompt is incomprehensible;",
            "   B. Mark as 'Irrelevant' if output doesn't match prompt intent.",
            "4. Evaluate each content piece:",
            "   A. Overall impression score first;",
            "   B. Individual metric scoring;",
            "   C. Consider creativity, accuracy, and appropriateness;",
            "   D. Cross-metric penalty for overlapping issues.",
            "5. Automated calculations will handle ratings.",
            "6. Document specific issues in notes.",
            "7. Review for completion (yellow cells).",
            "8. Part 2 compiles evaluation data.",
            "9. Provide analytical summary.",
            "10. Complete final assessment in Part 3."
        ],
        "terminology": {
            "source_issue": "Incomprehensible Prompt",
            "target_issue": "Irrelevant Generation",
            "scoring_instruction": "assign 0.9 to all metrics"
        },
        "includes_yellow_warning": True
    },
    
    "qa_evaluation": {
        "display_name": "QA Evaluation Process",
        "context": "Quality Assurance",
        "lines": [
            "1. QA Evaluation Guidelines:",
            "   A. Review QA-specific metrics and criteria;",
            "   B. Understand scoring methodology;",
            "   C. Check metric importance weights.",
            "2. Begin evaluation in Part 1.",
            "3. Pre-screening:",
            "   A. Flag incomprehensible sources;",
            "   B. Mark non-translations as irrelevant.",
            "4. Quality Assessment:",
            "   A. Overall quality rating;",
            "   B. Detailed metric evaluation;",
            "   C. Apply comprehensive scoring.",
            "5. Let formulas calculate final ratings.",
            "6. Add constructive feedback.",
            "7. Verify all scores are complete.",
            "8. Review analysis in Part 2.",
            "9. Summarize findings.",
            "10. Final recommendations in Part 3."
        ],
        "terminology": {
            "source_issue": "Source Quality Issue",
            "target_issue": "Translation Failure",
            "scoring_instruction": "rate as 0.9"
        },
        "includes_yellow_warning": False
    }
}

# ============ CUSTOM README BUILDER ============
class CustomReadmeBuilder:
    """Helper class for building custom README instructions"""
    
    @staticmethod
    def get_default_structure():
        """Returns the basic structure for custom README creation"""
        return {
            "intro_line": "1. Please read through READ ME tab before starting:",
            "sub_sections": {
                "metrics_review": "A. Review the metrics and their definitions",
                "scoring_review": "B. Understand the 1-5 scoring scale",
                "weights_review": "C. Note the metric weights"
            },
            "evaluation_start": "2. Proceed to Part 1 tabs to begin evaluation.",
            "pre_eval_checks": {
                "source_check": "A. If source is incomprehensible, select '{source_issue}' and skip",
                "target_check": "B. If target is irrelevant, select '{target_issue}' and {scoring_instruction}"
            },
            "scoring_process": [
                "4. For valid entries, evaluate each metric:",
                "   A. Start with Overall score",
                "   B. Score individual metrics",
                "   C. Apply penalties across metrics as needed"
            ],
            "completion_steps": [
                "5. Ratings auto-calculate - don't modify",
                "6. Add notes as needed",
                "7. Check for missing scores (yellow cells)",
                "8. Part 2 aggregates data",
                "9. Complete analysis summary",
                "10. Final assessment in Part 3",
                "11. Save with date and name"
            ]
        }

# ============ TERMINOLOGY OPTIONS ============
TERMINOLOGY_OPTIONS = {
    "source_issues": [
        "Incomprehensible Input",
        "Incomprehensible Source", 
        "Source Quality Issue",
        "Incomprehensible Prompt",
        "Unreadable Input"
    ],
    "target_issues": [
        "Irrelevant Output",
        "Irrelevant Target",
        "Translation Failure", 
        "Irrelevant Generation",
        "Non-Translation"
    ],
    "scoring_methods": [
        "score 0.9 under every metric",
        "score 0.9 for all metrics",
        "assign 0.9 to all metrics",
        "rate as 0.9",
        "skip evaluation"
    ]
}