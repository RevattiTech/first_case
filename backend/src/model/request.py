import uuid
from datetime import datetime
import sqlalchemy as s

from src.model import Base


class Request(Base):
    __tablename__ = 'requests'

    id = s.Column(s.UUID, primary_key=True, default=uuid.uuid4())
    host = s.Column(s.String, nullable=True)
    execution_time = s.Column(s.String, nullable=True)
    status = s.Column(s.String, nullable=True)
    open_port = s.Column(s.String, nullable=True)
    vulnerabilities = s.Column(s.JSON, nullable=True, default={})
    user_id = s.Column(s.Integer, default=0)

    def __init__(self, id , host, execution_time, status, open_port, vulnerabilities, user_id):
        self.id = id
        self.host = host
        self.execution_time = execution_time
        self.status = status
        self.open_port = open_port
        self.vulnerabilities = vulnerabilities
        self.user_id = user_id

    def to_dict(self):
        return {
            'id': str(self.id),
            'host': self.host,
            'execution_time': self.execution_time,
            'status': self.status,
            'open_port': self.open_port,
            'vulnerabilities': self.vulnerabilities,
            'user_id': self.user_id
        }


class Data(Base):
    __tablename__ = 'data'
    name = s.Column(s.String)
    id = s.Column(s.UUID, primary_key=True, default=uuid.uuid4())
    title = s.Column(s.Text, nullable=True)
    score = s.Column(s.Text, nullable=True)
    href = s.Column(s.Text, nullable=True)
    types = s.Column(s.Text, nullable=True)
    published = s.Column(s.DateTime, default=datetime.now())
    source = s.Column(s.Text, nullable=True)
    language = s.Column(s.Text, nullable=True)

    def to_dict(self):
        return {
            "name": self.name,
            "id": str(self.id),
            "title": self.title,
            "score": self.score,
            "href": self.href,
            "types": self.types,
            "published": self.published.isoformat() if self.published else None,  # ISO format for datetime
            "source": self.source,
            "language": self.language
        }
