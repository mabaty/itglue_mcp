from typing import Annotated, Optional

from fastmcp import FastMCP

from itglue_mcp.client import ITGlueClient, unwrap

_TYPE = "organizations"


def register(mcp: FastMCP, client: ITGlueClient) -> None:

    @mcp.tool()
    async def list_organizations(
        filter_name: Annotated[Optional[str], "Filter by organization name (partial match)"] = None,
        page_number: Annotated[int, "Page number (1-based)"] = 1,
        page_size: Annotated[int, "Results per page (max 1000)"] = 50,
    ) -> dict:
        """List IT Glue organizations."""
        params: dict = {"page[number]": page_number, "page[size]": page_size}
        if filter_name:
            params["filter[name]"] = filter_name
        return unwrap(await client.get("/organizations", params))

    @mcp.tool()
    async def get_organization(
        id: Annotated[str, "Organization ID"],
    ) -> dict:
        """Get a single IT Glue organization by ID."""
        return unwrap(await client.get(f"/organizations/{id}"))

    @mcp.tool()
    async def create_organization(
        name: Annotated[str, "Organization name"],
        short_name: Annotated[Optional[str], "Short name / abbreviation"] = None,
        description: Annotated[Optional[str], "Description"] = None,
    ) -> dict:
        """Create a new IT Glue organization."""
        attrs: dict = {"name": name}
        if short_name:
            attrs["short-name"] = short_name
        if description:
            attrs["description"] = description
        payload = {"data": {"type": _TYPE, "attributes": attrs}}
        return unwrap(await client.post("/organizations", payload))

    @mcp.tool()
    async def update_organization(
        id: Annotated[str, "Organization ID"],
        name: Annotated[Optional[str], "New name"] = None,
        short_name: Annotated[Optional[str], "New short name"] = None,
        description: Annotated[Optional[str], "New description"] = None,
    ) -> dict:
        """Update an existing IT Glue organization."""
        attrs: dict = {}
        if name:
            attrs["name"] = name
        if short_name:
            attrs["short-name"] = short_name
        if description:
            attrs["description"] = description
        payload = {"data": {"type": _TYPE, "attributes": attrs}}
        return unwrap(await client.patch(f"/organizations/{id}", payload))
