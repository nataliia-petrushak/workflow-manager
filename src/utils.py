import networkx as nx
from validation import edges_validation
from schemas import Workflow


def add_nodes_to_workflow_graph(workflow: Workflow, graph: nx.DiGraph) -> nx.DiGraph:
    for node in workflow.nodes:
        if node.node_type == "message":
            graph.add_node(node.id, node_type=node.type, message=node.message, status=node.status)
        elif node.node_type == "condition":
            graph.add_node(node.id, node_type=node.type, condition=node.condition)
        else:
            graph.add_node(node.id, node_type=node)
    return graph


def add_edges_to_workflow_graph(workflow: Workflow, graph: nx.DiGraph) -> nx.DiGraph:
    for edge in workflow.edges:
        edges_validation(graph, edge.start_node_id, edge.end_node_id)
        graph.add_edge(edge.start_node_id, edge.end_node_id, name=edge.name)

    return graph


def construct_workflow_graph(workflow: Workflow) -> nx.DiGraph:
    empty_graph = nx.DiGraph()
    graph_with_nodes = add_nodes_to_workflow_graph(workflow, empty_graph)
    graph = add_edges_to_workflow_graph(workflow, graph_with_nodes)
    return graph


def find_start_and_end_nodes(graph: nx.DiGraph) -> dict:
    """Find the start and end nodes by looking for a node type"""
    result = {"start": None, "end": None}

    for node in graph.nodes:
        if node.node_type == "start":
            result["start"] = node
        if node.node_type == "end":
            result["end"] = node

    return result


def choose_next_node(graph: nx.DiGraph, current_node, condition_match: bool):
    outgoing_edges = graph.out_edges(current_node, data=True)

    for _, next_node, edge_data in outgoing_edges:
        if ((condition_match and edge_data.get("name") == "yes")
                or (not condition_match and edge_data.get("name") == "no")):
            return next_node


def create_path(graph: nx.DiGraph, shortest_path):
    result = shortest_path.copy()
    messages = []

    for i, node in enumerate(shortest_path[:-1]):
        if node.node_type == "message":
            messages.append(node)
        if node.node_type == "condition":
            if messages[-1].status == node.condition:
                next_node = choose_next_node(graph, node, True)
            else:
                next_node = choose_next_node(graph, node, False)
            if next_node is not None:
                result[i + 1] = next_node
    return result


def execute_workflow_logic(workflow):
    graph = construct_workflow_graph(workflow)

    start_and_end = find_start_and_end_nodes(graph)

    shortest_path = nx.shortest_path(
        graph, source=start_and_end["start"], target=start_and_end["end"]
    )
    final_path = create_path(graph, shortest_path)

    return final_path
