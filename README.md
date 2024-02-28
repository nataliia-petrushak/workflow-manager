# Workflow Management API
This API provides functionality for managing workflows using graph concepts. It allows users to create four types of nodes and includes features for managing graphs, implementing algorithms for determining paths from the initial to the final node.

### Description
The Workflow Management API is designed to facilitate the creation and management of workflows. It utilizes the FastAPI framework along with Pydantic for handling web requests and integrates with the NetworkX library for graph management. The API includes endpoints for creating, updating, and deleting workflows, as well as for configuring and initiating workflows.

### API Requirements
* Workflow CRUD: 
Endpoints for creating, updating, and deleting workflows.
* Node Creation: 
Endpoint for adding new nodes (Start, Message, Condition, End) to a workflow.
* Node Configuration: 
Ability to modify parameters for nodes or delete nodes.
* Workflow Execution: 
Endpoint for initializing and executing selected workflows, returning a detailed path from Start to End Node or an error if it's impossible to reach the end node along with a description of the reason.

### Technologies Used
- FastAPI: A modern, fast (high-performance), web framework for building APIs with Python.
- Pydantic: Data validation and settings management using Python type hints.
- NetworkX: A Python library for creating, manipulating, and studying complex networks and graphs.

### Installation and Setup

Clone this repository:

```git clone https://github.com/nataliia-petrushak/workflow-manager.git```

Install the required dependencies using pip:

``` pip install -r requirements.txt```

Run the API using uvicorn: 

``` uvicorn main:app --reload ```

Create a database using alembic:

```alembic upgrade head```

Access the API documentation at http://localhost:8000/docs.

## Usage
1. Create a new workflow using the provided endpoints.
2. Add nodes to the workflow specifying their types and configurations.
3. Configure the nodes as needed.
4. Initiate and execute the workflow to observe the detailed path from the start to end node (in the end you will get a picture as you can see below)

<br><br>
<h5>Here you can see all the graph</h5>
<img width="636" alt="Screenshot 2024-02-28 at 23 59 11" src="https://github.com/nataliia-petrushak/workflow-manager/assets/87134904/b0960013-bfd7-46bc-b38b-7aedcdef89c6">
<br><br>
<h5>And in this picture you can see the shortest path due to conditions</h5>
<img width="1440" alt="Screenshot 2024-02-28 at 23 59 36" src="https://github.com/nataliia-petrushak/workflow-manager/assets/87134904/84e57179-ffbe-45c4-8d8c-96a680fca22c">
<br><br>
<h5>Here you can see how the docs look like</h5>
<img width="1430" alt="Screenshot 2024-02-28 at 23 58 53" src="https://github.com/nataliia-petrushak/workflow-manager/assets/87134904/653b2dee-4c41-4b65-bc16-d6b3b20672f1">
