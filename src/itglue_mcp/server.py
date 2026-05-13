from fastmcp import FastMCP

from itglue_mcp.client import ITGlueClient
from itglue_mcp.tools import configurations, documents, flexible_assets, organizations

mcp = FastMCP("IT Glue")
_client = ITGlueClient()

organizations.register(mcp, _client)
configurations.register(mcp, _client)
documents.register(mcp, _client)
flexible_assets.register(mcp, _client)


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
