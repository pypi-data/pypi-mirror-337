import asyncio
from dataclasses import dataclass
from typing import Dict, List, Any
from urllib.parse import urlparse

import click
import httpx
import mcp.types as types
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions
from mcp.shared.exceptions import McpError
import mcp.server.stdio

SENTRY_API_BASE = "https://new-sentry.devops.xiaohongshu.com/api/0/"
MISSING_AUTH_TOKEN_MESSAGE = (
    """Sentry authentication token not found. Please specify your Sentry auth token."""
)


@dataclass
class SentryTagData:
    issue_id: str
    tags: Dict[str, List[str]]

    def to_text(self) -> str:
        text = f"\nSentry Tags for Issue {self.issue_id}:\n"
        for key, values in self.tags.items():
            text += f"\n{key}:\n"
            for value in values:
                text += f"  - {value}\n"
        return text

    def to_prompt_result(self) -> types.GetPromptResult:
        return types.GetPromptResult(
            description=f"Sentry Tags for Issue {self.issue_id}",
            messages=[
                types.PromptMessage(
                    role="user", content=types.TextContent(type="text", text=self.to_text())
                )
            ],
        )

    def to_tool_result(self) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
        return [types.TextContent(type="text", text=self.to_text())]

@dataclass
class SentryIssueData:
    title: str
    issue_id: str
    status: str
    level: str
    first_seen: str
    last_seen: str
    count: int
    stacktrace: str

    def to_text(self) -> str:
        return f"""
Sentry Issue: {self.title}
Issue ID: {self.issue_id}
Status: {self.status}
Level: {self.level}
First Seen: {self.first_seen}
Last Seen: {self.last_seen}
Event Count: {self.count}

{self.stacktrace}
        """

    def to_prompt_result(self) -> types.GetPromptResult:
        return types.GetPromptResult(
            description=f"Sentry Issue: {self.title}",
            messages=[
                types.PromptMessage(
                    role="user", content=types.TextContent(type="text", text=self.to_text())
                )
            ],
        )

    def to_tool_result(self) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
        return [types.TextContent(type="text", text=self.to_text())]


class SentryError(Exception):
    pass


def extract_issue_id(issue_id_or_url: str) -> str:
    """
    Extracts the Sentry issue ID from either a full URL or a standalone ID.

    This function validates the input and returns the numeric issue ID.
    It raises SentryError for invalid inputs, including empty strings,
    non-Sentry URLs, malformed paths, and non-numeric IDs.
    """
    if not issue_id_or_url:
        raise SentryError("Missing issue_id_or_url argument")

    if issue_id_or_url.startswith(("http://", "https://")):
        parsed_url = urlparse(issue_id_or_url)
        if not parsed_url.hostname or not parsed_url.hostname.endswith(".sentry.io"):
            raise SentryError("Invalid Sentry URL. Must be a URL ending with .sentry.io")

        path_parts = parsed_url.path.strip("/").split("/")
        if len(path_parts) < 2 or path_parts[0] != "issues":
            raise SentryError(
                "Invalid Sentry issue URL. Path must contain '/issues/{issue_id}'"
            )

        issue_id = path_parts[-1]
    else:
        issue_id = issue_id_or_url

    if not issue_id.isdigit():
        raise SentryError("Invalid Sentry issue ID. Must be a numeric value.")

    return issue_id


def create_stacktrace(latest_event: dict) -> str:
    """
    Creates a formatted stacktrace string from the latest Sentry event.

    This function extracts exception information and stacktrace details from the
    provided event dictionary, formatting them into a human-readable string.
    It handles multiple exceptions and includes file, line number, and function
    information for each frame in the stacktrace.

    Args:
        latest_event (dict): A dictionary containing the latest Sentry event data.

    Returns:
        str: A formatted string containing the stacktrace information,
             or "No stacktrace found" if no relevant data is present.
    """
    stacktraces = []
    for entry in latest_event.get("entries", []):
        if entry["type"] != "exception":
            continue

        exception_data = entry["data"]["values"]
        for exception in exception_data:
            exception_type = exception.get("type", "Unknown")
            exception_value = exception.get("value", "")
            stacktrace = exception.get("stacktrace")

            stacktrace_text = f"Exception: {exception_type}: {exception_value}\n\n"
            if stacktrace:
                stacktrace_text += "Stacktrace:\n"
                for frame in stacktrace.get("frames", []):
                    filename = frame.get("filename", "Unknown")
                    lineno = frame.get("lineNo", "?")
                    function = frame.get("function", "Unknown")

                    stacktrace_text += f"{filename}:{lineno} in {function}\n"

                    if "context" in frame:
                        context = frame["context"]
                        for ctx_line in context:
                            stacktrace_text += f"    {ctx_line[1]}\n"

                    stacktrace_text += "\n"

            stacktraces.append(stacktrace_text)

    return "\n".join(stacktraces) if stacktraces else "No stacktrace found"


async def handle_sentry_tags(
    http_client: httpx.AsyncClient, auth_token: str, issue_id_or_url: str
) -> SentryTagData:
    try:
        issue_id = extract_issue_id(issue_id_or_url)

        # Get issue tags
        response = await http_client.get(
            f"issues/{issue_id}/tags/",
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        if response.status_code == 401:
            raise McpError(
                "Error: Unauthorized. Please check your MCP_SENTRY_AUTH_TOKEN token."
            )
        response.raise_for_status()
        tags_data = response.json()

        # Process tags data
        tags = {}
        for tag in tags_data:
            tag_key = tag.get("key", "unknown")
            tag_values = [entry.get("value") for entry in tag.get("topValues", [])]
            if tag_values:
                tags[tag_key] = tag_values

        return SentryTagData(
            issue_id=issue_id,
            tags=tags
        )

    except SentryError as e:
        raise McpError(str(e))
    except httpx.HTTPStatusError as e:
        raise McpError(f"Error fetching Sentry tags: {str(e)}")
    except Exception as e:
        raise McpError(f"An error occurred: {str(e)}")

async def handle_sentry_issue(
    http_client: httpx.AsyncClient, auth_token: str, issue_id_or_url: str
) -> SentryIssueData:
    try:
        issue_id = extract_issue_id(issue_id_or_url)

        response = await http_client.get(
            f"issues/{issue_id}/", headers={"Authorization": f"Bearer {auth_token}"}
        )
        if response.status_code == 401:
            raise McpError(
                "Error: Unauthorized. Please check your MCP_SENTRY_AUTH_TOKEN token."
            )
        response.raise_for_status()
        issue_data = response.json()

        # Get issue hashes
        hashes_response = await http_client.get(
            f"issues/{issue_id}/hashes/",
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        hashes_response.raise_for_status()
        hashes = hashes_response.json()

        if not hashes:
            raise McpError("No Sentry events found for this issue")

        latest_event = hashes[0]["latestEvent"]
        stacktrace = create_stacktrace(latest_event)

        return SentryIssueData(
            title=issue_data["title"],
            issue_id=issue_id,
            status=issue_data["status"],
            level=issue_data["level"],
            first_seen=issue_data["firstSeen"],
            last_seen=issue_data["lastSeen"],
            count=issue_data["count"],
            stacktrace=stacktrace
        )

    except SentryError as e:
        raise McpError(str(e))
    except httpx.HTTPStatusError as e:
        raise McpError(f"Error fetching Sentry issue: {str(e)}")
    except Exception as e:
        raise McpError(f"An error occurred: {str(e)}")


@dataclass
class SentryStatsData:
    issue_id: str
    stat_type: str
    stats: Dict[str, Any]

    def to_text(self) -> str:
        text = f"\nSentry Stats for Issue {self.issue_id} (by {self.stat_type}):\n"
        
        if self.stat_type == "release":
            text += "\nEvents by Release:\n"
            for release, count in self.stats.items():
                text += f"  {release}: {count} events\n"
        elif self.stat_type == "24h":
            text += "\nEvents in last 24 hours:\n"
            for timestamp, count in self.stats.items():
                text += f"  {timestamp}: {count} events\n"
        else:
            text += "\nEvents by Category:\n"
            for category, count in self.stats.items():
                text += f"  {category}: {count} events\n"
        
        return text

    def to_prompt_result(self) -> types.GetPromptResult:
        return types.GetPromptResult(
            description=f"Sentry Stats for Issue {self.issue_id}",
            messages=[
                types.PromptMessage(
                    role="user", content=types.TextContent(type="text", text=self.to_text())
                )
            ],
        )

    def to_tool_result(self) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
        return [types.TextContent(type="text", text=self.to_text())]


async def handle_sentry_stats(
    http_client: httpx.AsyncClient, 
    auth_token: str, 
    issue_id_or_url: str,
    stat_type: str = "release"
) -> SentryStatsData:
    """
    Retrieve statistics for a Sentry issue.
    
    Args:
        http_client: The HTTP client to use for requests
        auth_token: Sentry authentication token
        issue_id_or_url: The Sentry issue ID or URL
        stat_type: Type of stats to retrieve. Can be:
            - "release": Group events by release version
            - "24h": Events in the last 24 hours
            - "os": Group by operating system
            - "device": Group by device
            - "status": Group by event status
    
    Returns:
        SentryStatsData containing the requested statistics
    """
    try:
        issue_id = extract_issue_id(issue_id_or_url)
        
        # 获取统计数据
        response = await http_client.get(
            f"issues/{issue_id}/stats/",
            params={"stat": stat_type, "period": "14d"},
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        
        if response.status_code == 401:
            raise McpError(
                "Error: Unauthorized. Please check your MCP_SENTRY_AUTH_TOKEN token."
            )
        response.raise_for_status()
        
        stats_data = response.json()
        
        return SentryStatsData(
            issue_id=issue_id,
            stat_type=stat_type,
            stats=stats_data
        )
        
    except SentryError as e:
        raise McpError(str(e))
    except httpx.HTTPStatusError as e:
        raise McpError(f"Error fetching Sentry stats: {str(e)}")
    except Exception as e:
        raise McpError(f"An error occurred: {str(e)}")


async def serve(auth_token: str) -> Server:
    server = Server("sentry")
    http_client = httpx.AsyncClient(base_url=SENTRY_API_BASE)

    @server.list_prompts()
    async def handle_list_prompts() -> list[types.Prompt]:
        return [
            types.Prompt(
                name="sentry-issue",
                description="Retrieve a Sentry issue by ID or URL",
                arguments=[
                    types.PromptArgument(
                        name="issue_id_or_url",
                        description="Sentry issue ID or URL",
                        required=True,
                    )
                ],
            ),
            types.Prompt(
                name="sentry-tags",
                description="Retrieve tags for a Sentry issue by ID or URL",
                arguments=[
                    types.PromptArgument(
                        name="issue_id_or_url",
                        description="Sentry issue ID or URL",
                        required=True,
                    )
                ],
            )
        ]

    @server.get_prompt()
    async def handle_get_prompt(
        name: str, arguments: dict[str, str] | None
    ) -> types.GetPromptResult:
        if name == "sentry-issue":
            issue_id_or_url = (arguments or {}).get("issue_id_or_url", "")
            issue_data = await handle_sentry_issue(http_client, auth_token, issue_id_or_url)
            return issue_data.to_prompt_result()
        elif name == "sentry-tags":
            issue_id_or_url = (arguments or {}).get("issue_id_or_url", "")
            tags_data = await handle_sentry_tags(http_client, auth_token, issue_id_or_url)
            return tags_data.to_prompt_result()
        else:
            raise ValueError(f"Unknown prompt: {name}")

    @server.list_tools()
    async def handle_list_tools() -> list[types.Tool]:
        return [
            types.Tool(
                name="get_sentry_issue",
                description="""Retrieve and analyze a Sentry issue by ID or URL. Use this tool when you need to:
                - Investigate production errors and crashes
                - Access detailed stacktraces from Sentry
                - Analyze error patterns and frequencies
                - Get information about when issues first/last occurred
                - Review error counts and status""",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "issue_id_or_url": {
                            "type": "string",
                            "description": "Sentry issue ID or URL to analyze"
                        }
                    },
                    "required": ["issue_id_or_url"]
                }
            ),
            types.Tool(
                name="get_sentry_tags",
                description="""Retrieve and analyze tags for a Sentry issue by ID or URL. Use this tool when you need to:
                - View all tags associated with an issue
                - Analyze error patterns by tag values
                - Get device, OS, app version information
                - Review user segments affected by the issue""",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "issue_id_or_url": {
                            "type": "string",
                            "description": "Sentry issue ID or URL to analyze"
                        }
                    },
                    "required": ["issue_id_or_url"]
                }
            ),
            types.Tool(
                name="get_sentry_stats",
                description="""Retrieve and analyze statistics for a Sentry issue by ID or URL. Use this tool when you need to:
                - Track event frequency over time
                - Analyze event distribution across releases
                - Monitor issue trends
                - Identify spikes in error occurrences
                - Compare impact across different versions""",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "issue_id_or_url": {
                            "type": "string",
                            "description": "Sentry issue ID or URL to analyze"
                        },
                        "stat_type": {
                            "type": "string",
                            "description": "Type of statistics to retrieve (release, 24h, os, device, status)",
                            "enum": ["release", "24h", "os", "device", "status"],
                            "default": "release"
                        }
                    },
                    "required": ["issue_id_or_url"]
                }
            )
        ]

    @server.call_tool()
    async def handle_call_tool(
        name: str, arguments: dict | None
    ) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
        if name == "get_sentry_issue":
            issue_id_or_url = (arguments or {}).get("issue_id_or_url", "")
            issue_data = await handle_sentry_issue(http_client, auth_token, issue_id_or_url)
            return issue_data.to_tool_result()
        elif name == "get_sentry_tags":
            issue_id_or_url = (arguments or {}).get("issue_id_or_url", "")
            tags_data = await handle_sentry_tags(http_client, auth_token, issue_id_or_url)
            return tags_data.to_tool_result()
        elif name == "get_sentry_stats":
            issue_id_or_url = (arguments or {}).get("issue_id_or_url", "")
            stat_type = (arguments or {}).get("stat_type", "release")
            stats_data = await handle_sentry_stats(http_client, auth_token, issue_id_or_url, stat_type)
            return stats_data.to_tool_result()
        else:
            raise ValueError(f"Unknown tool: {name}")

    return server

@click.command()
@click.option(
    "--auth-token",
    envvar="SENTRY_TOKEN",
    required=True,
    help="Sentry authentication token",
)
def main(auth_token: str):
    async def _run():
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            server = await serve(auth_token)
            await server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="sentry",
                    server_version="0.4.1",
                    capabilities=server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={},
                    ),
                ),
            )
    asyncio.run(_run())
