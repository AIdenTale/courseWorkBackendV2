from typing import Tuple, Any
import psycopg2

from ReportKafkaConsumer.models.db import ReportModel

conn = psycopg2.connect(
    "dbname=reports user=service password=hsdg4731jhpasklaksd host=88.218.66.164 port=5432"
)

def execute_sql_query(query: str, args: Tuple[Any, ...] | None = None, must_commit: bool | None = None) -> Any:
    cur = conn.cursor()
    cur.execute(query, args)

    if must_commit:
        conn.commit()

        if "RETURNING" in query:
            records = cur.fetchall()
            return records

        return

    records = cur.fetchall()
    return records

def delete_completed_report(report: ReportModel):
    execute_sql_query(
        "DELETE FROM public.reports WHERE id = %s",
        (report.id,),
        True
    )
    print(f"Report with ID {report.id} deleted successfully.")
