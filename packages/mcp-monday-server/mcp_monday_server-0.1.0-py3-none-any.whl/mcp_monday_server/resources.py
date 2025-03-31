from typing import Dict, Any, Union
from .common import logger, monday_client, MONDAY_BOARD_ID

class MondayResources:
    """Class to manage Monday.com resources with schema caching capabilities."""
    
    def __init__(self):
        self.boards = monday_client.boards
        self.items = monday_client.items
        self.groups = monday_client.groups
        self.columns = monday_client.columns
        self._board_schemas = {} 
    
    def get_board_schema(self, board_id: Union[int, str]) -> Dict[str, Any]:
        """Get schema of a specific board with caching."""

        if board_id in self._board_schemas:
            logger.info(f"Using cached schema for board {board_id}")
            return self._board_schemas[board_id]
        
        logger.info(f"Getting schema from board {board_id}")
        
        board_data = self.boards.fetch_boards_by_id(board_id)
        columns_data = self.boards.fetch_columns_by_board_id(board_id)
        groups_data = self.groups.get_groups_by_board(board_id)
        
        result = {
            "board_info": {"id": board_id, "name": board_data["data"]["boards"][0]["name"]},
            "columns": columns_data["data"]["boards"][0]["columns"],
            "groups": groups_data["data"]["boards"][0]["groups"],
            "tags": board_data["data"]["boards"][0].get("tags", [])
        }
        
        self._board_schemas[board_id] = result
        return result
    
    def get_item_by_id(self, item_id: Union[int, str]) -> Dict[str, Any]:
        """Get item details by item ID."""
        
        logger.info(f"Getting item with ID {item_id}")
        return self.items.fetch_items_by_id(item_id)

    def get_items_by_column_value(self, board_id: Union[int, str], column_id: Union[int, str], column_value: str) -> Dict[str, Any]:
        """Get items by column value."""
        
        logger.info(f"Getting items from board {board_id} with column {column_id} and value {column_value}")
        return self.items.fetch_items_by_column_value(board_id, column_id, column_value)

monday_resources = MondayResources()

def get_board_schema(board_id: Union[int, str] = MONDAY_BOARD_ID) -> Dict[str, Any]:
    return monday_resources.get_board_schema(board_id)

def get_item_by_id(item_id: Union[int, str]) -> Dict[str, Any]:
    return monday_resources.get_item_by_id(item_id)

def get_items_by_column_value(board_id: Union[int, str], column_id: Union[int, str], column_value: str) -> Dict[str, Any]:
    return monday_resources.get_items_by_column_value(board_id, column_id, column_value)