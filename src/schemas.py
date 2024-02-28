from pydantic import BaseModel
from src.models import MessageStatus


class WorkflowBase(BaseModel):
    name: str


class WorkflowCreate(WorkflowBase):
    pass


class Workflow(WorkflowBase):
    id: int

    class Config:
        orm_mode = True


class NodeBase(BaseModel):
    node_type: str


class NodeCreate(NodeBase):
    workflow_id: int


class Node(NodeBase):
    id: int
    workflow: Workflow

    class Config:
        orm_mode = True


class MessageNodeBase(BaseModel):
    text: str
    node_type: str = "message"
    status: MessageStatus


class MessageNodeCreate(MessageNodeBase):
    workflow_id: int


class MessageNode(MessageNodeBase):
    id: int
    workflow: Workflow

    class Config:
        orm_mode = True


class ConditionNodeBase(BaseModel):
    node_type: str = "condition"
    condition: MessageStatus


class ConditionNodeCreate(ConditionNodeBase):
    workflow_id: int


class ConditionNode(ConditionNodeBase):
    id: int
    workflow: Workflow

    class Config:
        orm_mode = True


class EdgeBase(BaseModel):
    name: str | None
    start_node_id: int
    end_node_id: int


class EdgeCreate(EdgeBase):
    workflow_id: int


class Edge(EdgeBase):
    id: int
    workflow: Workflow

    class Config:
        orm_mode = True
