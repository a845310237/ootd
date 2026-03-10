"""FastAPI application for OOTD (Outfit of the Day) application."""
from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.deps import get_db, get_current_user
from app.models.user import User
from app.api.v1 import api_router
from app.utils.helpers import register_helpers
import os

# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure upload directory exists
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Template configuration
templates = Jinja2Templates(directory="app/templates")
register_helpers(templates.env)  # Register custom helper functions

# Register API routes
app.include_router(api_router, prefix="/api/v1")


# ========================================
# Page Routes
# ========================================

@app.get("/")
async def index(request: Request):
    """Home page."""
    # Try to get current user, but don't require authentication
    try:
        from app.core.security import decode_access_token

        token = request.cookies.get("access_token")
        if token:
            payload = decode_access_token(token)
            if payload:
                db: Session = next(get_db())
                user = db.query(User).filter(User.email == payload.get("sub")).first()
                if user:
                    return RedirectResponse(url="/dashboard", status_code=302)
    except:
        pass

    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/auth/login")
async def login_page(request: Request):
    """Login page."""
    # Redirect to dashboard if already logged in
    try:
        from app.core.security import decode_access_token

        token = request.cookies.get("access_token")
        if token:
            payload = decode_access_token(token)
            if payload:
                return RedirectResponse(url="/dashboard", status_code=302)
    except:
        pass

    return templates.TemplateResponse("auth/login.html", {"request": request})


@app.get("/auth/register")
async def register_page(request: Request):
    """Registration page."""
    return templates.TemplateResponse("auth/register.html", {"request": request})


@app.post("/auth/logout")
async def logout_page():
    """Logout endpoint."""
    response = RedirectResponse(url="/auth/login", status_code=303)
    response.delete_cookie("access_token")
    return response


# ========================================
# Dashboard Routes
# ========================================

@app.get("/dashboard")
async def dashboard_index(request: Request):
    """Dashboard home page."""
    return templates.TemplateResponse(
        "dashboard/index.html",
        {"request": request}
    )


@app.get("/dashboard/profile")
async def profile_page(request: Request):
    """User profile page."""
    return templates.TemplateResponse(
        "dashboard/profile.html",
        {"request": request}
    )


@app.get("/dashboard/wardrobe")
async def wardrobe_page(request: Request):
    """Wardrobe management page."""
    return templates.TemplateResponse(
        "dashboard/wardrobe.html",
        {"request": request}
    )


@app.get("/dashboard/outfits")
async def outfits_page(request: Request):
    """Outfits management page."""
    return templates.TemplateResponse(
        "dashboard/outfits.html",
        {"request": request}
    )


# ========================================
# Health Check
# ========================================

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "debug": settings.DEBUG
    }


# ========================================
# Error Handlers
# ========================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions."""
    if request.headers.get("accept", "").startswith("application/json"):
        # Return JSON for API requests
        from fastapi.responses import JSONResponse
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail}
        )
    else:
        # Return HTML for page requests
        return templates.TemplateResponse(
            "error.html",
            {
                "request": request,
                "status_code": exc.status_code,
                "detail": exc.detail
            },
            status_code=exc.status_code
        )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions."""
    import logging

    logging.error(f"Unhandled exception: {exc}", exc_info=True)

    if request.headers.get("accept", "").startswith("application/json"):
        # Return JSON for API requests
        from fastapi.responses import JSONResponse
        return JSONResponse(
            status_code=500,
            content={"detail": "内部服务器错误"}
        )
    else:
        # Return HTML for page requests
        return templates.TemplateResponse(
            "error.html",
            {
                "request": request,
                "status_code": 500,
                "detail": "内部服务器错误"
            },
            status_code=500
        )


# ========================================
# Startup Event
# ========================================

@app.on_event("startup")
async def startup_event():
    """Run application startup tasks."""
    import logging

    logging.info(f"Starting {settings.APP_NAME}")
    logging.info(f"Debug mode: {settings.DEBUG}")

    # Initialize database tables
    try:
        from app.models.database import init_db, engine
        init_db()
        logging.info("Database tables created successfully")

        # Test database connection
        with engine.connect() as conn:
            logging.info("Database connection successful")
    except Exception as e:
        logging.error(f"Database initialization failed: {e}")


# ========================================
# Main Entry Point
# ========================================

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
