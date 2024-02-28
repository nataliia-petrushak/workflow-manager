from fastapi import HTTPException


def edges_validation(graph, start_node_id: int, end_node_id: int) -> None:

    # Count the number of successors of the start node
    successors = len(list(graph.successors(start_node_id)))

    # Validate the outgoing edges of the start node
    if graph.nodes[start_node_id]["node_type"] == "start" and successors == 1:
        raise HTTPException(status_code=400, detail="Start node can only have one outgoing edge.")

    # Raise an exception if the start node has incoming edges
    elif graph.nodes[end_node_id]["node_type"] == "start":
        raise HTTPException(
            status_code=400, detail="Start node can't have incoming edge."
        )

    # Raise an exception if a message node has more than one outgoing edge
    elif graph.nodes[start_node_id]["node_type"] == "message" and successors == 1:
        raise HTTPException(
            status_code=400, detail="Message node can only have one outgoing edge."
        )

    # Raise an exception if a condition node has more than two outgoing edges
    elif graph.nodes[start_node_id]["node_type"] == "condition" and successors == 2:
        raise HTTPException(
            status_code=400, detail="Condition node can only have 2 outgoing edges."
        )

    # Raise an exception if the end node has outgoing edges
    elif graph.nodes[start_node_id]["node_type"] == "end":
        raise HTTPException(
            status_code=400, detail="End node cannot have outgoing edge."
        )
