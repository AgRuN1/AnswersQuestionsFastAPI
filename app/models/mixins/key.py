from sqlalchemy import Column, Integer

class IdMixin:
    id = Column(Integer, primary_key=True, autoincrement=True)