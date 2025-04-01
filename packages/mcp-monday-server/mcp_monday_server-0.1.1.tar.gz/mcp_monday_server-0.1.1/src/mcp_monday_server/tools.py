from .common import logger, mcp, monday_client, MONDAY_BOARD_ID
from .resources import get_board_schema, get_item_by_id, get_items_by_column_value

@mcp.tool(name="Get_Board_Schema", description="Get schema from a specific board.")
async def get_board_schema_tool():
    return get_board_schema(MONDAY_BOARD_ID)

@mcp.tool(name="Get_Item_Details", description="Get item details by item ID.")
async def get_item_by_id_tool(item_id: str):
    return get_item_by_id(item_id)

@mcp.tool(name="Get_Items_by_Column_Value", description="Get items by column value.")
async def get_items_by_column_value_tool(column_id: str, column_value: str):
    return get_items_by_column_value(MONDAY_BOARD_ID, column_id, column_value)

@mcp.tool(name="Create_Item", description="Create a new item in the board.")
async def create_item_tool(item_name: str, group_id: str, column_values: dict):
    logger.info(f"Creating new item with name {item_name} in group {group_id} with values {column_values}")
    return monday_client.items.create_item(MONDAY_BOARD_ID,group_id,item_name,column_values)
    
@mcp.tool(name="Update_Item", description="Update an existing item in the board.")
async def update_item_tool(item_id: str, column_values: dict):
    logger.info(f"Updating item {item_id} with values {column_values}")
    return monday_client.items.change_multiple_column_values(MONDAY_BOARD_ID,item_id,column_values)
    
@mcp.tool(name="Delete_Item", description="Delete an item from the board.")
async def delete_item_tool(item_id: str):
    logger.info(f"Deleting item {item_id}")
    return monday_client.items.delete_item_by_id(item_id)