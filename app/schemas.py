from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class ToneEnum(str, Enum):
    professional = "professional"
    creative = "creative"
    technical = "technical"
    executive = "executive"


#requesti models

class TailorRequest(BaseModel):
    resume_text: str = Field(..., description="The candidate's full resume text")
    job_description: str = Field(..., description="The target job description")
    tone: ToneEnum = Field(ToneEnum.professional, description="Writing tone for the tailored resume")

    model_config = {
        "json_schema_extra": {
            "example": {
                "resume_text": "John Doe\nSoftware Engineer\n5 years of Python experience...",
                "job_description": "We are looking for a Senior Python Engineer...",
                "tone": "professional"
            }
        }
    }


class CoverLetterRequest(BaseModel):
    resume_text: str = Field(..., description="The candidate's full resume text")
    job_description: str = Field(..., description="The target job description")
    company_name: str = Field(..., description="Name of the company being applied to")
    candidate_name: str = Field(..., description="Candidate's full name")
    tone: ToneEnum = Field(ToneEnum.professional, description="Writing tone for the cover letter")


class GapAnalysisRequest(BaseModel):
    resume_text: str = Field(..., description="The candidate's full resume text")
    job_description: str = Field(..., description="The target job description")


class BulletImprovementRequest(BaseModel):
    bullet_points: list[str] = Field(..., description="List of resume bullet points to improve")
    target_role: Optional[str] = Field(None, description="Target role to tailor the bullets for")


#response models

class TailorResponse(BaseModel):
    tailored_resume: str = Field(..., description="The tailored resume text")
    changes_summary: str = Field(..., description="Summary of key changes made")
    match_score: int = Field(..., description="Estimated match score 0-100", ge=0, le=100)


class CoverLetterResponse(BaseModel):
    cover_letter: str = Field(..., description="The generated cover letter")
    word_count: int = Field(..., description="Word count of the cover letter")


class SkillGap(BaseModel):
    skill: str
    importance: str 
    suggestion: str


class GapAnalysisResponse(BaseModel):
    matching_skills: list[str] = Field(..., description="Skills the candidate already has")
    missing_skills: list[SkillGap] = Field(..., description="Skills the candidate is missing")
    overall_fit_score: int = Field(..., ge=0, le=100)
    recommendation: str = Field(..., description="Overall recommendation")


class ImprovedBullet(BaseModel):
    original: str
    improved: str
    improvement_reason: str


class BulletImprovementResponse(BaseModel):
    improved_bullets: list[ImprovedBullet]
    general_tips: list[str]


class HealthResponse(BaseModel):
    status: str
    version: str
    model: str
