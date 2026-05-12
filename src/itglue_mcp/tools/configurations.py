from typing import Annotated, Optional

from fastmcp import FastMCP

from itglue_mcp.client import ITGlueClient, unwrap

_TYPE = "configurations"


def register(mcp: FastMCP, client: ITGlueClient) -> None:

    @mcp.tool()
    async def list_configurations(
        organization_id: Annotated[Optional[str], "Filter by organization ID"] = None,
        filter_name: Annotated[Optional[str], "Filter by configuration name (partial match)"] = None,
        page_number: Annotated[int, "Page number (1-based)"] = 1,
        page_size: Annotated[int, "Results per page (max 1000)"] = 50,
    ) -> dict:
        """List IT Glue configurations (assets)."""
        params: dict = {"page[number]": page_number, "page[size]": page_size}
        if organization_id:
            params["filter[organization-id]"] = organization_id
        if filter_name:
            params["filter[name]"] = filter_name
        return unwrap(await client.get("/configurations", params))

    @mcp.tool()
    async def get_configuration(
        id: Annotated[str, "Configuration ID"],
    ) -> dict:
        """Get a single IT Glue configuration by ID."""
        return unwrap(await client.get(f"/configurations/{id}"))

    @mcp.tool()
    async def create_configuration(
        organization_id: Annotated[str, "Organization ID this configuration belongs to"],
        name: Annotated[str, "Configuration name"],
        configuration_type_id: Annotated[str, "Configuration type ID"],
        hostname: Annotated[Optional[str], "Hostname"] = None,
        primary_ip: Annotated[Optional[str], "Primary IP address"] = None,
        notes: Annotated[Optional[str], "Notes"] = None,
    ) -> dict:
        """Create a new IT Glue configuration (asset)."""
        attrs: dict = {
            "name": name,
            "organization-id": organization_id,
            "configuration-type-id": configuration_type_id,
        }
        if hostname:
            attrs["hostname"] = hostname
        if primary_ip:
            attrs["primary-ip"] = primary_ip
        if notes:
            attrs["notes"] = notes
        payload = {"data": {"type": _TYPE, "attributes": attrs}}
        return unwrap(await client.post("/configurations", payload))

    @mcp.tool()
    async def update_configuration(
        id: Annotated[str, "Configuration ID"],
        name: Annotated[Optional[str], "New name"] = None,
        hostname: Annotated[Optional[str], "New hostname"] = None,
        primary_ip: Annotated[Optional[str], "New primary IP address"] = None,
        notes: Annotated[Optional[str], "New notes"] = None,
    ) -> dict:
        """Update an existing IT Glue configuration."""
        attrs: dict = {}
        if name:
            attrs["name"] = name
        if hostname:
            attrs["hostname"] = hostname
        if primary_ip:
            attrs["primary-ip"] = primary_ip
        if notes:
            attrs["notes"] = notes
        payload = {"data": {"type": _TYPE, "attributes": attrs}}
        return unwrap(await client.patch(f"/configurations/{id}", payload))

    @mcp.tool()
    async def delete_configuration(
        id: Annotated[str, "Configuration ID to delete"],
    ) -> dict:
        """Delete an IT Glue configuration. This action is irreversible."""
        await client.delete(f"/configurations/{id}")
        return {"deleted": True, "id": id}
