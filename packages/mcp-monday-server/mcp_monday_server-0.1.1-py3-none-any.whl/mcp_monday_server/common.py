import os, logging
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from monday import MondayClient

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers= [logging.FileHandler('mcp_monday_server.log') ,logging.StreamHandler()])

logger = logging.getLogger('mcp_monday_server')

# Load environment variables
load_dotenv()

# Configuration
MONDAY_API_KEY = os.getenv('MONDAY_API_KEY')
MONDAY_BOARD_ID = os.getenv('MONDAY_BOARD_ID')

# Initialize Monday server
mcp = FastMCP(
    name="mcp_monday_server",
    instructions=f"This server provides tools to interact with {MONDAY_BOARD_ID} monday board and its items"
)

# Initialize Monday client
monday_client = MondayClient(token=MONDAY_API_KEY)