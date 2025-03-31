from unittest.mock import MagicMock
import asyncio
from typing import Optional, Set
from qink.lib.core_api_client import (
    CoreAPIClient,
    CoreAPIConfig,
    Org,
    Processor,
)


class TCPProxy:
    """A general TCP proxy server for testing purposes."""

    def __init__(
        self, target_host: str, target_port: int, listen_port: int = 0
    ):
        self.target_host = target_host
        self.target_port = target_port
        self.listen_port = listen_port
        self.server: Optional[asyncio.AbstractServer] = None
        self._tasks: Set[asyncio.Task] = set()
        self._connections: Set[asyncio.StreamWriter] = set()

    async def _handle_client(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ) -> None:
        server_reader, server_writer = await asyncio.open_connection(
            self.target_host, self.target_port
        )

        async def forward(reader, writer):
            try:
                while data := await reader.read(1024):
                    writer.write(data)
                    await writer.drain()
            except Exception as e:
                print("Connection dropped:", e)
            finally:
                writer.close()

        self._connections.add(writer)

        task = asyncio.gather(
            forward(reader, server_writer),
            forward(server_reader, writer),
        )

        self._tasks.add(task)

        await task

    async def _proxy_data(
        self,
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter,
        direction: str,
    ) -> None:
        """Proxy data in one direction."""
        try:
            while True:
                data = await reader.read(8192)  # 8KB chunks
                if not data:
                    break
                writer.write(data)
                await writer.drain()
        except asyncio.CancelledError:
            pass
        except Exception as e:
            print(f"Error in {direction}: {e}")

    async def start(self) -> int:
        """Start the proxy server and return the actual port it's
        listening on."""
        self.server = await asyncio.start_server(
            self._handle_client, "localhost", self.listen_port
        )
        return self.server.sockets[0].getsockname()[1]

    async def stop(self):
        """Stop the proxy server and all connections."""
        if self.server:
            # Close all client connections
            for writer in self._connections.copy():
                writer.close()
                try:
                    await writer.wait_closed()
                except Exception:
                    pass

            # Close the server
            self.server.close()

            # Cancel all tasks
            for task in self._tasks:
                task.cancel()

            # Wait for tasks to complete
            if self._tasks:
                await asyncio.gather(*self._tasks, return_exceptions=True)

            # Wait for server to close with timeout
            try:
                await asyncio.wait_for(self.server.wait_closed(), timeout=1.0)
            except asyncio.TimeoutError:
                print("Warning: Server close timed out")

            # Clear all sets
            self._tasks.clear()
            self._connections.clear()


class MockCoreAPIClient(CoreAPIClient):
    """Mock CoreAPIClient that returns predefined data."""

    def __init__(
        self,
        config: CoreAPIConfig,
        orgs: list[Org],
        processors: list[Processor],
    ):
        super().__init__(config)
        self._orgs = orgs
        self._processors = processors
        self._session = MagicMock()

    async def get_orgs(self) -> list[Org]:
        return self._orgs

    async def get_processors(self) -> list[Processor]:
        return self._processors
