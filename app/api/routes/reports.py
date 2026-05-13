from typing import List
from fastapi import Depends, APIRouter, Query
from app.crud.crud_reports import get_report_metrics, get_volunteer_ranking
from app.schemas.reports import ReportMetrics, VoluntarioRanking
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from datetime import datetime

router = APIRouter()


@router.get("/reports/metrics", response_model=ReportMetrics)
async def metrics(
    mes: int = Query(None, ge=1, le=12),
    ano: int = Query(None, ge=2020),
    session: AsyncSession = Depends(get_db),
):
    agora = datetime.now()
    if not mes:
        mes = agora.month
    if not ano:
        ano = agora.year
    return await get_report_metrics(session, mes, ano)


@router.get("/reports/ranking", response_model=List[VoluntarioRanking])
async def ranking(session: AsyncSession = Depends(get_db)):
    return await get_volunteer_ranking(session)
