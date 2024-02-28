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
    workflow_id: int


class NodeCreate(NodeBase):
    pass


class Node(NodeBase):
    id: int
    workflow: Workflow

    class Config:
        orm_mode = True


class MessageNodeBase(NodeBase):
    text: str
    status: MessageStatus


class MessageNodeCreate(MessageNodeBase):
    pass


class MessageNode(MessageNodeBase):
    id: int

    class Config:
        orm_mode = True


class ConditionNodeBase(NodeBase):
    condition: MessageStatus


class ConditionNodeCreate(ConditionNodeBase):
    pass


class ConditionNode(ConditionNodeBase):
    id: int

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
