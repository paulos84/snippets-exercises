from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///:memory:', echo=True)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base(bind=engine)


class Parent(Base):
    __tablename__ = 'parent'
    id = Column(Integer, primary_key=True)
    # children = relationship("Child")
    children = relationship("Child", back_populates="parent")

class Child(Base):
    __tablename__ = 'child'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('parent.id'))
    # parent = relationship("Parent")
    parent = relationship("Parent", back_populates="children")

Base.metadata.create_all()

parent = Parent(id=1)
child = Child(id=5)
child2 = Child(id=7)

child.parent = parent
parent.children.append(child2)

print([a.id for a in parent.children])
print(child.parent.id)

session.add(child)
session.commit()

print(session.query(Child).all())

from sqlalchemy import inspect

insp = inspect(Child)
print(list(insp.columns))