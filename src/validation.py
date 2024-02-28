from fastapi import HTTPException


def edges_validation(graph, start_node_id: int, end_node_id: int) -> None:
    successors = len(list(graph.successors(start_node_id)))

    if graph.nodes[start_node_id]["type"] == "start" and successors == 1:
        raise HTTPException(status_code=400, detail="Start node can only have one outgoing edge.")

    elif graph.nodes[end_node_id]["type"] == "start":
        raise HTTPException(
            status_code=400, detail="Start node can't have incoming edge."
        )

    elif graph.nodes[start_node_id]["type"] == "message" and successors == 1:
        raise HTTPException(
            status_code=400, detail="Message node can only have one outgoing edge."
        )

    elif graph.nodes[start_node_id]["type"] == "condition" and successors == 2:
        raise HTTPException(
            status_code=400, detail="Condition node can only have 2 outgoing edges."
        )

    elif graph.nodes[start_node_id]["type"] == "end":
        raise HTTPException(
            status_code=400, detail="End node cannot have outgoing edge."
        )
