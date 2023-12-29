import enum
import os

from databases import Database
from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData, Table, Integer, Column, String, ForeignKey, DateTime, Enum

load_dotenv()

DATABASE_URI = os.getenv('DATABASE_URI')

engine = create_engine(DATABASE_URI)
metadata = MetaData()


class ReviewStatus(str, enum.Enum):
    pending = 'pending'
    approved = 'approved'
    rejected = 'rejected'
    hidden = 'hidden'


review = Table(
    'review',
    metadata,
    Column('id_review', Integer, primary_key=True),
    Column('review_text', String, nullable=False),
    Column('rating', Integer, nullable=False),
    Column('created_at', DateTime, nullable=False),
    Column('review_status', Enum(ReviewStatus), default=ReviewStatus.pending),
    Column('fk_user', ForeignKey('user.id_user'), nullable=False),
    Column('fk_attraction', ForeignKey('attraction.id_attraction'), nullable=False)
)

user = Table(
    'user',
    metadata,
    Column('id_user', Integer, primary_key=True),
    Column('email', String, nullable=False),
    Column('first_name', String),
    Column('last_name', String)
)

database = Database(DATABASE_URI)
