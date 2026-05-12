from typing import Annotated, Optional

from fastmcp import FastMCP

from itglue_mcp.client import ITGlueClient, unwrap

_TYPE = "documents"


def register(mcp: FastMCP, client: ITGlueClient) -> None:

    @mcp.tool()
    async def list_documents(
        organization_id: Annotated[Optional[str], "Filter by organization ID"] = None,
        filter_name: Annotated[Optional[str], "Filter by document name (partial match)"] = None,
        page_number: Annotated[int, "Page number (1-based)"] = 1,
        page_size: Annotated[int, "Results per page (max 1000)"] = 50,
    ) -> dict:
        """List IT Glue documents."""
        params: dict = {"page[number]": page_number, "page[size]": page_size}
        if organization_id:
            params["filter[organization-id]"] = organization_id
        if filter_name:
            params["filter[name]"] = filter_name
        return unwrap(await client.get("/documents", params))

    @mcp.tool()
    async def get_document(
        id: Annotated[str, "Document ID"],
    ) -> dict:
        """Get a single IT Glue document by ID."""
        return unwrap(await client.get(f"/documents/{id}"))

    @mcp.tool()
    async def create_document(
        organization_id: Annotated[str, "Organization ID this document belongs to"],
        name: Annotated[str, "Document name / title"],
        content: Annotated[Optional[str], "Initial text content for the document body"] = None,
    ) -> dict:
        """Create a new IT Glue document and optionally populate its body."""
        doc_payload = {
            "data": {
                "type": _TYPE,
                "attributes": {
                    "organization-id": organization_id,
                    "name": name,
                },
            }
        }
        doc = unwrap(await client.post("/documents", doc_payload))
        doc_id = doc.get("id") if isinstance(doc, dict) else doc[0].get("id")

        if content and doc_id:
            section_payload = {
                "data": {
                    "type": "document_contents",
                    "attributes": {
                        "document-id": doc_id,
                        "content": content,
                    },
                }
            }
            await client.post(f"/documents/{doc_id}/document_contents", section_payload)

        return doc

    @mcp.tool()
    async def update_document(
        id: Annotated[str, "Document ID"],
        name: Annotated[Optional[str], "New document name / title"] = None,
    ) -> dict:
        """Update an IT Glue document's metadata (name/title)."""
        attrs: dict = {}
        if name:
            attrs["name"] = name
        payload = {"data": {"type": _TYPE, "attributes": attrs}}
        return unwrap(await client.patch(f"/documents/{id}", payload))

    @mcp.tool()
    async def delete_document(
        id: Annotated[str, "Document ID to delete"],
    ) -> dict:
        """Delete an IT Glue document. This action is irreversible."""
        await client.delete(f"/documents/{id}")
        return {"deleted": True, "id": id}
