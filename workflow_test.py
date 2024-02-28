from src import crud
from src.schemas import WorkflowCreate, NodeCreate, EdgeCreate, MessageNodeCreate, ConditionNodeCreate
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models import DBWorkflow, Base, DBNode
from src.utils import execute_workflow_logic


SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session")
def db_engine():
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture(scope="function")
def db_session(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


class TestWorkflow:
    def setup_method(self, method):
        self.workflow_data_1 = WorkflowCreate(name="test_workflow_1")
        self.workflow_data_2 = WorkflowCreate(name="test_workflow_2")
        self.workflow_data_3 = WorkflowCreate(name="test_workflow_3")

    def test_create_workflow(self, db_session):
        result = crud.create_workflow(db_session, self.workflow_data_1)

        assert isinstance(result, DBWorkflow)
        assert result.name == self.workflow_data_1.name

    def test_get_all_workflows(self, db_session):
        created_workflow_1 = crud.create_workflow(db_session, self.workflow_data_1)
        created_workflow_2 = crud.create_workflow(db_session, self.workflow_data_2)
        created_workflow_3 = crud.create_workflow(db_session, self.workflow_data_3)

        result = crud.get_all_workflows(db_session)

        assert created_workflow_1 in result
        assert created_workflow_2 in result
        assert created_workflow_3 in result

    def test_get_workflow_by_id(self, db_session):
        created_workflow_1 = crud.create_workflow(db_session, self.workflow_data_1)
        created_workflow_2 = crud.create_workflow(db_session, self.workflow_data_2)

        result = crud.get_workflow(db_session, created_workflow_1.id)

        assert created_workflow_1 == result
        assert created_workflow_2 != result
        assert isinstance(result, DBWorkflow)

    def test_update_workflow(self, db_session):
        created_workflow = crud.create_workflow(db_session, self.workflow_data_1)

        updated_workflow = WorkflowCreate(name="test_workflow_2")
        result = crud.update_workflow(db_session, created_workflow.id, updated_workflow)

        assert result.id == created_workflow.id
        assert result.name == "test_workflow_2"

    def test_delete_workflow(self, db_session):
        created_workflow = crud.create_workflow(db_session, self.workflow_data_1)
        deleted_workflow = crud.delete_workflow(db_session, created_workflow.id)
        result = crud.get_all_workflows(db_session)

        assert deleted_workflow not in result


class TestNode:
    def setup_method(self, method):
        self.workflow_data = WorkflowCreate(name="test_workflow")
        self.message_data = {
            "node_type": "message",
            "text": "test message",
            "status": "open",
        }
        self.condition_data = {
            "node_type": "condition",
            "condition": "open",
        }

    def test_create_start_node(self, db_session):
        workflow = crud.create_workflow(db_session, self.workflow_data)
        start_node_data = NodeCreate(node_type="start", workflow_id=workflow.id)

        result = crud.create_node(db_session, start_node_data)

        assert isinstance(result, DBNode)
        assert result.node_type == "start"
        assert result.workflow_id == workflow.id

    def test_create_message_node(self, db_session):
        workflow = crud.create_workflow(db_session, self.workflow_data)

        message_node_data = MessageNodeCreate(**self.message_data, workflow_id=workflow.id)
        result = crud.create_message_node(db_session, message_node_data)

        assert isinstance(result, DBNode)
        assert result.node_type == "message"
        assert result.text == self.message_data["text"]
        assert result.status == self.message_data["status"]
        assert result.workflow_id == workflow.id

    def test_create_condition_node(self, db_session):
        workflow = crud.create_workflow(db_session, self.workflow_data)

        condition_node_data = ConditionNodeCreate(**self.condition_data, workflow_id=workflow.id)
        result = crud.create_condition_node(db_session, condition_node_data)

        assert isinstance(result, DBNode)
        assert result.node_type == self.condition_data["node_type"]
        assert result.condition == self.condition_data["condition"]
        assert result.workflow_id == workflow.id

    def test_create_end_node(self, db_session):
        workflow = crud.create_workflow(db_session, self.workflow_data)
        end_node_data = NodeCreate(node_type="end", workflow_id=workflow.id)

        result = crud.create_node(db_session, end_node_data)

        assert isinstance(result, DBNode)
        assert result.node_type == "end"
        assert result.workflow_id == workflow.id

    def test_get_all_nodes(self, db_session):
        workflow = crud.create_workflow(db_session, self.workflow_data)

        start_node = NodeCreate(node_type="start", workflow_id=workflow.id)
        end_node = NodeCreate(node_type="end", workflow_id=workflow.id)
        message_node = MessageNodeCreate(
            **self.message_data, workflow_id=workflow.id
        )

        start_node = crud.create_node(db_session, start_node)
        end_node = crud.create_node(db_session, end_node)
        message_node = crud.create_message_node(db_session, message_node)

        result = crud.get_all_nodes(db_session)

        assert start_node in result
        assert end_node in result
        assert message_node in result
        assert len(result) == 3

    def test_get_node_by_id(self, db_session):
        workflow = crud.create_workflow(db_session, self.workflow_data)

        start_node_data = NodeCreate(node_type="start", workflow_id=workflow.id)
        end_node_data = NodeCreate(node_type="end", workflow_id=workflow.id)

        start_node = crud.create_node(db_session, start_node_data)
        end_node = crud.create_node(db_session, end_node_data)

        result = crud.get_node_by_id(db_session, start_node.id)

        assert start_node == result
        assert end_node != result
        assert isinstance(result, DBNode)

    def test_update_message_node(self, db_session):
        workflow = crud.create_workflow(db_session, self.workflow_data)

        message_node_data = MessageNodeCreate(**self.message_data, workflow_id=workflow.id)
        message_node = crud.create_message_node(db_session, message_node_data)

        updated_data = {
            "node_type": "message",
            "text": "test",
            "status": "sent",
            "workflow_id": workflow.id
        }
        message_node_data = MessageNodeCreate(**updated_data)
        result = crud.update_message_node(db_session, message_node.id, message_node_data)

        assert isinstance(result, DBNode)
        assert result.node_type == "message"
        assert message_node.id == result.id
        assert result.text == updated_data["text"]
        assert result.status == updated_data["status"]
        assert result.workflow_id == workflow.id

    def test_update_condition_node(self, db_session):
        workflow = crud.create_workflow(db_session, self.workflow_data)

        condition_data = ConditionNodeCreate(**self.condition_data, workflow_id=workflow.id)
        condition_node = crud.create_condition_node(db_session, condition_data)

        updated_data = {
            "node_type": "condition",
            "condition": "sent",
            "workflow_id": workflow.id
        }
        condition_node_data = ConditionNodeCreate(**updated_data)
        result = crud.update_condition_node(db_session, condition_node.id, condition_node_data)

        assert isinstance(result, DBNode)
        assert result.node_type == "condition"
        assert condition_node.id == result.id
        assert result.condition == updated_data["condition"]
        assert result.workflow_id == workflow.id

    def test_delete_node(self, db_session):
        workflow = crud.create_workflow(db_session, self.workflow_data)
        start_node_data = NodeCreate(node_type="start", workflow_id=workflow.id)
        created_node = crud.create_node(db_session, start_node_data)

        crud.delete_node(db_session, created_node.id)
        result = crud.get_all_nodes(db_session)

        assert created_node not in result


class TestEdge:
    def setup_method(self, db_session):
        self.workflow_data = WorkflowCreate(name="test_workflow")
        self.message_data = {
            "node_type": "message",
            "text": "test message",
            "status": "open",
        }
        self.condition_data = {
            "node_type": "condition",
            "condition": "sent",
        }

    def test_create_edge(self, db_session):
        workflow = crud.create_workflow(db_session, self.workflow_data)
        start_node_data = NodeCreate(node_type="start", workflow_id=workflow.id)
        start_node = crud.create_node(db_session, start_node_data)
        message_data = MessageNodeCreate(**self.message_data, workflow_id=workflow.id)
        message_node = crud.create_message_node(db_session, message_data)

        edge_data = {
            "name": "",
            "start_node_id": start_node.id,
            "end_node_id": message_node.id,
            "workflow_id": workflow.id
        }
        edge = EdgeCreate(**edge_data)
        result = crud.create_edge(db_session, edge)

        assert result.name == edge_data["name"]
        assert result.start_node_id == edge_data["start_node_id"]
        assert result.end_node_id == edge_data["end_node_id"]
        assert result.workflow_id == edge_data["workflow_id"]

    def create_test_workflow_1(self, db_session):
        workflow = crud.create_workflow(db_session, self.workflow_data)

        start_node_data = NodeCreate(node_type="start", workflow_id=workflow.id)
        start_node = crud.create_node(db_session, start_node_data)

        message_data = MessageNodeCreate(**self.message_data, workflow_id=workflow.id)
        message_node_1 = crud.create_message_node(db_session, message_data)

        edge_data = {
            "name": "",
            "start_node_id": start_node.id,
            "end_node_id": message_node_1.id,
            "workflow_id": workflow.id
        }
        edge_data_1 = EdgeCreate(**edge_data)
        edge_1 = crud.create_edge(db_session, edge_data_1)

        condition_data = ConditionNodeCreate(**self.condition_data, workflow_id=workflow.id)
        condition_node = crud.create_condition_node(db_session, condition_data)
        edge_data["start_node_id"] = message_node_1.id
        edge_data["end_node_id"] = condition_node.id
        edge_data_2 = EdgeCreate(**edge_data)
        edge_2 = crud.create_edge(db_session, edge_data_2)

        message_node_2 = crud.create_message_node(db_session, message_data)
        edge_data["name"] = "yes"
        edge_data["start_node_id"] = condition_node.id
        edge_data["end_node_id"] = message_node_2.id
        edge_data_3 = EdgeCreate(**edge_data)
        edge_3 = crud.create_edge(db_session, edge_data_3)

        message_node_3 = crud.create_message_node(db_session, message_data)
        edge_data["name"] = "no"
        edge_data["end_node_id"] = message_node_3.id
        edge_data_4 = EdgeCreate(**edge_data)
        edge_4 = crud.create_edge(db_session, edge_data_4)

        message_node_4 = crud.create_message_node(db_session, message_data)
        edge_data["name"] = ""
        edge_data["start_node_id"] = message_node_2.id
        edge_data["end_node_id"] = message_node_4.id
        edge_data_5 = EdgeCreate(**edge_data)
        edge_5 = crud.create_edge(db_session, edge_data_5)

        end_node_data = NodeCreate(node_type="end", workflow_id=workflow.id)
        end_node = crud.create_node(db_session, end_node_data)
        edge_data["start_node_id"] = message_node_4.id
        edge_data["end_node_id"] = end_node.id
        edge_data_6 = EdgeCreate(**edge_data)
        edge_6 = crud.create_edge(db_session, edge_data_6)

        edge_data["start_node_id"] = message_node_3.id
        edge_data_7 = EdgeCreate(**edge_data)
        edge_7 = crud.create_edge(db_session, edge_data_7)

        return workflow

    def create_test_workflow_2(self, db_session):
        workflow = crud.create_workflow(db_session, self.workflow_data)

        start_node_data = NodeCreate(node_type="start", workflow_id=workflow.id)
        start_node = crud.create_node(db_session, start_node_data)

        message_data = MessageNodeCreate(**self.message_data, workflow_id=workflow.id)
        message_node_1 = crud.create_message_node(db_session, message_data)

        edge_data = {
            "name": "",
            "start_node_id": start_node.id,
            "end_node_id": message_node_1.id,
            "workflow_id": workflow.id
        }
        edge_data_1 = EdgeCreate(**edge_data)
        edge_1 = crud.create_edge(db_session, edge_data_1)

        condition_data = ConditionNodeCreate(**self.condition_data, workflow_id=workflow.id)
        condition_node = crud.create_condition_node(db_session, condition_data)
        edge_data["start_node_id"] = message_node_1.id
        edge_data["end_node_id"] = condition_node.id
        edge_data_2 = EdgeCreate(**edge_data)
        edge_2 = crud.create_edge(db_session, edge_data_2)

        message_node_2 = crud.create_message_node(db_session, message_data)
        edge_data["name"] = "yes"
        edge_data["start_node_id"] = condition_node.id
        edge_data["end_node_id"] = message_node_2.id
        edge_data_3 = EdgeCreate(**edge_data)
        edge_3 = crud.create_edge(db_session, edge_data_3)

        condition_data = {
            "node_type": "condition",
            "condition": "open",
            "workflow_id": workflow.id
        }

        condition_data = ConditionNodeCreate(**condition_data)
        condition_node_2 = crud.create_condition_node(db_session, condition_data)
        edge_data["name"] = "no"
        edge_data["end_node_id"] = condition_node_2.id
        edge_data_4 = EdgeCreate(**edge_data)
        edge_4 = crud.create_edge(db_session, edge_data_4)

        message_node_3 = crud.create_message_node(db_session, message_data)
        edge_data["name"] = "yes"
        edge_data["start_node_id"] = condition_node_2.id
        edge_data["end_node_id"] = message_node_3.id
        edge_data_5 = EdgeCreate(**edge_data)
        edge_5 = crud.create_edge(db_session, edge_data_5)

        message_node_4 = crud.create_message_node(db_session, message_data)
        edge_data["name"] = "no"
        edge_data["end_node_id"] = message_node_4.id
        edge_data_6 = EdgeCreate(**edge_data)
        edge_6 = crud.create_edge(db_session, edge_data_6)

        end_node_data = NodeCreate(node_type="end", workflow_id=workflow.id)
        end_node = crud.create_node(db_session, end_node_data)
        edge_data["start_node_id"] = message_node_4.id
        edge_data["end_node_id"] = end_node.id
        edge_data_7 = EdgeCreate(**edge_data)
        edge_7 = crud.create_edge(db_session, edge_data_7)

        edge_data["start_node_id"] = message_node_3.id
        edge_data_8 = EdgeCreate(**edge_data)
        edge_8 = crud.create_edge(db_session, edge_data_8)

        edge_data["start_node_id"] = message_node_2.id
        edge_data_9 = EdgeCreate(**edge_data)
        edge_9 = crud.create_edge(db_session, edge_data_9)

        return workflow

    def test_workflow_1_execute(self, db_session):
        workflow = self.create_test_workflow_1(db_session)
        result = execute_workflow_logic(workflow)

        assert result == [1, 2, 3, 5, 7]

    def test_workflow_2_execute(self, db_session):
        workflow = self.create_test_workflow_2(db_session)
        result = execute_workflow_logic(workflow)

        assert result == [1, 2, 3, 5, 6, 8]
