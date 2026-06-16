from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.pagination import PaginationParams


class BaseRepository:
    def __init__(self, model):
        self.model = model

    def list(self, db: Session, filters: dict, pagination: PaginationParams):
        query = select(self.model).filter_by(**filters).offset(pagination.offset).limit(pagination.limit)
        rows = db.execute(query).scalars().all()
        total = db.query(self.model).filter_by(**filters).count()
        return rows, {"page": pagination.page, "limit": pagination.limit, "total": total}

    def get(self, db: Session, filters: dict, record_id: str):
        return db.query(self.model).filter_by(**filters, id=record_id).first()

    def create(self, db: Session, payload: dict):
        record = self.model(**payload)
        db.add(record)
        db.flush()
        return record

    def update(self, db: Session, record, payload: dict):
        for key, value in payload.items():
            setattr(record, key, value)
        db.flush()
        return record
