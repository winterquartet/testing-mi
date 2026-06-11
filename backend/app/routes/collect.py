from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.models.evidence import Evidence
from app.models.analysis import CollectionRequest
from app.services.analysis_service import AnalysisService, get_analysis_service

router = APIRouter(
    prefix="",
    tags=["Collection"]
)

@router.post(
    "/collect",
    response_model=List[Evidence],
    status_code=status.HTTP_200_OK,
    summary="Trigger raw evidence collection",
    description="Activates specific collectors to gather evidence related to a search query or competitor name."
)
async def collect_evidence(
    request: CollectionRequest,
    service: AnalysisService = Depends(get_analysis_service)
):
    try:
        if not request.sources:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="At least one source must be provided in the request."
            )
        
        evidence = await service.collect_evidence(request.query, request.sources)
        return evidence
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during evidence collection: {str(e)}"
        )
