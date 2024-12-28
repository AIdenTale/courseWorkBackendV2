from sqlalchemy import create_engine, func
from sqlalchemy.orm import declarative_base, sessionmaker

from reportsService.models import ReportOrder
from reportsService.schemas import ReportAggregatedStatuses, ReportAggregatedStatusesData

SQLALCHEMY_DATABASE_URL = "postgresql://root:mypassword@213.171.25.1:5432/reports"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_aggregated_statuses_data():
    session = SessionLocal()
    orders = (((session.query(ReportOrder.order_status, func.count().label('status_count'))
             .filter(ReportOrder.order_status.in_(['Pending', 'Cancelled', 'Completed'])))
             .group_by(ReportOrder.order_status))
             .all())

    ordersAggregated = []
    for order in orders:
        ordersAggregated.append(ReportAggregatedStatuses(
            state=order[0],
            count=order[1],
        ))

    data = ReportAggregatedStatusesData(data=ordersAggregated)

    return data