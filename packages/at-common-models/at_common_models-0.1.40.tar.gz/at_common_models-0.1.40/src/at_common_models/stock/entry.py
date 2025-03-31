# app/models/user.py
from sqlalchemy import Column, String
from at_common_models.base import BaseModel

class StockEntry(BaseModel):
    __tablename__ = "stock_entries"

    # Core user information
    symbol = Column(String(5), nullable=False, primary_key=True)

    def __str__(self):
        return f"<StockEntry(symbol={self.symbol})>"

    def __repr__(self):
        return f"<StockEntry(symbol={self.symbol})>"
