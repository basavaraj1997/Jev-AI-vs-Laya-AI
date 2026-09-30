"""
Pydantic Schemas for Convai Laya AI Decision Engine REST API
============================================================
Defines request and response structures for System 1 decision primitives:
- Choice: Multi-category classification
- Noul: Boolean / Propositional verification with calibrated probability
- Score: Ordinal rubric scoring
"""

from typing import Any, Dict, List, Literal, Optional, Union
from pydantic import BaseModel, Field

class ChoiceQuestion(BaseModel):
    type: Literal["choice"] = Field(
        default="choice",
        description="Select 'choice' for categorical classification."
    )
    instructions: str = Field(
        ...,
        description="The question or directive for the model (e.g., 'Select the target engineering team').",
        examples=["Which engineering team should resolve this production error?"]
    )
    criteria: List[str] = Field(
        ...,
        description="List of possible outcome labels or category options.",
        examples=[["sre_oncall", "billing_support", "frontend_team", "account_security"]]
    )

class NoulQuestion(BaseModel):
    type: Literal["noul"] = Field(
        default="noul",
        description="Select 'noul' for boolean hypothesis verification."
    )
    instructions: str = Field(
        ...,
        description="The propositional statement to evaluate as true/false against the context state.",
        examples=["Does this incident indicate an active production outage requiring urgent human escalation?"]
    )

class ScoreQuestion(BaseModel):
    type: Literal["score"] = Field(
        default="score",
        description="Select 'score' for ordinal rubric rating."
    )
    instructions: str = Field(
        ...,
        description="The rubric evaluation prompt.",
        examples=["Rate the operational severity of this issue from lowest to highest."]
    )
    criteria: List[str] = Field(
        ...,
        description="Ordered list of score levels (index 0 lowest).",
        examples=[["P4_low", "P3_medium", "P2_high", "P1_critical"]]
    )

QuestionDefinition = Union[ChoiceQuestion, NoulQuestion, ScoreQuestion, Dict[str, Any]]

class PredictionRequest(BaseModel):
    state: Dict[str, Any] = Field(
        ...,
        description="The context data or state to evaluate (must contain 'text' or structured context fields).",
        examples=[{
            "text": "CRITICAL: PostgreSQL master node out of memory on prod-us-east-1. Database returning HTTP 500."
        }]
    )
    questions: Dict[str, QuestionDefinition] = Field(
        ...,
        description="Dictionary mapping question IDs to their primitive definitions (Choice, Noul, Score).",
        examples=[{
            "service_domain": {
                "type": "choice",
                "instructions": "Which domain handles this?",
                "criteria": ["infrastructure", "billing", "frontend", "auth"]
            },
            "requires_pagerduty": {
                "type": "noul",
                "instructions": "Does this require waking up the on-call engineer?"
            },
            "severity_score": {
                "type": "score",
                "instructions": "Rate severity level.",
                "criteria": ["P4_low", "P3_medium", "P2_high", "P1_critical"]
            }
        }]
    )

class HealthResponse(BaseModel):
    status: str
    model: str
    device: str
    version: str
    uptime_seconds: float
    is_ready: bool

class PresetItem(BaseModel):
    id: str
    title: str
    description: str
    request: PredictionRequest
