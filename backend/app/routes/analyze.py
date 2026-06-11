from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.models.analysis import AnalysisRequest, AnalysisResponse
from app.models.market_pulse import MarketPulse
from app.models.opportunity import Opportunity
from app.services.analysis_service import AnalysisService, get_analysis_service

router = APIRouter(
    prefix="",
    tags=["Analysis & Intelligence"]
)

@router.post(
    "/analyze",
    response_model=AnalysisResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Trigger topic analysis",
    description="Collects evidence, processes signals, evaluates opportunities/threats, and updates the platform's state."
)
async def analyze_topic(
    request: AnalysisRequest,
    service: AnalysisService = Depends(get_analysis_service)
):
    try:
        response = await service.analyze_topic(request)
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during analysis: {str(e)}"
        )

@router.get(
    "/market-pulse",
    response_model=MarketPulse,
    status_code=status.HTTP_200_OK,
    summary="Get current Market Pulse status",
    description="Returns the aggregated status of detected signals, top opportunities, and top threats."
)
async def get_market_pulse(
    service: AnalysisService = Depends(get_analysis_service)
):
    try:
        pulse = await service.generate_market_pulse()
        return pulse
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate market pulse: {str(e)}"
        )

@router.get(
    "/opportunities",
    response_model=List[Opportunity],
    status_code=status.HTTP_200_OK,
    summary="List identified Opportunities",
    description="Returns a list of all opportunities currently identified from historical/recent analysis cycles."
)
async def get_opportunities(
    service: AnalysisService = Depends(get_analysis_service)
):
    try:
        opps = await service.get_opportunities()
        return opps
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch opportunities: {str(e)}"
        )
