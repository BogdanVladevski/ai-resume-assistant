import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import get_settings
from app.schemas import (
    TailorRequest, TailorResponse,
    CoverLetterRequest, CoverLetterResponse,
    GapAnalysisRequest, GapAnalysisResponse,
    BulletImprovementRequest, BulletImprovementResponse,
    HealthResponse,
)
from app.chains import (
    run_tailor_chain,
    run_cover_letter_chain,
    run_gap_analysis_chain,
    run_bullet_improvement_chain,
)

#logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)


#app lifecycle
@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    logger.info("Starting %s v%s — model: %s", settings.app_name, settings.version, settings.model_name)
    yield
    logger.info("Shutting down %s", settings.app_name)


#app init
settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description=(
        "AI-powered resume tailoring, cover letter generation, "
        "skill gap analysis, and bullet point improvement — "
        "built with LangChain + OpenAI."
    ),
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


#error expection handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.exception("Unhandled error: %s", exc)
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal error occurred. Please try again."},
    )


#routes

@app.get("/health", response_model=HealthResponse, tags=["System"])
async def health_check():
    """Liveness probe — confirms the service is running."""
    return HealthResponse(
        status="healthy",
        version=settings.version,
        model=settings.model_name,
    )


@app.post("/resume/tailor", response_model=TailorResponse, tags=["Resume"])
async def tailor_resume(request: TailorRequest):
    """
    Tailor a resume to a specific job description.

    - Rewrites the summary and bullet points to match the role
    - Mirrors ATS-friendly keywords from the job description
    - Returns the tailored resume, a changes summary, and a match score (0–100)
    """
    try:
        return await run_tailor_chain(
            resume_text=request.resume_text,
            job_description=request.job_description,
            tone=request.tone.value,
        )
    except Exception as e:
        logger.error("tailor_resume failed: %s", e)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/resume/cover-letter", response_model=CoverLetterResponse, tags=["Resume"])
async def generate_cover_letter(request: CoverLetterRequest):
    """
    Generate a tailored cover letter for a job application.

    - Personalised to the candidate's experience and the target role
    - Hooks the reader in the opening sentence
    - Returns the cover letter text and word count
    """
    try:
        return await run_cover_letter_chain(
            resume_text=request.resume_text,
            job_description=request.job_description,
            company_name=request.company_name,
            candidate_name=request.candidate_name,
            tone=request.tone.value,
        )
    except Exception as e:
        logger.error("generate_cover_letter failed: %s", e)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/resume/gap-analysis", response_model=GapAnalysisResponse, tags=["Analysis"])
async def gap_analysis(request: GapAnalysisRequest):
    """
    Analyse the gap between a resume and a job description.

    - Identifies matching skills and critical gaps
    - Scores overall fit (0–100)
    - Provides actionable suggestions for each missing skill
    """
    try:
        return await run_gap_analysis_chain(
            resume_text=request.resume_text,
            job_description=request.job_description,
        )
    except Exception as e:
        logger.error("gap_analysis failed: %s", e)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/resume/improve-bullets", response_model=BulletImprovementResponse, tags=["Resume"])
async def improve_bullets(request: BulletImprovementRequest):
    """
    Transform weak resume bullet points into powerful achievement statements.

    - Applies STAR method (Situation, Task, Action, Result)
    - Adds metrics and strong action verbs
    - Optionally tailored to a target role
    """
    try:
        return await run_bullet_improvement_chain(
            bullet_points=request.bullet_points,
            target_role=request.target_role,
        )
    except Exception as e:
        logger.error("improve_bullets failed: %s", e)
        raise HTTPException(status_code=500, detail=str(e))
