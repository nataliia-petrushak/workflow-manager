import networkx as nx
import matplotlib.pyplot as plt

from src.validation import edges_validation
from src.schemas import Workflow


def add_nodes_to_workflow_graph(workflow: Workflow, graph: nx.DiGraph) -> nx.DiGraph:
    """Add nodes from the workflow to the graph."""

    for node in workflow.nodes:
        if node.node_type == "message":
            graph.add_node(node.id, node_type=node.node_type, text=node.text, status=node.status)
        elif node.node_type == "condition":
            graph.add_node(node.id, node_type=node.node_type, condition=node.condition)
        else:
            graph.add_node(node.id, node_type=node.node_type)
    return graph


def add_edges_to_workflow_graph(workflow: Workflow, graph: nx.DiGraph) -> nx.DiGraph:
    """Add edges from the workflow to the graph."""

    for edge in workflow.edges:
        edges_validation(graph, edge.start_node_id, edge.end_node_id)
        graph.add_edge(edge.start_node_id, edge.end_node_id, name=edge.name)

    return graph


def construct_workflow_graph(workflow: Workflow) -> nx.DiGraph:
    """Construct the workflow graph from the given Workflow object."""

    graph = nx.DiGraph()
    graph = add_nodes_to_workflow_graph(workflow, graph)
    graph = add_edges_to_workflow_graph(workflow, graph)
    return graph


def find_start_and_end_nodes(graph: nx.DiGraph) -> dict:
    """Find the start and end nodes by looking for a node type"""

    result = {"start": None, "end": None}

    for node in graph.nodes:
        if graph.nodes[node]["node_type"] == "start":
            result["start"] = node
        if graph.nodes[node]["node_type"] == "end":
            result["end"] = node

    return result


def choose_next_node(
        graph: nx.DiGraph, current_node: int, condition_match: bool = True
):
    """Choose the next node based on the current node and condition."""

    outgoing_edges = graph.out_edges(current_node, data=True)

    for _, next_node, edge_data in outgoing_edges:
        if graph.nodes[current_node]["node_type"] == "condition":
            if ((condition_match and edge_data.get("name") == "yes")
                    or (not condition_match and edge_data.get("name") == "no")):
                return next_node
        else:
            return next_node


def create_path(graph: nx.DiGraph, start: int, end: int) -> list:
    """Create a path through the graph from start to end."""

    result = []
    node = start
    message = None

    while node <= end:
        result.append(node)

        if graph.nodes[node]["node_type"] == "message":
            message = graph.nodes[node]
            node = choose_next_node(graph, node)
        elif graph.nodes[node]["node_type"] == "condition":
            if message["status"] == graph.nodes[node]["condition"]:
                next_node = choose_next_node(graph, node)
            else:
                next_node = choose_next_node(graph, node, False)
            node = next_node
        else:
            node += 1

    return result


def execute_workflow_logic(workflow: Workflow) -> list:
    """Execute the workflow logic and return the final path."""

    graph = construct_workflow_graph(workflow)

    start_and_end = find_start_and_end_nodes(graph)

    final_path = create_path(graph, start_and_end["start"], start_and_end["end"])

    pict = nx.spring_layout(graph)  # Layout for the nodes
    nx.draw(graph, pict, with_labels=True, node_size=700, node_color="skyblue")

    # Display the graph
    plt.show()

    return final_path
