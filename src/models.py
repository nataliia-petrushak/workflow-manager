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
    message = auto()
    condition = auto()
    end = auto()


class DBWorkflow(Base):
    __tablename__ = "workflows"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class DBNode(Base):
    __tablename__ = "nodes"

    id = Column(Integer, primary_key=True)
    node_type = Column(Enum(NodeTypes), nullable=False)
    workflow_id = Column(Integer, ForeignKey("workflows"))
    workflow = relationship("Workflow", back_populates="nodes")


class DBMessageNode(DBNode):
    __tablename__ = "message_nodes"

    id = Column(Integer, ForeignKey("node.id"), primary_key=True)
    text = Column(String(), nullable=False)
    status = Column(Enum(MessageStatus), nullable=False)


class DBConditionNode(DBNode):
    __tablename__ = "condition_nodes"

    id = Column(Integer, ForeignKey("node.id"), primary_key=True)
    condition = Column(Enum(MessageStatus), nullable=False)


class DBEdge(Base):
    __tablename__ = "edges"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True, default="")
    workflow_id = Column(Integer, ForeignKey("workflows"))
    start_node_id = Column(Integer, ForeignKey("node.id"))
    end_node_id = Column(Integer, ForeignKey("node.id"))

    start_node = relationship("DBNode", foreign_keys=[start_node_id])
    end_node = relationship("DBNode", foreign_keys=[end_node_id])
    workflow = relationship("Workflow", back_populates="edges")
