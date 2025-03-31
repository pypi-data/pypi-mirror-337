"""
Linko MCP - A Model Context Protocol extension for accessing Linko study notes and resources.

This module implements MCP tools to allow LLMs to access the Linko API for retrieving 
study notes, resources, and subject information.
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

# Import local modules
from . import auth
from .api_client import LinkoAPIClient, LinkoAPIError, LinkoAuthError

# Get the directory of the current script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Define logs directory
LOGS_DIR = os.path.join(SCRIPT_DIR, "logs")
# Ensure logs directory exists
os.makedirs(LOGS_DIR, exist_ok=True)

# Setup logging with rotation
log_file = os.path.join(LOGS_DIR, "linko_mcp.log")
handler = RotatingFileHandler(
    filename=log_file,
    maxBytes=5*1024*1024,  # 5MB
    backupCount=3           # Keep 3 backup files
)
logging.basicConfig(
    level=logging.INFO, # Default to INFO, can be overridden by args
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[handler, logging.StreamHandler()] # Also log to console
)
# Set httpx logger level higher to avoid verbose connection logs
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger('linko_mcp') # Main logger

# --- MCP Server Setup ---

# Global API client instance (initialized later)
api_client: Optional[LinkoAPIClient] = None

# Reference to hold command line args
cmd_args = None

@asynccontextmanager
async def lifespan(server: FastMCP) -> AsyncIterator[dict]:
    """Manage server startup and shutdown lifecycle."""
    # Get arguments from global reference
    global cmd_args
    
    # Initialize on startup
    start_result = await startup(cmd_args)
    try:
        yield start_result
    finally:
        # Clean up on shutdown
        await shutdown()

# Create FastMCP instance with lifespan
mcp = FastMCP("Linko MCP", lifespan=lifespan)

# --- Helper Functions (Type conversion, etc.) ---

def _parse_int(value: Any, default: int) -> int:
    """Safely parse an integer."""
    try:
        return int(value) if value is not None else default
    except (ValueError, TypeError):
        return default

def _parse_str(value: Any) -> Optional[str]:
    """Safely parse a string, returning None if empty."""
    return str(value) if value else None

# --- Error Handling Wrapper for Tools ---

async def _handle_api_call(tool_name: str, coro, *args, **kwargs) -> Dict[str, Any]:
    """Wraps API calls in tools to handle common errors."""
    global api_client
    if not api_client:
         logger.error(f"{tool_name}: API client not initialized.")
         return {"error": "Internal Server Error", "message": "API client not available."}
         
    try:
        return await coro(*args, **kwargs)
    except LinkoAuthError as e:
        logger.error(f"{tool_name}: Authentication error: {e}")
        return {"error": "Authentication Failed", "message": str(e) or "Authentication token invalid or expired. Please restart MCP."}
    except LinkoAPIError as e:
        logger.error(f"{tool_name}: API error (Status: {e.status_code}): {e}")
        return {"error": f"API Request Failed (Status: {e.status_code})", "message": str(e)}
    except Exception as e:
        logger.exception(f"{tool_name}: Unexpected error occurred.") # Log full traceback
        return {"error": "Unexpected Error", "message": f"An unexpected error occurred: {str(e)}"}
        
# --- MCP Tool Definitions ---

@mcp.tool()
async def get_notes(
    keyword=None,
    limit=10,
    subject_name=None,
    resource_name=None,
    days_ago=None,
    offset=0
) -> Dict[str, Any]:
    """
    Get user's study notes from Linko with versatile filtering options and pagination.
    
    Core capabilities:
    - Search notes using keywords (with semantic embedding for relevance)
    - Filter notes by subject/topic
    - Filter notes by resource (book, article, video, etc.)
    - Filter notes by time period
    - Get recent notes when no filters are applied
    - Use offset for pagination (fetches notes in batches)
    
    NOTE: The maximum number of notes returned per request is capped at 10.

    Usage examples:
    - "Get my psychology notes" → get_notes(subject_name="psychology")
    - "Find notes about machine learning" → get_notes(keyword="machine learning")
    - "Show my notes on the book 'Thinking Fast and Slow'" → get_notes(resource_name="Thinking Fast and Slow")
    - "Get my notes from the past week" → get_notes(days_ago=7)
    - "Show my 5 most recent notes" → get_notes(limit=5)
    - "Get the next 10 notes about machine learning" → get_notes(keyword="machine learning", offset=10)
    
    Args:
        keyword: Search term to find notes by content (uses semantic embedding for relevance)
        limit: Maximum number of notes to return (default: 10, **max: 10**)
        subject_name: Subject/knowledge name to filter notes by topic (e.g., "Psychology", "Machine Learning")
        resource_name: Resource title to get notes from a specific resource (e.g., book title, article name)
        days_ago: Filter to get notes from the last N days (e.g., 7 for notes from the past week)
        offset: Number of notes to skip for pagination (default: 0)
    
    Returns:
        A dictionary containing:
        - notes: List of notes matching the criteria with content previews
        - total_count: Total number of notes found matching the criteria
        - displayed_count: Number of notes returned (limited by the limit parameter)
        - search_context: Description of the search criteria applied
    """
    async def core_logic():
        # Type conversions
        keyword_str = _parse_str(keyword)
        subject_name_str = _parse_str(subject_name)
        resource_name_str = _parse_str(resource_name)
        days_ago_int = _parse_int(days_ago, default=None)
        limit_int = min(_parse_int(limit, default=10), 10) # Enforce max limit of 10
        offset_int = _parse_int(offset, default=0)
        
        # Fetch IDs if names are provided
        resource_id = await api_client.search_resource_id(resource_name_str) if resource_name_str else None
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
            logger.info(f"Searching notes with keyword: '{keyword_str}'")
        else:
            # Use list endpoint for filtering by ID, date, etc.
            params["limit"] = str(limit_int)
            params["offset"] = str(offset_int)
            if subject_id:
                params["filter_knowledge"] = subject_id
            if resource_id:
                # Note: Check if the backend /api/note/ supports resource_id filtering directly
                # If not, filtering might need to happen client-side after fetching,
                # or the search endpoint might be better even without a keyword.
                # Assuming it supports `resource_id` for now based on old code structure.
                params["resource_id"] = resource_id 
            # Date filtering needs to be applied *after* fetching if using list endpoint
            
            filter_msg = []
            if subject_name_str: filter_msg.append(f"subject '{subject_name_str}' (ID: {subject_id})")
            if resource_name_str: filter_msg.append(f"resource '{resource_name_str}' (ID: {resource_id})")
            if days_ago_int: filter_msg.append(f"from last {days_ago_int} days")
            logger.info(f"Fetching notes with filters: {', '.join(filter_msg) if filter_msg else 'Recent notes'} (Limit: {limit_int})")

        # --- Make API Call --- 
        try:
            response_data = await api_client.get(endpoint, params=params)
            
            # Add debug logging for API response
            logger.info(f"API Response for notes with offset {offset_int}: params={params}")
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
                    total_count_from_api = 0
                else:
                    notes = response_data
                    total_count_from_api = len(notes)
            else:
                # For list endpoint, response should be a dict with results and count
                if not isinstance(response_data, dict):
                    logger.warning(f"Expected dict response from list endpoint, got {type(response_data)}")
                    notes = []
                    total_count_from_api = 0
                else:
                    notes = response_data.get("results", [])
                    total_count_from_api = response_data.get("count", len(notes))
            
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
                total_count_from_api = len(notes)
            
            # --- Prepare notes for return ---
            # Format each note to include the essential fields
            formatted_notes = process_notes_response(notes)
            
            # --- Build search context description ---
            context_parts = []
            if keyword_str:
                context_parts.append(f"containing keyword '{keyword_str}'")
            if subject_name_str:
                context_parts.append(f"from subject '{subject_name_str}'")
            if resource_name_str:
                context_parts.append(f"from resource '{resource_name_str}'")
            if days_ago_int:
                context_parts.append(f"created in the last {days_ago_int} days")
            
            search_context = "Notes " + (", ".join(context_parts) if context_parts else "from your recent studies")
            if offset_int > 0:
                search_context += f" (skipping first {offset_int} results)"
            
            return {
                "notes": formatted_notes,
                "total_count": total_count_from_api,
                "displayed_count": len(formatted_notes),
                "search_context": search_context
            }
            
        except Exception as e:
            logger.exception(f"Error processing notes response: {e}")
            return {"error": "Processing Error", "message": f"Error processing notes: {str(e)}"}
    
    # Call with error handling wrapper
    return await _handle_api_call("get_notes", core_logic)

def process_notes_response(notes):
    """Process and format note objects from API response."""
    formatted_notes = []
    
    for note in notes:
        note_id = note.get("id")
        title = note.get("title", "")
        content = note.get("content", "")
        
        # Extract dates
        created_at = note.get("created_at", "")
        updated_at = note.get("updated_at", "")
        
        # Extract associated data
        knowledge = note.get("knowledge", {})
        knowledge_name = knowledge.get("title", "") if isinstance(knowledge, dict) else ""
        
        resource = note.get("resource", {}) 
        resource_name = resource.get("title", "") if isinstance(resource, dict) else ""
        
        # Prepare a formatted object with consistent structure
        formatted_note = {
            "id": note_id,
            "title": title,
            "content": content,
            "subject": knowledge_name,
            "resource": resource_name,
            "created_at": created_at,
            "updated_at": updated_at
        }
        
        formatted_notes.append(formatted_note)
    
    return formatted_notes

@mcp.tool()
async def get_resources(
    keyword=None,
    limit=10,
    subject_name=None,
    resource_type=None,
    finished=None,
    offset=0
) -> Dict[str, Any]:
    """
    Get learning resources from Linko with filtering options.
    
    Core capabilities:
    - Search resources by keyword
    - Filter by subject/topic
    - Filter by resource type (book, article, course, etc.)
    - Filter by completion status
    
    Usage examples:
    - "Find books on machine learning" → get_resources(keyword="machine learning", resource_type="book")
    - "Show resources for my psychology studies" → get_resources(subject_name="psychology")
    - "Get my completed courses" → get_resources(resource_type="course", finished=True)
    - "Find articles about neural networks" → get_resources(keyword="neural networks", resource_type="article")
    
    Args:
        keyword: Search term to find resources by title, author, etc.
        limit: Maximum number of resources to return (default: 10)
        subject_name: Subject/knowledge area to filter resources by (e.g., "Psychology")
        resource_type: Type of resource to filter by (e.g., "book", "article", "course", "video")
        finished: Filter by completion status (True=completed, False=in progress/not started)
        offset: Number of resources to skip for pagination (default: 0)
    
    Returns:
        A dictionary containing:
        - resources: List of resources matching the criteria
        - total_count: Total number of resources found
        - displayed_count: Number of resources returned (limited by limit)
        - search_context: Description of the search criteria applied
    """
    async def core_logic():
        # Type conversions and validation
        keyword_str = _parse_str(keyword)
        subject_name_str = _parse_str(subject_name)
        resource_type_str = _parse_str(resource_type)
        limit_int = _parse_int(limit, default=10)
        offset_int = _parse_int(offset, default=0)
        
        # Normalize resource type to lowercase and validate
        if resource_type_str:
            resource_type_str = resource_type_str.lower()
            valid_types = ["book", "article", "video", "course", "paper", "podcast", "other"]
            if resource_type_str not in valid_types:
                logger.warning(f"Invalid resource type: '{resource_type_str}'. Valid types are: {', '.join(valid_types)}")
        
        # Get subject ID
        subject_id = await api_client.search_knowledge_id(subject_name_str) if subject_name_str else None
        
        # --- Build API request parameters ---
        params = {}
        endpoint = "/api/resources/"  # Default endpoint for resources
        search_used = False
        
        if keyword_str:
            # Search endpoint if keyword is provided
            endpoint = "/api/search/search_resource/"
            params["keyword"] = keyword_str
            search_used = True
            logger.info(f"Searching resources with keyword: '{keyword_str}'")
        else:
            # Use list endpoint with filters
            params["limit"] = str(limit_int)
            params["offset"] = str(offset_int)
            if subject_id:
                params["knowledge"] = subject_id
            if resource_type_str:
                params["resource_type"] = resource_type_str.capitalize()  # API might expect capitalized type
                
            # Build log message for filters
            filter_msg = []
            if subject_name_str: filter_msg.append(f"subject '{subject_name_str}' (ID: {subject_id})")
            if resource_type_str: filter_msg.append(f"type '{resource_type_str}'")
            if finished is not None: filter_msg.append(f"status: {'completed' if finished else 'not completed'}")
            logger.info(f"Fetching resources with filters: {', '.join(filter_msg) if filter_msg else 'All resources'} (Limit: {limit_int})")
        
        # --- Make API Call ---
        response_data = await api_client.get(endpoint, params=params)
        
        # --- Process Response ---
        if search_used:
            # For search endpoint, response is a list
            if not isinstance(response_data, list):
                logger.warning(f"Expected list response from search endpoint, got {type(response_data)}")
                resources = []
                total_count = 0
            else:
                resources = response_data
                total_count = len(resources)
        else:
            # For list endpoint, response is a dict with results and count
            if not isinstance(response_data, dict):
                logger.warning(f"Expected dict response from list endpoint, got {type(response_data)}")
                resources = []
                total_count = 0
            else:
                resources = response_data.get("results", [])
                total_count = response_data.get("count", len(resources))
        
        # --- Apply client-side filtering not handled by API ---
        # Filter by finished status if specified
        if finished is not None:
            resources = [r for r in resources if r.get("is_finished", False) == finished]
            # Update total count for client-side filtering
            total_count = len(resources)
        
        # Apply offset/limit for search results (if API doesn't do pagination)
        if search_used:
            # Apply offset
            resources = resources[offset_int:]
            # Apply limit
            resources = resources[:limit_int]
        
        # --- Format resources for response ---
        formatted_resources = []
        for resource in resources:
            # Extract basic fields
            resource_id = resource.get("id")
            title = resource.get("title", "")
            author = resource.get("author", "")
            resource_type = resource.get("resource_type", "")
            description = resource.get("description", "")
            is_finished = resource.get("is_finished", False)
            
            # Extract knowledge/subject
            knowledge_data = resource.get("knowledge", {})
            subject_name = knowledge_data.get("title", "") if isinstance(knowledge_data, dict) else ""
            
            # Format for response
            formatted_resource = {
                "id": resource_id,
                "title": title,
                "author": author,
                "type": resource_type,
                "description": description,
                "subject": subject_name,
                "is_finished": is_finished
            }
            
            formatted_resources.append(formatted_resource)
        
        # --- Build search context description ---
        context_parts = []
        if keyword_str:
            context_parts.append(f"matching '{keyword_str}'")
        if subject_name_str:
            context_parts.append(f"in subject '{subject_name_str}'")
        if resource_type_str:
            context_parts.append(f"of type '{resource_type_str}'")
        if finished is not None:
            context_parts.append(f"marked as {'completed' if finished else 'not completed'}")
        
        search_context = "Resources " + (", ".join(context_parts) if context_parts else "from your collection")
        if offset_int > 0:
            search_context += f" (skipping first {offset_int} results)"
        
        return {
            "resources": formatted_resources,
            "total_count": total_count,
            "displayed_count": len(formatted_resources),
            "search_context": search_context
        }
    
    # Call with error handling wrapper
    return await _handle_api_call("get_resources", core_logic)

@mcp.tool()
async def get_subjects(
    subject_id=None,
    limit=10,
    include_content=False,
    offset=0
) -> Dict[str, Any]:
    """
    Get information about the user's knowledge subjects from Linko.
    
    Core capabilities:
    - List all subjects/knowledge areas
    - Get detailed information about a specific subject
    - Get associated resources for each subject

    Usage examples:
    - "What subjects am I studying?" → get_subjects()
    - "Tell me about my Machine Learning studies" → get_subjects(subject_id=<id>)
    - "Show me all my subjects with details" → get_subjects(include_content=True)
    
    Args:
        subject_id: ID of a specific subject to fetch details for
        limit: Maximum number of subjects to return (default: 10)
        include_content: Whether to include detailed content/description (default: False)
        offset: Number of subjects to skip for pagination (default: 0)
    
    Returns:
        A dictionary containing:
        - subjects: List of subjects with basic info (or detailed info for a single subject)
        - total_count: Total number of subjects
        - displayed_count: Number of subjects returned (limited by limit)
    """
    async def core_logic():
        # Type conversions
        subject_id_int = _parse_int(subject_id, default=None)
        limit_int = _parse_int(limit, default=10)
        offset_int = _parse_int(offset, default=0)
        include_content_bool = bool(include_content)
        
        # --- Build request parameters ---
        params = {}
        endpoint = "/api/knowledge/"
        
        if subject_id_int:
            # Fetch a specific subject by ID
            endpoint = f"{endpoint}{subject_id_int}/"
            logger.info(f"Fetching specific subject with ID: {subject_id_int}")
        else:
            # Fetch list of subjects with pagination
            params["limit"] = str(limit_int)
            params["offset"] = str(offset_int)
            logger.info(f"Fetching subjects list (Limit: {limit_int}, Offset: {offset_int})")
        
        # --- Make API Call ---
        response_data = await api_client.get(endpoint, params=params)
        
        # --- Process Response ---
        if subject_id_int:
            # Single subject response
            if not isinstance(response_data, dict):
                logger.warning(f"Expected dict response for single subject, got {type(response_data)}")
                return {
                    "subjects": [],
                    "total_count": 0,
                    "displayed_count": 0
                }
            
            # Format the single subject response
            subjects = [format_subject(response_data, include_detail=include_content_bool)]
            total_count = 1
        else:
            # List of subjects
            if not isinstance(response_data, dict):
                logger.warning(f"Expected dict response for subjects list, got {type(response_data)}")
                return {
                    "subjects": [],
                    "total_count": 0,
                    "displayed_count": 0
                }
            
            # Get results and count from paginated response
            subjects_data = response_data.get("results", [])
            total_count = response_data.get("count", len(subjects_data))
            
            # Format each subject
            subjects = [format_subject(subject, include_detail=include_content_bool) for subject in subjects_data]
        
        return {
            "subjects": subjects,
            "total_count": total_count,
            "displayed_count": len(subjects)
        }
    
    # Helper function to format a subject
    def format_subject(subject_data, include_detail=False):
        subject_id = subject_data.get("id")
        title = subject_data.get("title", "")
        description = subject_data.get("description", "")
        
        # Basic subject info
        formatted_subject = {
            "id": subject_id,
            "title": title,
        }
        
        # Add additional details if requested
        if include_detail:
            formatted_subject["description"] = description
            
            # Include resource count if available
            resources = subject_data.get("resources", [])
            if isinstance(resources, list):
                formatted_subject["resource_count"] = len(resources)
            
            # Include note count if available
            notes = subject_data.get("notes", [])
            if isinstance(notes, list):
                formatted_subject["note_count"] = len(notes)
        
        return formatted_subject
    
    # Call with error handling wrapper
    return await _handle_api_call("get_subjects", core_logic)

# --- Command Line Arguments ---

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Linko MCP - Access your Linko study notes and resources")
    parser.add_argument("--username", help="Linko email address (overrides environment variable)")
    parser.add_argument("--password", help="Linko password (overrides environment variable)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")
    parser.add_argument("--base-url", help="Linko API base URL (default: https://www.linko.study)")
    return parser.parse_args()

# --- Authentication Check ---

async def check_authentication(cmd_args) -> bool:
    """Check authentication status and authenticate if needed."""
    global api_client
    
    # Set logging level based on verbose flag
    if cmd_args.verbose:
        logging.getLogger('linko_mcp').setLevel(logging.DEBUG)
        logging.getLogger('linko_mcp.auth').setLevel(logging.DEBUG)
        logging.getLogger('linko_mcp.api_client').setLevel(logging.DEBUG)
        logger.debug("Verbose logging enabled")
    
    # Create API client with specified base URL if provided
    api_client = LinkoAPIClient(
        base_url=cmd_args.base_url
    )
    
    # Check for stored token first
    token_data = auth.get_stored_token()
    if token_data and 'access_token' in token_data:
        token = token_data['access_token']
        logger.info("Found stored access token, verifying...")
        
        if await auth.verify_token(token, base_url=cmd_args.base_url):
            logger.info("Stored token is valid.")
            return True
        else:
            logger.warning("Stored token is invalid or expired.")
            
            # Try refreshing token
            logger.info("Attempting to refresh token...")
            new_token = await auth.refresh_access_token(base_url=cmd_args.base_url)
            if new_token:
                logger.info("Token refreshed successfully.")
                return True
            else:
                logger.warning("Token refresh failed, need to re-authenticate.")
    else:
        logger.info("No stored token found.")
    
    # If we get here, we need authentication with username/password
    username = cmd_args.username
    password = cmd_args.password
    
    # If not provided via command line, try environment variables
    if not username or not password:
        env_username, env_password, _ = auth.get_credentials_from_env()
        username = username or env_username
        password = password or env_password
    
    # If still not available, prompt user (only works in interactive mode)
    if not username:
        logger.info("Username not provided via arguments or environment variables.")
        try:
            username = input("Linko email: ")
        except (EOFError, KeyboardInterrupt):
            logger.error("Authentication canceled.")
            return False
    
    if not password:
        logger.info("Password not provided via arguments or environment variables.")
        try:
            password = getpass.getpass("Linko password: ")
        except (EOFError, KeyboardInterrupt):
            logger.error("Authentication canceled.")
            return False
    
    # Attempt authentication
    if not username or not password:
        logger.error("Username and password are required. Please provide via command line arguments, environment variables, or interactive prompt.")
        return False
    
    logger.info(f"Authenticating with username: {username}")
    auth_result = await auth.authenticate(
        username=username,
        password=password,
        base_url=cmd_args.base_url
    )
    
    if auth_result:
        logger.info("Authentication successful.")
        return True
    else:
        logger.error("Authentication failed. Please check your credentials.")
        return False

# --- Startup/Shutdown Functions ---

async def startup(args): 
    """Startup function for the MCP server."""
    logger.info("Starting Linko MCP...")
    
    # Check authentication
    auth_success = await check_authentication(args)
    if not auth_success:
        logger.error("Authentication failed, MCP may not function correctly.")
        # Don't exit - some endpoints might work without auth
    
    # Initialize MCP server
    logger.info("Linko MCP ready to serve requests.")
    return {"status": "started", "authenticated": auth_success}

async def shutdown():
    """Shutdown function for the MCP server."""
    logger.info("Shutting down Linko MCP...")
    
    # Close API client if active
    global api_client
    if api_client:
        await api_client.close()
        logger.info("API client connection closed.")
    
    logger.info("Linko MCP shutdown complete.")
    return {"status": "shutdown"}

# --- Main Entry Point ---

def main():
    """Main entry point for the Linko MCP service."""
    # Parse command line arguments
    args = parse_args()
    
    # Set args in global reference for lifespan to access
    global cmd_args
    cmd_args = args
    
    # Start the MCP server
    sys.exit(mcp.run())

if __name__ == "__main__":
    main() 