from typing import Annotated, Any, Optional

from fastmcp import FastMCP

from itglue_mcp.client import ITGlueClient, unwrap

_TYPE = "flexible_assets"


def register(mcp: FastMCP, client: ITGlueClient) -> None:

    @mcp.tool()
    async def list_flexible_asset_types(
        page_number: Annotated[int, "Page number (1-based)"] = 1,
        page_size: Annotated[int, "Results per page (max 1000)"] = 50,
    ) -> dict:
        """List all flexible asset type definitions in IT Glue."""
        params = {"page[number]": page_number, "page[size]": page_size}
        return unwrap(await client.get("/flexible_asset_types", params))

    @mcp.tool()
    async def list_flexible_assets(
        flexible_asset_type_id: Annotated[str, "Flexible asset type ID to query"],
        organization_id: Annotated[Optional[str], "Filter by organization ID"] = None,
        page_number: Annotated[int, "Page number (1-based)"] = 1,
        page_size: Annotated[int, "Results per page (max 1000)"] = 50,
    ) -> dict:
        """List flexible assets of a given type."""
        params: dict = {
            "filter[flexible_asset_type_id]": flexible_asset_type_id,
            "page[number]": page_number,
            "page[size]": page_size,
        }
        if organization_id:
            params["filter[organization_id]"] = organization_id
        return unwrap(await client.get("/flexible_assets", params))

    @mcp.tool()
    async def get_flexible_asset(
        id: Annotated[str, "Flexible asset ID"],
    ) -> dict:
        """Get a single IT Glue flexible asset by ID."""
        return unwrap(await client.get(f"/flexible_assets/{id}"))

    @mcp.tool()
    async def create_flexible_asset(
        flexible_asset_type_id: Annotated[str, "Flexible asset type ID"],
        organization_id: Annotated[str, "Organization ID"],
        traits: Annotated[dict[str, Any], "Key-value pairs matching the asset type's field names"],
    ) -> dict:
        """Create a new IT Glue flexible asset."""
        payload = {
            "data": {
                "type": _TYPE,
                "attributes": {
                    "flexible-asset-type-id": flexible_asset_type_id,
                    "organization-id": organization_id,
                    "traits": traits,
                },
            }
        }
        return unwrap(await client.post("/flexible_assets", payload))

    @mcp.tool()
    async def update_flexible_asset(
        id: Annotated[str, "Flexible asset ID"],
        traits: Annotated[dict[str, Any], "Updated key-value trait pairs"],
    ) -> dict:
        """Update traits on an existing IT Glue flexible asset."""
        payload = {
            "data": {
                "type": _TYPE,
                "attributes": {"traits": traits},
            }
        }
        return unwrap(await client.patch(f"/flexible_assets/{id}", payload))

    @mcp.tool()
    async def delete_flexible_asset(
        id: Annotated[str, "Flexible asset ID to delete"],
    ) -> dict:
        """Delete an IT Glue flexible asset. This action is irreversible."""
        await client.delete(f"/flexible_assets/{id}")
        return {"deleted": True, "id": id}
