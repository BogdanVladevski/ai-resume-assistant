import json
import re
import logging
from langchain_openai import ChatOpenAI
from langchain.schema.output_parser import StrOutputParser

from app.config import get_settings
from app.prompts import (
    tailor_prompt,
    cover_letter_prompt,
    gap_analysis_prompt,
    bullet_improvement_prompt,
)
from app.schemas import (
    TailorResponse,
    CoverLetterResponse,
    GapAnalysisResponse,
    BulletImprovementResponse,
    SkillGap,
    ImprovedBullet,
)

logger = logging.getLogger(__name__)


def _get_llm(temperature: float | None = None) -> ChatOpenAI:
    """Instantiate the ChatOpenAI model from settings."""
    settings = get_settings()
    return ChatOpenAI(
        model=settings.model_name,
        temperature=temperature if temperature is not None else settings.temperature,
        max_tokens=settings.max_tokens,
        openai_api_key=settings.openai_api_key,
    )


def _parse_json_response(raw: str) -> dict:
    """Strip markdown fences and parse JSON from model output."""
    cleaned = re.sub(r"```(?:json)?", "", raw).strip().rstrip("`").strip()
    return json.loads(cleaned)


#tailoring resume

async def run_tailor_chain(
    resume_text: str,
    job_description: str,
    tone: str,
) -> TailorResponse:
    llm = _get_llm()
    chain = tailor_prompt | llm | StrOutputParser()

    logger.info("Running tailor chain (tone=%s)", tone)
    raw_output: str = await chain.ainvoke({
        "resume_text": resume_text,
        "job_description": job_description,
        "tone": tone,
    })

    match_score = 75  
    changes_summary = ""
    tailored_resume = raw_output

    if "CHANGES SUMMARY:" in raw_output:
        parts = raw_output.split("CHANGES SUMMARY:")
        tailored_resume = parts[0].strip()
        rest = parts[1]

        score_match = re.search(r"MATCH_SCORE:\s*(\d+)", rest)
        if score_match:
            match_score = min(100, max(0, int(score_match.group(1))))
            changes_summary = rest[: score_match.start()].strip()
        else:
            changes_summary = rest.strip()

    return TailorResponse(
        tailored_resume=tailored_resume,
        changes_summary=changes_summary,
        match_score=match_score,
    )


#Cover Letter

async def run_cover_letter_chain(
    resume_text: str,
    job_description: str,
    company_name: str,
    candidate_name: str,
    tone: str,
) -> CoverLetterResponse:
    llm = _get_llm(temperature=0.6)  # slightly more creative
    chain = cover_letter_prompt | llm | StrOutputParser()

    logger.info("Running cover letter chain for %s @ %s", candidate_name, company_name)
    cover_letter: str = await chain.ainvoke({
        "resume_text": resume_text,
        "job_description": job_description,
        "company_name": company_name,
        "candidate_name": candidate_name,
        "tone": tone,
    })

    word_count = len(cover_letter.split())
    return CoverLetterResponse(cover_letter=cover_letter.strip(), word_count=word_count)


#Gap analysis

async def run_gap_analysis_chain(
    resume_text: str,
    job_description: str,
) -> GapAnalysisResponse:
    llm = _get_llm(temperature=0.1)  
    chain = gap_analysis_prompt | llm | StrOutputParser()

    logger.info("Running gap analysis chain")
    raw_output: str = await chain.ainvoke({
        "resume_text": resume_text,
        "job_description": job_description,
    })

    data = _parse_json_response(raw_output)

    missing_skills = [
        SkillGap(
            skill=s["skill"],
            importance=s.get("importance", "nice-to-have"),
            suggestion=s.get("suggestion", ""),
        )
        for s in data.get("missing_skills", [])
    ]

    return GapAnalysisResponse(
        matching_skills=data.get("matching_skills", []),
        missing_skills=missing_skills,
        overall_fit_score=min(100, max(0, int(data.get("overall_fit_score", 50)))),
        recommendation=data.get("recommendation", ""),
    )


#bullet improvement

async def run_bullet_improvement_chain(
    bullet_points: list[str],
    target_role: str | None,
) -> BulletImprovementResponse:
    llm = _get_llm(temperature=0.4)
    chain = bullet_improvement_prompt | llm | StrOutputParser()

    bullet_points_text = "\n".join(f"- {b}" for b in bullet_points)
    role_label = target_role or "General / Not specified"

    logger.info("Running bullet improvement chain (%d bullets)", len(bullet_points))
    raw_output: str = await chain.ainvoke({
        "bullet_points_text": bullet_points_text,
        "target_role": role_label,
    })

    data = _parse_json_response(raw_output)

    improved = [
        ImprovedBullet(
            original=b["original"],
            improved=b["improved"],
            improvement_reason=b.get("improvement_reason", ""),
        )
        for b in data.get("improved_bullets", [])
    ]

    return BulletImprovementResponse(
        improved_bullets=improved,
        general_tips=data.get("general_tips", []),
    )
