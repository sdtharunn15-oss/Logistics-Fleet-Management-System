from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.tracking import (
    TrackingCreate,
    TrackingResponse,
)
from app.services.tracking_service import (
    TrackingService,
)


router = APIRouter(
    prefix="/tracking",
    tags=["Tracking"],
)


@router.get(
    "",
    response_model=list[TrackingResponse],
)
def get_tracking_records(
    db: Session = Depends(get_db),
):
    return TrackingService.get_tracking_records(db)


@router.post(
    "",
    response_model=TrackingResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_tracking_record(
    tracking_data: TrackingCreate,
    db: Session = Depends(get_db),
):
    try:
        return TrackingService.create_tracking_record(
            db,
            tracking_data,
        )

    except LookupError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )


@router.get(
    "/{tracking_id}",
    response_model=TrackingResponse,
)
def get_tracking_record(
    tracking_id: int,
    db: Session = Depends(get_db),
):
    try:
        return TrackingService.get_tracking_record(
            db,
            tracking_id,
        )

    except LookupError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )


@router.delete("/{tracking_id}")
def delete_tracking_record(
    tracking_id: int,
    db: Session = Depends(get_db),
):
    try:
        TrackingService.delete_tracking_record(
            db,
            tracking_id,
        )

        return {
            "message": (
                "Tracking record deleted successfully"
            )
        }

    except LookupError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )