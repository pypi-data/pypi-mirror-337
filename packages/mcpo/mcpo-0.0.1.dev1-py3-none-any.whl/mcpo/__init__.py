import sys
import asyncio
import typer
from typing_extensions import Annotated
from typing import Optional, List

app = typer.Typer()


@app.command(
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True}
)
def main(
    ctx: typer.Context,
    host: Annotated[
        Optional[str],
        typer.Option("--host", "-H", help="Host to bind the server to."),
    ] = "0.0.0.0",
    port: Annotated[
        Optional[int],
        typer.Option("--port", "-p", help="Port to bind the server to."),
    ] = 8080,
):
    # Find the position of "--"
    if "--" not in sys.argv:
        typer.echo("Usage: mcpo --host 0.0.0.0 --port 8000 -- your_mcp_command")
        raise typer.Exit(1)

    idx = sys.argv.index("--")
    server_command: List[str] = sys.argv[idx + 1 :]

    if not server_command:
        typer.echo("Error: You must specify the MCP server command after '--'")
        raise typer.Exit(1)

    from mcpo.main import run

    # Run your async run function from mcpo.main
    asyncio.run(run(host, port, server_command))


if __name__ == "__main__":
    app()
