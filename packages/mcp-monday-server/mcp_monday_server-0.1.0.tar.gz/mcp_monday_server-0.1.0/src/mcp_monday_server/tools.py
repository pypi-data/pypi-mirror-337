from .common import logger, MONDAY_BOARD_ID
from .resources import get_board_schema, get_item_by_id, get_items_by_column_value
from mcp import types

def register_tools(server, monday_client):
    """Registrar todas las herramientas con el servidor MCP."""
    
    tools = [
        types.Tool(
            name="Get_Board_Schema",
            description="Get schema from the configured Monday.com board.",
            inputSchema={"type": "object", "properties": {}}
        ),
        types.Tool(
            name="Get_Item_Details",
            description="Get item details by item ID.",
            inputSchema={
                "type": "object",
                "properties": {"item_id": {"type": "string"}},
                "required": ["item_id"]
            }
        ),
        types.Tool(
            name="Get_Items_by_Column_Value",
            description="Get items by column value.",
            inputSchema={
                "type": "object",
                "properties": {
                    "column_id": {"type": "string"},
                    "column_value": {"type": "string"}
                },
                "required": ["column_id", "column_value"]
            }
        ),
        types.Tool(
            name="Create_Item",
            description="Create a new item in the board.",
            inputSchema={
                "type": "object",
                "properties": {
                    "item_name": {"type": "string"},
                    "group_id": {"type": "string"},
                    "column_values": {"type": "object"}
                },
                "required": ["item_name", "group_id"]
            }
        ),
        types.Tool(
            name="Update_Item",
            description="Update an existing item in the board.",
            inputSchema={
                "type": "object",
                "properties": {
                    "item_id": {"type": "string"},
                    "column_values": {"type": "object"}
                },
                "required": ["item_id", "column_values"]
            }
        ),
        types.Tool(
            name="Delete_Item",
            description="Delete an item from the board.",
            inputSchema={
                "type": "object",
                "properties": {"item_id": {"type": "string"}},
                "required": ["item_id"]
            }
        )
    ]
    
    @server.list_tools()
    async def handle_list_tools():
        return tools

    @server.call_tool()
    async def handle_call_tool(name, arguments):
        try:
            if name == "Get_Board_Schema":
                result = get_board_schema(MONDAY_BOARD_ID)
                return [types.TextContent(type="text", text=f"Board Schema: {result}")]
            
            elif name == "Get_Item_Details":
                item_id = arguments.get("item_id")
                response = get_item_by_id(item_id)
                return [types.TextContent(type="text", text=f"Item Details: {response}")]
            
            elif name == "Get_Items_by_Column_Value":
                column_id = arguments.get("column_id")
                column_value = arguments.get("column_value")
                response = get_items_by_column_value(MONDAY_BOARD_ID, column_id, column_value)
                return [types.TextContent(type="text", text=f"Items by column value: {response}")]
            
            elif name == "Create_Item":
                item_name = arguments.get("item_name")
                group_id = arguments.get("group_id")
                column_values = arguments.get("column_values", {})
                logger.info(f"Creating new item with name {item_name} in group {group_id} with values {column_values}")
                response = monday_client.items.create_item(MONDAY_BOARD_ID, group_id, item_name, column_values)
                return [types.TextContent(type="text", text=f"Created item: {response}")]
            
            elif name == "Update_Item":
                item_id = arguments.get("item_id")
                column_values = arguments.get("column_values", {})
                logger.info(f"Updating item {item_id} with values {column_values}")
                response = monday_client.items.change_multiple_column_values(MONDAY_BOARD_ID, item_id, column_values)
                return [types.TextContent(type="text", text=f"Updated item: {response}")]
            
            elif name == "Delete_Item":
                item_id = arguments.get("item_id")
                logger.info(f"Deleting item {item_id}")
                response = monday_client.items.delete_item_by_id(item_id)
                return [types.TextContent(type="text", text=f"Deleted item: {response}")]
            
            else:
                raise ValueError(f"Unknown tool: {name}")

        except Exception as e:
            logger.error(f"Error calling tool {name}: {e}")
            raise