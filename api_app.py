"""
Real Estate Intelligence System - FastAPI Backend
Multi-agent property analysis using Agno framework and Gemini AI
"""

import logging
from datetime import datetime
from typing import List, Dict, Any
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from config import settings
from agents.orchestrator import orchestrator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(
    title="Real Estate Intelligence System",
    description="AI-powered property analysis, valuation, and investment recommendations",
    version="1.0.0"
)

# ============================================================================
# DATA MODELS
# ============================================================================

class PropertyInput(BaseModel):
    """Property input model"""
    address: str
    bedrooms: int
    bathrooms: float
    sqft: int
    age_years: int
    location_type: str = "suburban"  # downtown, urban, suburban, rural
    condition: str = "fair"  # excellent, good, fair, needs_repair, poor
    neighborhood_rating: str = "average"  # excellent, good, average, developing, poor


class AnalysisRequest(BaseModel):
    """Property analysis request"""
    property: PropertyInput


class RealEstateIntelligence:
    """Real Estate Intelligence System with Agno Agents"""

    def __init__(self):
        """Initialize system"""
        logger.info("Initializing Real Estate Intelligence System with Agno Agents")
        self.orchestrator = orchestrator
        logger.info("Real Estate Intelligence System initialized successfully")

    def analyze_property(self, request: AnalysisRequest) -> Dict[str, Any]:
        """
        Analyze property using Agno agents for valuation and investment potential

        Args:
            request: Analysis request with property data

        Returns:
            Complete property analysis
        """
        logger.info(f"Starting analysis for: {request.property.address}")

        # Prepare property data
        property_data = {
            "address": request.property.address,
            "bedrooms": request.property.bedrooms,
            "bathrooms": request.property.bathrooms,
            "sqft": request.property.sqft,
            "age_years": request.property.age_years,
            "location_type": request.property.location_type,
            "condition": request.property.condition,
            "neighborhood_rating": request.property.neighborhood_rating
        }

        try:
            # Use Agno orchestrator with fallback to mock
            analysis = self.orchestrator.analyze_property(property_data)
            logger.info(f"Analysis completed for: {request.property.address}")
            return analysis

        except Exception as e:
            logger.error(f"Analysis failed: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "analysis_summary": {
                    "property_name": request.property.address,
                    "status": "failed"
                }
            }


# ============================================================================
# INITIALIZE APPLICATION
# ============================================================================

intelligence_system = RealEstateIntelligence()


# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "Real Estate Intelligence System",
        "version": "1.0.0",
        "framework": "Agno + Gemini AI",
        "status": "running",
        "endpoints": [
            "/analyze - POST property analysis request",
            "/health - GET health check",
            "/info - GET system information"
        ]
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "Real Estate Intelligence System is running",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/info")
async def system_info():
    """System information endpoint"""
    return {
        "name": "Real Estate Intelligence System",
        "version": "1.0.0",
        "framework": "Agno Framework",
        "model": settings.AGENT_MODEL,
        "database": settings.DB_FILE,
        "currency": settings.CURRENCY,
        "features": [
            "Property Valuation",
            "Market Analysis",
            "Investment Scoring",
            "Risk Assessment",
            "Future Projections"
        ]
    }


@app.post("/analyze")
async def analyze_property(request: AnalysisRequest):
    """
    Analyze property for investment potential

    Args:
        request: Property analysis request

    Returns:
        Complete property analysis
    """
    try:
        analysis = intelligence_system.analyze_property(request)
        return {
            "status": "success",
            "analysis": analysis,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error during analysis: {str(e)}")
        return {
            "status": "error",
            "message": str(e),
            "timestamp": datetime.now().isoformat()
        }


@app.post("/sample-analyze")
async def sample_analyze():
    """
    Run sample property analysis for demonstration

    Returns:
        Sample analysis result
    """
    try:
        sample_property = PropertyInput(
            address="123 Oak Street, Downtown District",
            bedrooms=3,
            bathrooms=2.5,
            sqft=2500,
            age_years=8,
            location_type="urban",
            condition="good",
            neighborhood_rating="good"
        )

        request = AnalysisRequest(property=sample_property)
        analysis = intelligence_system.analyze_property(request)

        return {
            "status": "success",
            "message": "Sample analysis completed",
            "analysis": analysis,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error in sample analysis: {str(e)}")
        return {
            "status": "error",
            "message": str(e)
        }


# ============================================================================
# STARTUP AND SHUTDOWN
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Startup event handler"""
    logger.info("Real Estate Intelligence System starting up")
    logger.info(f"Model: {settings.AGENT_MODEL}")
    logger.info(f"Database: {settings.DB_FILE}")
    logger.info(f"Currency: {settings.CURRENCY}")


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event handler"""
    logger.info("Real Estate Intelligence System shutting down")


# ============================================================================
# RUN APPLICATION
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    import socket

    logger.info("Starting Real Estate Intelligence System")

    # Find available port
    port = settings.API_PORT
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    for attempt in range(5):
        result = sock.connect_ex((settings.API_HOST, port))
        if result != 0:
            break
        port += 1

    sock.close()

    if port != settings.API_PORT:
        logger.warning(f"Port {settings.API_PORT} in use, using port {port}")

    logger.info(f"Server running at http://{settings.API_HOST}:{port}")

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=port,
        reload=settings.DEBUG
    )
