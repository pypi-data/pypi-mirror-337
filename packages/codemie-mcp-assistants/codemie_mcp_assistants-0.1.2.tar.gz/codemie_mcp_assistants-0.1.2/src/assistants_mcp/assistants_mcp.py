import os
import uuid
from typing import Any, Dict, List, Optional

from codemie_sdk import CodeMieClient
from codemie_sdk.models.assistant import (
    AssistantChatRequest,
    ChatMessage,
    ChatRole,
)
from mcp.server.fastmcp import FastMCP

DEFAULT_AUTH_CLIENT_ID = "codemie-sdk"
DEFAULT_AUTH_REALM_NAME = "codemie-prod"
DEFAULT_AUTH_SERVER_URL = (
    "https://keycloak.eks-core.aws.main.edp.projects.epam.com/auth"
)
DEFAULT_CODEMIE_API_DOMAIN = "https://codemie.lab.epam.com/code-assistant-api"

# Initialize FastMCP server
mcp = FastMCP("codemie-assistants")

# Client instance
_client: Optional[CodeMieClient] = None


def get_client() -> CodeMieClient:
    """Gets authenticated CodeMie client instance."""
    username = os.getenv("CODEMIE_USERNAME")
    password = os.getenv("CODEMIE_PASSWORD")
    auth_client_id = os.getenv("CODEMIE_AUTH_CLIENT_ID", DEFAULT_AUTH_CLIENT_ID)
    auth_realm_name = os.getenv("CODEMIE_AUTH_REALM_NAME", DEFAULT_AUTH_REALM_NAME)
    auth_server_url = os.getenv("CODEMIE_AUTH_SERVER_URL", DEFAULT_AUTH_SERVER_URL)
    codemie_api_domain = os.getenv("CODEMIE_API_DOMAIN", DEFAULT_CODEMIE_API_DOMAIN)

    if not username or not password:
        raise ValueError(
            "Username and password must be set via environment variables: CODEMIE_USERNAME, CODEMIE_PASSWORD"
        )

    return CodeMieClient(
        username=username,
        password=password,
        verify_ssl=False,
        auth_client_id=auth_client_id,
        auth_realm_name=auth_realm_name,
        auth_server_url=auth_server_url,
        codemie_api_domain=codemie_api_domain,
    )


@mcp.tool()
async def get_tools() -> List[Dict[str, Any]]:
    """Get available tools for assistants."""
    try:
        print("Getting tools")
        client = get_client()
        if client.token is None:
            raise ValueError("Client not initialized")
        toolkits = client.assistants.get_tools()

        # Convert to dict format for better visualization
        tools_list = []
        for toolkit in toolkits:
            tools_list.extend(
                [
                    {
                        "toolkit": toolkit.toolkit,
                        "tool": tool.name,
                        "label": tool.label or tool.name,
                        "settings_required": tool.settings_config,
                    }
                    for tool in toolkit.tools
                ]
            )

        return tools_list
    except Exception as e:
        print(f"Error getting tools: {str(e)}")
        raise e


@mcp.tool()
async def get_assistants(
    minimal: bool = True, project: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Get list of available assistants.

    Args:
        minimal: Return minimal info (default: True)
        project: Filter by project name
    """
    client = get_client()
    filters = {"project": project} if project else None

    assistants = client.assistants.list(minimal_response=minimal, filters=filters)

    # Convert to dict format
    return [
        {
            "id": asst.id,
            "name": asst.name,
            "description": asst.description,
            "project": getattr(asst, "project", None) if not minimal else None,
        }
        for asst in assistants
    ]


@mcp.tool()
async def chat_with_assistant(
    message: str,
    assistant_id: str,
    conversation_id: Optional[str] = None,
    history: Optional[List[Dict[str, str]]] = None,
) -> str:
    """Chat with a specific assistant.

    Args:
        message: User message
        assistant_id: ID of the assistant to chat with
        conversation_id: Optional conversation ID
        history: Optional chat history as list of dicts with role and message
    """
    client = get_client()

    # Convert history to ChatMessage objects if provided
    chat_history = []
    if history:
        for msg in history:
            chat_history.append(
                ChatMessage(role=ChatRole(msg["role"]), message=msg["message"])
            )

    # Create chat request
    request = AssistantChatRequest(
        text=message,
        conversation_id=conversation_id if conversation_id else str(uuid.uuid4()),
        history=chat_history,
        stream=False,  # For now using non-streaming responses
    )

    # Send chat request
    response = client.assistants.chat(assistant_id=assistant_id, request=request)

    return response.generated


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport="stdio")
