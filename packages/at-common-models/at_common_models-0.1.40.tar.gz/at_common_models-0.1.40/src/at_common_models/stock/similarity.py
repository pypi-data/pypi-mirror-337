# app/models/user.py
from sqlalchemy import Column, String, Float
from at_common_models.base import BaseModel

class StockSimilarity(BaseModel):
    __tablename__ = "stock_similarities"

    # Core user information
    symbol_1 = Column(String(5), nullable=False, primary_key=True, index=True)
    symbol_2 = Column(String(5), nullable=False, primary_key=True, index=True)
    similarity_description = Column(Float, nullable=False)
    similarity_market_cap = Column(Float, nullable=False)
    
    def __str__(self):
        return f"<StockSimilarity(symbol_1={self.symbol_1}, symbol_2={self.symbol_2}, similarity_description={self.similarity_description}, similarity_market_cap={self.similarity_market_cap})>"

    def __repr__(self):
        return f"<StockSimilarity(symbol_1={self.symbol_1}, symbol_2={self.symbol_2}, similarity_description={self.similarity_description}, similarity_market_cap={self.similarity_market_cap})>"
