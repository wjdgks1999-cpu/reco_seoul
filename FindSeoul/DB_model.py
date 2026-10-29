from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    Numeric,
    Text,
)
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class IdTable(Base):
    __tablename__ = 'id_table'
    __table_args__ = {'schema': 'seouldata'}

    original_id = Column(String, primary_key=True, index=True)
    google_id = Column(String,nullable=True)
    original_spot_name = Column(String,nullable=True)
    display_name = Column(String,nullable=True)
    clean_spot_name = Column(String,nullable=True)
    rating = Column(Numeric(2, 1),nullable=True)
    business_status = Column(String,nullable=True)
    user_rating_count = Column(Integer,nullable=True)
    google_maps_uri = Column(String,nullable=True)
    image_url = Column(String,nullable=True)
    content_url_ko = Column(String,nullable=True)
    formatted_address = Column(String,nullable=True)
    latitude = Column(Float,nullable=True)
    longitude = Column(Float,nullable=True)
    content_url_en = Column(String,nullable=True)
    details_ko = Column(Text,nullable=True)
    details_en = Column(Text,nullable=True)