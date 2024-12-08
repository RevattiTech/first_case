import uuid
import sqlalchemy as s
from src.model import Base


class User(Base):
    __tablename__ = 'users'

    id = s.Column(s.UUID, primary_key=True, default=uuid.uuid4())
    first_name = s.Column(s.String, nullable=True)
    last_name = s.Column(s.String, nullable=True)
    username = s.Column(s.String, nullable=True)
    chat_id = s.Column(s.Integer, default=0)
    photo_url = s.Column(s.String, nullable=True)
