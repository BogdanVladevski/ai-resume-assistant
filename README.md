# AI Resume Assistant

An AI powered REST API built with **Python, FastAPI, LangChain, and OpenAI** that helps users improve resumes, generate cover letters, find missing skills, and rewrite resume bullet points.

This project was created to learn **LLM applications, prompt engineering, API development, and structured AI outputs**.

---

## Features

* Tailor a resume to a job description
* Generate cover letters
* Analyze missing skills between a resume and a job posting
* Improve weak resume bullet points
* JSON API responses using FastAPI

---

## Tech Stack

* **Python 3.12**
* **FastAPI**
* **LangChain**
* **OpenAI API (GPT-4o)**
* **Pydantic**
* **Docker**

---

## How It Works

1. A user sends a request to a FastAPI endpoint.
2. LangChain formats a prompt based on the request.
3. OpenAI generates a response.
4. The response is validated using Pydantic models.
5. FastAPI returns a structured JSON response.

---

## Installation

### Run Locally

```bash
git clone https://github.com/yourname/ai-resume-assistant.git

cd ai-resume-assistant

pip install -r requirements.txt
```

Create a `.env` file:

```env
OPENAI_API_KEY=your_api_key
```

Run the API:

```bash
uvicorn app.main:app --reload
```

Open Swagger docs:

```txt
http://localhost:8000/docs
```

---

## Example Endpoint

### Resume Tailoring

POST `/resume/tailor`

Request:

```json
{
  "resume_text": "Python developer with FastAPI experience",
  "job_description": "Backend Engineer using Python and Docker"
}
```

Response:

```json
{
  "tailored_resume": "...",
  "match_score": 78
}
```

---

## Prompt Engineering

This project uses custom prompts to:

* match resume keywords to job descriptions
* adjust tone for different outputs
* generate structured responses
* improve ATS alignment

---

## Docker

Build:

```bash
docker build -t ai-resume-assistant .
```

Run:

```bash
docker run -p 8000:8000 ai-resume-assistant
```

---

## What I Learned

Through this project I practiced:

* LangChain workflows
* Prompt engineering
* FastAPI development
* REST API design
* Structured outputs using Pydantic
* Docker basics
* Working with OpenAI APIs

---

## Future Improvements

* PDF resume uploads
* Authentication
* Response streaming
* Caching
* Deployment to Azure / AWS
