"""Circuit tools for Nautobot MCP."""

from asgiref.sync import sync_to_async
from nautobot_mcp.tools.registry import register_tool
from nautobot.circuits.models import Circuit


@register_tool
async def get_circuit_by_id(cid: str) -> str:
    """Get circuit by CID."""

    @sync_to_async
    def get_circuit_sync(cid):
        try:
            circuit = Circuit.objects.get(cid=cid)
            return (
                f"Circuit ID: {circuit.cid}\n"
                f"Provider: {circuit.provider}\n"
                f"Type: {circuit.type}\n"
                f"Status: {circuit.status}"
            )
        except Circuit.DoesNotExist:
            return f"Circuit with ID '{cid}' not found."

    return await get_circuit_sync(cid)
