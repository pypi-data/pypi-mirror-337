from typing import Dict, Any, Union
from .common import logger, monday_client

def get_board_schema(board_id: Union[int, str]) -> Dict[str, Any]:
    """
    Get schema of a specific board.
    """
    logger.info(f"Getting schema from board {board_id}")
    
    board_data = monday_client.boards.fetch_boards_by_id(board_id)
    columns_data = monday_client.boards.fetch_columns_by_board_id(board_id)
    groups_data = monday_client.groups.get_groups_by_board(board_id)
    
    result = {
        "board_info": {"id": board_id, "name": board_data["data"]["boards"][0]["name"]},
        "columns": columns_data["data"]["boards"][0]["columns"],
        "groups": groups_data["data"]["boards"][0]["groups"],
        "tags": board_data["data"]["boards"][0].get("tags", [])
    }
    
    return result

def get_item_by_id(item_id: Union[int, str]) -> Dict[str, Any]:
    """
    Get item details by item ID.
    """
    logger.info(f"Getting item with ID {item_id}")
    return monday_client.items.fetch_items_by_id(item_id)

def get_items_by_column_value(board_id: Union[int, str], column_id: Union[int, str], column_value: str) -> Dict[str, Any]:
    """
    Get items by column value.
    """
    logger.info(f"Getting items from board {board_id} with column {column_id} and value {column_value}")
    return monday_client.items.fetch_items_by_column_value(board_id, column_id, column_value)