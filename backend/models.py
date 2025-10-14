from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database import Base


class URL(Base):
    __tablename__ = 'urls'


    ##Primary Key - Auto-incrementing ID (1, 2, 3)
    id = Column(Integer, primary_key=True, index=True)

    ## The Short code - unique identifier for the shortened URL
    short_code = Column(String, unique=True, index=True, nullable=False)

    ## The original long url
    original_url = Column(String, nullable=False)

    ## The timestamp when the shortened url was created
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    ## Click counter to count how many times the url has been clicked
    click_count = Column(Integer, default=0)

