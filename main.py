import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse

# Import router and DB engine
from routes import router
from models import engine, Base

app = FastAPI(title="SmartSpend AI Backend", docs_url="/docs", redoc_url="/redoc")

# Create DB tables if they don't exist
Base.metadata.create_all(bind=engine)

# Include API router (no prefix, routes are defined absolute)

@app.middleware("http")
async def normalize_api_prefix(request: Request, call_next):
    if request.scope.get("path", "").startswith("/api/"):
        request.scope["path"] = request.scope["path"][4:] or "/"
    return await call_next(request)

app.include_router(router)

@app.get("/health", response_model=dict)
async def health() -> dict:
    return {"status": "ok"}

@app.get("/", response_class=HTMLResponse)
async def root() -> HTMLResponse:
    html = """
    <!DOCTYPE html>
    <html lang='en'>
    <head>
        <meta charset='UTF-8'>
        <title>SmartSpend AI</title>
        <style>
            body { background-color: #1e1e2e; color: #f0f4f8; font-family: Arial, Helvetica, sans-serif; padding: 2rem; }
            h1 { color: #37ecba; }
            a { color: #37ecba; text-decoration: none; }
            a:hover { text-decoration: underline; }
            .endpoint { margin: 0.5rem 0; }
            .section { margin-top: 2rem; }
        </style>
    </head>
    <body>
        <h1>SmartSpend AI</h1>
        <p>Transform your spending habits with AI‑powered insights and proactive financial coaching.</p>
        <div class="section">
            <h2>Available API Endpoints</h2>
            <div class="endpoint"><strong>GET</strong> /health – health check</div>
            <div class="endpoint"><strong>POST</strong> /transactions/categorize – AI expense categorization</div>
            <div class="endpoint"><strong>GET</strong> /budget/recommendations – AI budget recommendation</div>
            <div class="endpoint"><strong>GET</strong> /spending/insights – AI spending insights</div>
        </div>
        <div class="section">
            <h2>Tech Stack</h2>
            <ul>
                <li>FastAPI 0.115.0</li>
                <li>PostgreSQL (SQLAlchemy 2.0.35)</li>
                <li>DigitalOcean Serverless Inference (openai‑gpt‑oss‑120b)</li>
                <li>Python 3.12+</li>
            </ul>
        </div>
        <div class="section">
            <a href="/docs">OpenAPI Docs</a> | <a href="/redoc">ReDoc</a>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html, status_code=200)
