from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.analyze import router as analyze_router
from app.routes.collect import router as collect_router

# Initialize the FastAPI app with meta info
app = FastAPI(
    title="Autonomous Market Intelligence Platform API",
    description="Production-ready FastAPI backend for collecting market updates, detecting signals, and evaluating opportunities/threats.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for frontend flexibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the routes
app.include_router(analyze_router)
app.include_router(collect_router)

@app.get("/", tags=["Health"])
async def health_check():
    """
    Health check endpoint verifying the backend is running and operational.
    """
    return {
        "status": "healthy",
        "service": "Autonomous Market Intelligence Platform API",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    # Allow running directly via 'python app/main.py' for convenience
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
