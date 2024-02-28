from sqlalchemy.orm import Session

import models
from schemas import (
    NodeCreate,
    MessageNodeCreate,
    ConditionNodeCreate,
    EdgeCreate,
    WorkflowCreate
)


def create_workflow(db: Session, workflow: WorkflowCreate) -> models.DBWorkflow:
    db_workflow = models.DBWorkflow(name=workflow.name)
    db.add(db_workflow)
    db.commit()
    db.refresh(db_workflow)

    return db_workflow


def get_workflow(db: Session, workflow_id: int) -> models.DBWorkflow:
    return db.query(models.DBWorkflow).filter(
        models.DBWorkflow.id == workflow_id
    ).first()


def get_all_workflows(db: Session) -> list[models.DBWorkflow]:
    return db.query(models.DBWorkflow).all()


def update_workflow(
        db: Session, workflow_id: int, workflow: WorkflowCreate
) -> models.DBWorkflow:
    db_workflow = get_workflow(db, workflow_id)
    db_workflow.name = workflow.name
    db.commit()
    db.refresh(db_workflow)

    return db_workflow


def delete_workflow(db: Session, workflow_id: int) -> None:
    db_workflow = get_workflow(db, workflow_id)
    db.delete(db_workflow)
    db.commit()


def create_node(db: Session, node: NodeCreate) -> models.DBNode:
    db_node = models.DBNode(
        node_type=node.node_type
    )
    db.add(db_node)
    db.commit()
    db.refresh(db_node)

    return db_node


def get_all_nodes(db: Session) -> list[models.DBNode]:
    return db.query(models.DBNode).all()


def get_node(db: Session, node_id: int) -> models.DBNode:
    return db.query(models.DBNode).filter(models.DBNode.id == node_id).first()


def delete_node(db: Session, node_id: int) -> None:
    node = db.query(models.DBNode).filter(models.DBNode.id == node_id).first()
    db.delete(node)
    db.commit()


def create_message_node(
        db: Session, message_node: MessageNodeCreate
) -> models.DBMessageNode:
    db_message_node = models.DBMessageNode(
        node_type=message_node.node_type,
        text=message_node.text,
        status=message_node.status
    )
    db.add(db_message_node)
    db.commit()
    db.refresh(db_message_node)

    return db_message_node


def update_node(
        db: Session, node_id: int, data: MessageNodeCreate | ConditionNodeCreate
) -> models.DBMessageNode | ConditionNodeCreate:
    node = get_node(db, node_id=node_id)
    for var, value in vars(data).items():
        setattr(node, var, value) if value else None
    db.commit()
    db.refresh(node)
    return node


def create_condition_node(
        db: Session, condition_node: ConditionNodeCreate
) -> models.DBConditionNode:
    db_condition_node = models.DBConditionNode(
        node_type=condition_node.node_type,
        condition=condition_node.condition,
    )
    db.add(db_condition_node)
    db.commit()
    db.refresh(db_condition_node)

    return db_condition_node


def create_edge(db: Session, edge: EdgeCreate) -> models.DBEdge:
    db_edge = models.DBEdge(
        name=edge.name,
        start_node_id=edge.start_node_id,
        end_node_id=edge.end_node_id
    )
    db.add(db_edge)
    db.commit()
    db.refresh(db_edge)

    return db_edge


def delete_edge(db: Session, edge_id: int) -> None:
    edge = db.query(models.DBEdge).filter(models.DBEdge.id == edge_id).first()
    db.delete(edge)
    db.commit()
