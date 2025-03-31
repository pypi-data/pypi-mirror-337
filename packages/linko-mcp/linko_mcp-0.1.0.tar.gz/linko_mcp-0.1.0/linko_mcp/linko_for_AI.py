"""
Linko MCP for AI - A Model Context Protocol extension for AI assistants to manage their own notes in Linko.

This module implements MCP tools to allow AI assistants to create, retrieve, update, and delete
their own notes in Linko, supporting cognitive continuity between sessions.
"""

from mcp.server.fastmcp import FastMCP
import sys
import logging
import os
import getpass
import asyncio
import argparse
from logging.handlers import RotatingFileHandler
from typing import Dict, Any, Optional, List
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

# Import from package
from . import auth
from .api_client import LinkoAPIClient, LinkoAPIError, LinkoAuthError

# Get the directory of the current script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Define logs directory
LOGS_DIR = os.path.join(SCRIPT_DIR, "logs")
# Ensure logs directory exists
os.makedirs(LOGS_DIR, exist_ok=True)

# Setup logging with rotation (specific file for AI)
log_file = os.path.join(LOGS_DIR, "linko_for_AI.log")
handler = RotatingFileHandler(
    filename=log_file,
    maxBytes=5*1024*1024,  # 5MB
    backupCount=3           # Keep 3 backup files
)
# Configure root logger - level will be set by args later
logging.basicConfig(
    level=logging.INFO, # Default level
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[handler, logging.StreamHandler()] # Also log to console for AI MCP
)
# Set httpx logger level higher to avoid verbose connection logs
logging.getLogger("httpx").setLevel(logging.WARNING)
# Use specific logger for this module
logger = logging.getLogger('linko_for_AI')

# --- MCP Server Setup ---

# Global API client instance (initialized later)
api_client: Optional[LinkoAPIClient] = None

# Specific token path for AI
AI_TOKEN_PATH = os.path.expanduser("~/.linko/auth_ai.json")

# Reference to hold command line args
cmd_args = None

@asynccontextmanager
async def lifespan(server: FastMCP) -> AsyncIterator[dict]:
    """Manage server startup and shutdown lifecycle."""
    # Get arguments from global reference
    global cmd_args
    
    # Initialize on startup
    start_result = await startup_ai(cmd_args)
    try:
        yield start_result
    finally:
        # Clean up on shutdown
        await shutdown_ai()

# Create FastMCP instance with lifespan
mcp = FastMCP("Linko MCP for AI", lifespan=lifespan)

# --- Helper Functions (Shared with main module) ---

def _parse_int(value: Any, default: int) -> int:
    """Safely parse an integer."""
    try:
        return int(value) if value is not None else default
    except (ValueError, TypeError):
        return default

def _parse_str(value: Any) -> Optional[str]:
    """Safely parse a string, returning None if empty."""
    return str(value) if value else None

# --- Error Handling Wrapper (Adapted for AI tools) ---

async def _handle_api_call(tool_name: str, coro, *args, **kwargs) -> Dict[str, Any]:
    """Wraps API calls in AI tools to handle common errors."""
    global api_client
    if not api_client:
         logger.error(f"{tool_name}: API client not initialized.")
         # Provide a more specific error message for the AI context
         return {"error": "Internal Server Error", "message": "API client not available. Cannot interact with Linko."}

    try:
        return await coro(*args, **kwargs)
    except LinkoAuthError as e:
        logger.error(f"{tool_name}: Authentication error: {e}")
        # More specific message for AI context
        return {"error": "Authentication Failed", "message": str(e) or "Authentication token invalid or expired. Please restart AI MCP."}
    except LinkoAPIError as e:
        logger.error(f"{tool_name}: API error (Status: {e.status_code}): {e}")
        return {"error": f"API Request Failed (Status: {e.status_code})", "message": str(e)}
    except Exception as e:
        logger.exception(f"{tool_name}: Unexpected error occurred.") # Log full traceback
        return {"error": "Unexpected Error", "message": f"An unexpected error occurred: {str(e)}"}

# --- MCP Tool Definitions ---

@mcp.tool()
async def get_notes_for_AI(
    keyword=None,
    limit=10,
    subject_name=None,
    days_ago=None,
    offset=0
) -> Dict[str, Any]:
    """
    Get AI-created notes from Linko with versatile filtering options.

    This tool helps the AI retrieve its own notes using various filtering criteria.
    The AI can search by keyword, browse notes related to specific subjects/topics,
    or get its most recent notes.

    Core capabilities:
    - Search notes using keywords (with semantic embedding for relevance)
    - Filter notes by subject/topic
    - Filter notes by time period
    - Get recent notes when no filters are applied

    Usage examples:
    - "Get my psychology notes" → get_notes_for_AI(subject_name="psychology")
    - "Find notes about machine learning" → get_notes_for_AI(keyword="machine learning")
    - "Get my notes from the past week" → get_notes_for_AI(days_ago=7)
    - "Show my 5 most recent notes" → get_notes_for_AI(limit=5)
    - "Get my next 10 notes" → get_notes_for_AI(offset=10)

    Args:
        keyword: Search term to find notes by content (uses semantic embedding for relevance)
        limit: Maximum number of notes to return (default: 10)
        subject_name: Subject/knowledge name to filter notes by topic (e.g., "Psychology", "Machine Learning")
        days_ago: Filter to get notes from the last N days (e.g., 7 for notes from the past week)
        offset: Number of notes to skip for pagination (default: 0)

    Returns:
        A dictionary containing:
        - notes: List of notes matching the criteria with full content
        - total_count: Total number of notes found matching the criteria
        - displayed_count: Number of notes returned (limited by the limit parameter)
        - search_context: Description of the search criteria applied
    """
    async def core_logic():
        # Type conversions
        keyword_str = _parse_str(keyword)
        subject_name_str = _parse_str(subject_name)
        days_ago_int = _parse_int(days_ago, default=None)
        limit_int = _parse_int(limit, default=10)
        offset_int = _parse_int(offset, default=0)

        # Fetch subject ID using the shared client helper
        subject_id = await api_client.search_knowledge_id(subject_name_str) if subject_name_str else None

        # --- Build API request parameters ---
        params = {}
        endpoint = "/api/note/" # Default endpoint for filtering
        search_used = False

        if keyword_str:
            # Use search endpoint if keyword is provided
            endpoint = "/api/search/search_notes/"
            params["keyword"] = keyword_str
            search_used = True
            logger.info(f"AI Searching notes with keyword: '{keyword_str}'")
        else:
            # Use list endpoint for filtering by ID, date, etc.
            # Note: API might not paginate search results, pagination primarily for list view
            params["limit"] = str(limit_int)
            params["offset"] = str(offset_int)  # Use the offset parameter instead of hardcoded "0"
            if subject_id:
                params["filter_knowledge"] = subject_id
            # Date filtering needs client-side processing for list endpoint

            filter_msg = []
            if subject_name_str: filter_msg.append(f"subject '{subject_name_str}' (ID: {subject_id})")
            if days_ago_int: filter_msg.append(f"from last {days_ago_int} days")
            if offset_int > 0: filter_msg.append(f"offset {offset_int}")
            logger.info(f"AI Fetching notes with filters: {', '.join(filter_msg) if filter_msg else 'Recent notes'} (Limit: {limit_int})")

        # --- Make API Call using shared client ---
        response_data = await api_client.get(endpoint, params=params)
        
        # Add debug logging for API response
        logger.info(f"API Response for AI notes with offset {offset_int}: params={params}")
        if isinstance(response_data, dict):
            if "results" in response_data:
                logger.info(f"Response contains 'results' field with {len(response_data['results'])} notes")
                if "count" in response_data:
                    logger.info(f"Response 'count' field reports {response_data['count']} total notes")
            else:
                logger.info(f"Response structure: {list(response_data.keys())}")
        elif isinstance(response_data, list):
            logger.info(f"Response is a list with {len(response_data)} notes")
        else:
            logger.info(f"Response is of type {type(response_data)}")

        # --- Process Response ---
        if search_used:
            # For search endpoint, response is a list of notes
            if not isinstance(response_data, list):
                logger.warning(f"Expected list response from search endpoint, got {type(response_data)}")
                notes = []
                total_count = 0
            else:
                notes = response_data
                total_count = len(notes)
        else:
            # For list endpoint, response should be a dict with results and count
            if not isinstance(response_data, dict):
                logger.warning(f"Expected dict response from list endpoint, got {type(response_data)}")
                notes = []
                total_count = 0
            else:
                notes = response_data.get("results", [])
                total_count = response_data.get("count", len(notes))

        # --- Apply client-side filtering if needed ---
        # Filter by days_ago for list endpoint (search handles this via API)
        if days_ago_int is not None and not search_used:
            import datetime
            cutoff_date = datetime.datetime.now() - datetime.timedelta(days=days_ago_int)
            # Convert to UTC datetime string for comparison with API dates
            cutoff_str = cutoff_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            # Filter notes created after cutoff date
            notes = [note for note in notes if note.get("created_at", "") >= cutoff_str]
            # Adjust total_count
            total_count = len(notes)

        # --- Format notes for return ---
        formatted_notes = []
        for note in notes:
            note_id = note.get("id")
            title = note.get("title", "")
            content = note.get("content", "")
            
            # Extract dates
            created_at = note.get("created_at", "")
            updated_at = note.get("updated_at", "")
            
            # Extract knowledge/subject if available
            knowledge = note.get("knowledge", {})
            knowledge_name = knowledge.get("title", "") if isinstance(knowledge, dict) else ""
            
            # Format for response - include full data for AI's own notes
            formatted_note = {
                "id": note_id,
                "title": title,
                "content": content,
                "subject": knowledge_name,
                "created_at": created_at,
                "updated_at": updated_at
            }
            
            formatted_notes.append(formatted_note)

        # --- Build search context description ---
        context_parts = []
        if keyword_str:
            context_parts.append(f"containing keyword '{keyword_str}'")
        if subject_name_str:
            context_parts.append(f"from subject '{subject_name_str}'")
        if days_ago_int:
            context_parts.append(f"created in the last {days_ago_int} days")
        
        search_context = "Your notes " + (", ".join(context_parts) if context_parts else "from recent sessions")
        if offset_int > 0:
            search_context += f" (skipping first {offset_int} results)"
        
        return {
            "notes": formatted_notes,
            "total_count": total_count,
            "displayed_count": len(formatted_notes),
            "search_context": search_context
        }
    
    # Call with error handling wrapper
    return await _handle_api_call("get_notes_for_AI", core_logic)

@mcp.tool()
async def create_note_for_AI(
    title: str,
    content: str
) -> Dict[str, Any]:
    """
    Create a new note in Linko for AI use.

    This tool allows the AI to create its own notes in Linko, storing information
    it wants to remember for future reference.

    Args:
        title: Title of the note (required)
        content: Content of the note (required)

    Returns:
        A dictionary containing:
        - note: The created note data
        - detail: Status message
    """
    async def core_logic():
        # Validate required parameters
        if not title:
            return {"error": "Missing Title", "message": "Note title is required"}
        if not content:
            return {"error": "Missing Content", "message": "Note content is required"}
            
        # Prepare data for API
        note_data = {
            "title": title,
            "content": content
        }
        
        logger.info(f"AI Creating new note with title: '{title}'")
        
        # Make API call
        response = await api_client.post("/api/note/", json_data=note_data)
        
        # Check if response contains expected data
        if "id" not in response:
            logger.warning(f"Note creation response missing ID, response: {response}")
            return {"error": "Invalid Response", "message": "Note creation returned an invalid response"}
            
        # Format the response
        return {
            "note": {
                "id": response.get("id"),
                "title": response.get("title", title),
                "content": response.get("content", content),
                "created_at": response.get("created_at", ""),
                "updated_at": response.get("updated_at", "")
            },
            "detail": "Note created successfully"
        }
    
    # Call with error handling wrapper
    return await _handle_api_call("create_note_for_AI", core_logic)

@mcp.tool()
async def update_note_for_AI(
    note_id: str,
    title=None,
    content=None
) -> Dict[str, Any]:
    """
    Update an existing note in Linko for AI use.

    This tool allows the AI to update notes it has previously created.

    Args:
        note_id: ID of the note to update (required)
        title: New title for the note (optional)
        content: New content for the note (optional)

    Returns:
        A dictionary containing:
        - note: The updated note data
        - detail: Status message
    """
    async def core_logic():
        # Validate required parameters
        if not note_id:
            return {"error": "Missing Note ID", "message": "Note ID is required for updates"}
            
        # Must have at least one field to update
        if title is None and content is None:
            return {"error": "No Update Fields", "message": "At least one field (title or content) must be provided for update"}
            
        # Prepare data for API - only include fields that are provided
        note_data = {}
        if title is not None:
            note_data["title"] = title
        if content is not None:
            note_data["content"] = content
        
        logger.info(f"AI Updating note with ID: {note_id}")
        
        # First fetch the current note to verify it exists
        try:
            current_note = await api_client.get(f"/api/note/{note_id}/")
            if not current_note or "id" not in current_note:
                return {"error": "Note Not Found", "message": f"Note with ID {note_id} not found"}
        except LinkoAPIError as e:
            if e.status_code == 404:
                return {"error": "Note Not Found", "message": f"Note with ID {note_id} not found"}
            raise  # Re-raise other errors to be caught by error handler
            
        # Make update API call
        response = await api_client.put(f"/api/note/{note_id}/", json_data=note_data)
        
        # Format the response
        return {
            "note": {
                "id": response.get("id", note_id),
                "title": response.get("title", title if title is not None else current_note.get("title", "")),
                "content": response.get("content", content if content is not None else current_note.get("content", "")),
                "updated_at": response.get("updated_at", "")
            },
            "detail": "Note updated successfully"
        }
    
    # Call with error handling wrapper
    return await _handle_api_call("update_note_for_AI", core_logic)

@mcp.tool()
async def delete_note_for_AI(
    note_id: str
) -> Dict[str, Any]:
    """
    Delete a note from Linko for AI use.

    This tool allows the AI to delete notes it has previously created.

    Args:
        note_id: ID of the note to delete (required)

    Returns:
        A dictionary containing the status of the deletion
    """
    async def core_logic():
        # Validate required parameters
        if not note_id:
            return {"error": "Missing Note ID", "message": "Note ID is required for deletion"}
            
        logger.info(f"AI Deleting note with ID: {note_id}")
        
        # Make delete API call
        try:
            await api_client.delete(f"/api/note/{note_id}/")
            return {"detail": f"Note {note_id} deleted successfully"}
        except LinkoAPIError as e:
            if e.status_code == 404:
                return {"error": "Note Not Found", "message": f"Note with ID {note_id} not found or already deleted"}
            raise  # Re-raise other errors to be caught by error handler
    
    # Call with error handling wrapper
    return await _handle_api_call("delete_note_for_AI", core_logic)

# --- Command Line Arguments ---

def parse_args():
    """Parse command line arguments for AI MCP."""
    parser = argparse.ArgumentParser(description="Linko MCP for AI - Allow AI assistants to manage their notes")
    parser.add_argument("--username", help="AI's Linko email address (overrides environment variable)")
    parser.add_argument("--password", help="AI's Linko password (overrides environment variable)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")
    parser.add_argument("--base-url", help="Linko API base URL (default: https://www.linko.study)")
    return parser.parse_args()

# --- Authentication Check for AI ---

async def check_authentication_ai(cmd_args) -> bool:
    """Check authentication status and authenticate if needed for AI user."""
    global api_client
    
    # Set logging level based on verbose flag
    if cmd_args.verbose:
        logging.getLogger('linko_for_AI').setLevel(logging.DEBUG)
        logging.getLogger('linko_mcp.auth').setLevel(logging.DEBUG)
        logging.getLogger('linko_mcp.api_client').setLevel(logging.DEBUG)
        logger.debug("Verbose logging enabled for AI")
    
    # Create API client with specified base URL if provided, using AI-specific token path
    api_client = LinkoAPIClient(
        base_url=cmd_args.base_url,
        token_path=AI_TOKEN_PATH
    )
    
    # Check for stored AI token first
    token_data = auth.get_stored_token(token_path=AI_TOKEN_PATH)
    if token_data and 'access_token' in token_data:
        token = token_data['access_token']
        logger.info("Found stored AI access token, verifying...")
        
        if await auth.verify_token(token, base_url=cmd_args.base_url):
            logger.info("Stored AI token is valid.")
            return True
        else:
            logger.warning("Stored AI token is invalid or expired.")
            
            # Try refreshing token
            logger.info("Attempting to refresh AI token...")
            new_token = await auth.refresh_access_token(base_url=cmd_args.base_url, token_path=AI_TOKEN_PATH)
            if new_token:
                logger.info("AI token refreshed successfully.")
                return True
            else:
                logger.warning("AI token refresh failed, need to re-authenticate.")
    else:
        logger.info("No stored AI token found.")
    
    # If we get here, we need authentication with username/password
    username = cmd_args.username
    password = cmd_args.password
    
    # If not provided via command line, try environment variables (AI-specific ones)
    if not username or not password:
        env_username, env_password, _ = auth.get_ai_credentials_from_env()
        username = username or env_username
        password = password or env_password
    
    # If still not available, prompt user (only works in interactive mode)
    if not username:
        logger.info("AI username not provided via arguments or environment variables.")
        try:
            username = input("AI Linko email: ")
        except (EOFError, KeyboardInterrupt):
            logger.error("Authentication canceled.")
            return False
    
    if not password:
        logger.info("AI password not provided via arguments or environment variables.")
        try:
            password = getpass.getpass("AI Linko password: ")
        except (EOFError, KeyboardInterrupt):
            logger.error("Authentication canceled.")
            return False
    
    # Attempt authentication
    if not username or not password:
        logger.error("AI username and password are required. Please provide via command line arguments, environment variables, or interactive prompt.")
        return False
    
    logger.info(f"Authenticating with AI username: {username}")
    auth_result = await auth.authenticate(
        username=username,
        password=password,
        base_url=cmd_args.base_url,
        token_path=AI_TOKEN_PATH  # Use AI-specific token path
    )
    
    if auth_result:
        logger.info("AI authentication successful.")
        return True
    else:
        logger.error("AI authentication failed. Please check your credentials.")
        return False

# --- Startup/Shutdown Functions ---

async def startup_ai(args):
    """Startup function for the AI MCP server."""
    logger.info("Starting Linko MCP for AI...")
    
    # Check authentication for AI
    auth_success = await check_authentication_ai(args)
    if not auth_success:
        logger.error("AI authentication failed, MCP may not function correctly.")
        # Don't exit - some endpoints might work without auth
    
    # Initialize MCP server
    logger.info("Linko MCP for AI ready to serve requests.")
    return {"status": "started", "authenticated": auth_success}

async def shutdown_ai():
    """Shutdown function for the AI MCP server."""
    logger.info("Shutting down Linko MCP for AI...")
    
    # Close API client if active
    global api_client
    if api_client:
        await api_client.close()
        logger.info("AI API client connection closed.")
    
    logger.info("Linko MCP for AI shutdown complete.")
    return {"status": "shutdown"}

# --- Main Entry Point ---

def main():
    """Main entry point for the Linko MCP for AI service."""
    # Parse command line arguments
    args = parse_args()
    
    # Set args in global reference for lifespan to access
    global cmd_args
    cmd_args = args
    
    # Start the MCP server
    sys.exit(mcp.run())

if __name__ == "__main__":
    main() 