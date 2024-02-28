from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from enum import StrEnum, auto
from sqlalchemy.orm import relationship

from database import Base


class MessageStatus(StrEnum):
    open = auto()
    pending = auto()
    sent = auto()


class NodeTypes(StrEnum):
    start = auto()
    end = auto()
    message = auto()
    condition = auto()


class DBWorkflow(Base):
    __tablename__ = "workflows"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    nodes = relationship("DBNode", back_populates="workflow")
    edges = relationship("DBEdge", back_populates="workflow")


class DBNode(Base):
    __tablename__ = "nodes"

    id = Column(Integer, primary_key=True)
    node_type = Column(Enum(NodeTypes), nullable=False)
    text = Column(String(), nullable=True)
    status = Column(Enum(MessageStatus), nullable=True)
    condition = Column(Enum(MessageStatus), nullable=True)
    workflow_id = Column(Integer, ForeignKey("workflows.id"))

    workflow = relationship(
        "DBWorkflow", back_populates="nodes"
    )


class DBEdge(Base):
    __tablename__ = "edges"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True, default="")
    workflow_id = Column(Integer, ForeignKey("workflows.id"))
    start_node_id = Column(Integer, ForeignKey("nodes.id"))
    end_node_id = Column(Integer, ForeignKey("nodes.id"))

    start_node = relationship("DBNode", foreign_keys=[start_node_id])
    end_node = relationship("DBNode", foreign_keys=[end_node_id])
    workflow = relationship("DBWorkflow", back_populates="edges")
