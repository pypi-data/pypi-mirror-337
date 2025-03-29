# app/models/user.py
from sqlalchemy import Column, String, DateTime
from at_common_models.base import BaseModel

class StockCompanyProfile(BaseModel):
    __tablename__ = "stock_company_profiles"

    symbol = Column(String(5), nullable=False, primary_key=True)
    name = Column(String(255), nullable=False)
    currency = Column(String(3), nullable=False)
    cik = Column(String(10), nullable=False)
    isin = Column(String(12), nullable=False)
    cusip = Column(String(9), nullable=False)
    exchange_full_name = Column(String(255), nullable=False)
    exchange = Column(String(16), nullable=False)
    sector = Column(String(255), nullable=True)
    industry = Column(String(255), nullable=True)
    website = Column(String(2083), nullable=True)
    description = Column(String(2083), nullable=True)
    ceo = Column(String(255), nullable=True)
    phone = Column(String(255), nullable=True)
    address = Column(String(255), nullable=True)
    country = Column(String(255), nullable=True)
    city = Column(String(255), nullable=True)
    state = Column(String(255), nullable=True)
    zip = Column(String(255), nullable=True)
    image = Column(String(2083), nullable=True)
    ipo_date = Column(DateTime, nullable=True)

    def __str__(self):
        return f"<StockCompanyProfile(exchange={self.exchange}, symbol={self.symbol})>"

    def __repr__(self):
        return f"<StockCompanyProfile(exchange={self.exchange}, symbol={self.symbol})>"
