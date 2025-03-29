# app/models/user.py
from sqlalchemy import Column, String
from at_common_models.base import BaseModel

class StockEntry(BaseModel):
    __tablename__ = "stock_entries"

    # Core user information
    exchange = Column(String(32), nullable=False, primary_key=True)
    symbol = Column(String(255), nullable=False, primary_key=True)

    def __str__(self):
        return f"<StockEntry(exchange={self.exchange}, symbol={self.symbol})>)"

    def __repr__(self):
        return f"<StockEntry(exchange={self.exchange}, symbol={self.symbol})>)"
