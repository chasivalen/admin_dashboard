# ltx_automation_app/data/metrics_catalog.py

from typing import List, Dict, Tuple

# ========= EVERGREEN METRICS LIBRARY =========
# These are the standard metrics that users can choose from
EVERGREEN_METRICS = {
    "accuracy": {
        "display_name": "Accuracy",
        "definitions": {
            "mt": "source information is misinterpreted for the target translation, Numbers mismatch, Acronym mismatch",
            "genai": "Whether source information is misinterpreted or AI-generated content is factually incorrect",
            "qa": "Verification that translated content maintains the same meaning as source"
        },
        "default_notes": "e.g. 5km being translated as 3km, JAPAC being translated as APAC",
        "default_weight": 8
    },
    
    "fluency": {
        "display_name": "Fluency",
        "definitions": {
            "standard": "doesn't conform to grammar and syntactic rules of the target language, collocation issues, punctuation & spelling issues, wrong punctuations, missing spacing, typos; unidiomatic or unnatural translation, uneasy to understand",
            "natural": "unidiomatic or unnatural translation, uneasy to understand, doesn't sound like native speaker would say it"
        },
        "default_notes": "Note: Additional fluency examples and guidelines here",
        "default_weight": 5
    },
    
    "omission_addition": {
        "display_name": "Omission/Addition",
        "definitions": {
            "standard": "part of a segment missing or left in English, unnecessary/irrelevant information added to the target translation"
        },
        "default_notes": "Note: Examples and details here",
        "default_weight": 4
    },
    
    "compliance": {
        "display_name": "Compliance",
        "definitions": {
            "apple": "Apple Style & Terminology, Country standards, AppleCare Style & Terminology; Product/accessory/feature names, DNT, commonly used expressions within Apple; Date and time formats, format of the numbers not converting; Consistency with Terminology, Jargons and within the same article; Could be less important at the stage where the engine hasn't been trained with AppleCare content.",
            "general": "Adherence to client style guides, terminology databases, and brand guidelines"
        },
        "default_notes": "Please note that Apple MT is not engineered to convert measurements into different units, but please check if the formats of the numbers have been localized correctly in terms of measurement conventions. For example, whether commas, dots are added or removed per your locale.\n\n4,000\n4.000\n4000",
        "default_weight": 6
    }
}

# ========= CUSTOM METRICS LIBRARY =========
# Pre-defined custom metrics that users might want to use
CUSTOM_METRICS_LIBRARY = {
    "tone": {
        "display_name": "Tone",
        "definition": "Whether the generated content maintains appropriate tone for the context and audience",
        "default_notes": "Consider formality level, emotional tone, brand voice",
        "default_weight": 5
    },
    
    "cultural_adaptation": {
        "display_name": "Cultural Adaptation",
        "definition": "Content appropriately adapted for target culture including idioms, references, and local conventions",
        "default_notes": "",
        "default_weight": 4
    },
    
    "tag_url": {
        "display_name": "Tag/URL",
        "definition": "wrong/misplaced tags, wrongly localized url",
        "default_notes": "",
        "default_weight": 3
    },
    
    "red_flags": {
        "display_name": "Red Flags",
        "definition": "Profanity+Offensive+Political issues",
        "default_notes": "",
        "default_weight": None  # No weight
    }
}

# ========= ISSUES METRICS =========
# Fixed metrics for source/target issues
ISSUES_METRICS = {
    "incomprehensible_input": {
        "display_name": "Incomprehensible Input",
        "definition": "Impossible to understand the source/input",
        "notes": "Skip the evaluation for the segment",
        "weight": None
    },
    
    "irrelevant_output": {
        "display_name": "Irrelevant Output",
        "definition": "Target/output doesn't display translation of the source/input",
        "notes": "Mark All Metrics as 0.9",
        "weight": None
    }
}

# ========= HELPER FUNCTIONS =========
def get_evergreen_metric_names() -> List[str]:
    """Get list of evergreen metric names for dropdown"""
    return list(EVERGREEN_METRICS.keys())

def get_evergreen_metric_display_names() -> Dict[str, str]:
    """Get mapping of metric IDs to display names"""
    return {k: v["display_name"] for k, v in EVERGREEN_METRICS.items()}

def get_definitions_for_metric(metric_id: str) -> List[Tuple[str, str]]:
    """Get list of (def_id, definition_text) for a specific metric"""
    metric = EVERGREEN_METRICS.get(metric_id, {})
    definitions = metric.get("definitions", {})
    return [(def_id, def_text) for def_id, def_text in definitions.items()]

def get_custom_metric_suggestions() -> List[str]:
    """Get list of suggested custom metric names"""
    return [v["display_name"] for v in CUSTOM_METRICS_LIBRARY.values()]

def get_metric_details(metric_id: str) -> Dict:
    """Get full details for a metric (for Excel export)"""
    # Check evergreen first
    if metric_id in EVERGREEN_METRICS:
        return EVERGREEN_METRICS[metric_id]
    # Check custom library
    elif metric_id in CUSTOM_METRICS_LIBRARY:
        return CUSTOM_METRICS_LIBRARY[metric_id]
    # Check issues
    elif metric_id in ISSUES_METRICS:
        return ISSUES_METRICS[metric_id]
    return {}

# ========= LEGACY CATALOG FOR REFERENCE =========
# Keeping the old structure for reference/migration purposes
METRICS_CATALOG_LEGACY = {
    # ============ ACCURACY METRICS ============
    "accuracy_mt": {
        "display_name": "Accuracy",
        "category": "evergreen",
        "context": "MT",
        "definition": "source information is misinterpreted for the target translation, Numbers mismatch, Acronym mismatch",
        "notes": "e.g. 5km being translated as 3km, JAPAC being translated as APAC",
        "default_weight": 8,
        "row_height": 100
    },
    "accuracy_genai": {
        "display_name": "Accuracy",
        "category": "evergreen",
        "context": "GenAI",
        "definition": "Whether source information is misinterpreted or AI-generated content is factually incorrect",
        "notes": "",
        "default_weight": 7,
        "row_height": 70
    },
    "accuracy_qa": {
        "display_name": "Accuracy",
        "category": "evergreen",
        "context": "QA",
        "definition": "Verification that translated content maintains the same meaning as source",
        "notes": "Check for factual errors, number mismatches",
        "default_weight": 8,
        "row_height": 70
    },
    
    # ============ FLUENCY METRICS ============
    "fluency_standard": {
        "display_name": "Fluency",
        "category": "evergreen",
        "context": "Standard",
        "definition": "doesn't conform to grammar and syntactic rules of the target language, collocation issues, punctuation & spelling issues, wrong punctuations, missing spacing, typos; unidiomatic or unnatural translation, uneasy to understand",
        "notes": "Note: Additional fluency examples and guidelines here",
        "default_weight": 5,
        "row_height": 30
    },
    "fluency_natural": {
        "display_name": "Fluency/Naturalness",
        "category": "evergreen",
        "context": "Enhanced",
        "definition": "unidiomatic or unnatural translation, uneasy to understand, doesn't sound like native speaker would say it",
        "notes": "",
        "default_weight": 6,
        "row_height": 40
    },
    
    # ============ OMISSION/ADDITION METRICS ============
    "omission_addition": {
        "display_name": "Omission/Addition",
        "category": "evergreen",
        "context": "Standard",
        "definition": "part of a segment missing or left in English, unnecessary/irrelevant information added to the target translation",
        "notes": "Note: Examples and details here",
        "default_weight": 4,
        "row_height": 70
    },
    
    # ============ COMPLIANCE METRICS ============
    "compliance_apple": {
        "display_name": "Compliance",
        "category": "evergreen",
        "context": "Apple Style",
        "definition": "Apple Style & Terminology, Country standards, AppleCare Style & Terminology; Product/accessory/feature names, DNT, commonly used expressions within Apple; Date and time formats, format of the numbers not converting; Consistency with Terminology, Jargons and within the same article; Could be less important at the stage where the engine hasn't been trained with AppleCare content.",
        "notes": "Please note that Apple MT is not engineered to convert measurements into different units, but please check if the formats of the numbers have been localized correctly in terms of measurement conventions. For example, whether commas, dots are added or removed per your locale.\n\n4,000\n4.000\n4000",
        "default_weight": 6,
        "row_height": 40
    },
    
    # ============ CUSTOM METRICS ============
    "tone": {
        "display_name": "Tone",
        "category": "custom",
        "context": "GenAI",
        "definition": "Whether the generated content maintains appropriate tone for the context and audience",
        "notes": "Consider formality level, emotional tone, brand voice",
        "default_weight": 5,
        "row_height": 120
    },
    "cultural_adaptation": {
        "display_name": "Cultural Adaptation",
        "category": "custom",
        "context": "Localization",
        "definition": "Content appropriately adapted for target culture including idioms, references, and local conventions",
        "notes": "",
        "default_weight": 4,
        "row_height": 60
    },
    "tag_url": {
        "display_name": "Tag/URL",
        "category": "custom",
        "context": "Technical",
        "definition": "wrong/misplaced tags, wrongly localized url",
        "notes": "",
        "default_weight": 3,
        "row_height": 45
    },
    "red_flags": {
        "display_name": "Red Flags",
        "category": "custom",
        "context": "Safety",
        "definition": "Profanity+Offensive+Political issues",
        "notes": "",
        "default_weight": None,  # No weight
        "row_height": 45
    },
    
    # ============ SOURCE/TARGET ISSUES ============
    "incomprehensible_input": {
        "display_name": "Incomprehensible Input",
        "category": "source_target",
        "context": "Pre-Eval",
        "definition": "Impossible to understand the source/input",
        "notes": "Skip the evaluation for the segment",
        "default_weight": None,
        "row_height": 45
    },
    "irrelevant_output": {
        "display_name": "Irrelevant Output",
        "category": "source_target",
        "context": "Pre-Eval",
        "definition": "Target/output doesn't display translation of the source/input",
        "notes": "Mark All Metrics as 0.9",
        "default_weight": None,
        "row_height": 45
    }
}