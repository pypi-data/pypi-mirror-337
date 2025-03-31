from __future__ import annotations

import asyncio

from typing import Any, Callable, Set, Tuple

from pydantic import ValidationError
from websockets.asyncio.server import ServerConnection, serve
from websockets.exceptions import ConnectionClosed

from .update import Position, Update, UpdatePacket

from datetime import datetime


class UpdateServer:
    handle_incoming_update: Callable[[Update], None]
    get_at_position: Callable[[Position], Any]
    update_queue: asyncio.Queue[UpdatePacket]
    stop_event: asyncio.Event
    connections: Set[ServerConnection]
    port: int = 8765

    def __init__(
        self,
        get_at_position: Callable[[Position], Any],
        handle_incoming_update: Callable[[Update], None],
    ):
        self.get_at_position = get_at_position
        self.handle_incoming_update = handle_incoming_update
        self.update_queue = asyncio.Queue()
        self.stop_event = asyncio.Event()
        self.connections = set()
        self.recv_task = None
        self.send_task = None

    async def handle_recieve(self, websocket):
        if websocket not in self.connections:
            self.connections.add(websocket)

        root_position = Position([])
        root_value = self.get_at_position(root_position)
        root_update = Update(timestamp=datetime.now(),
                             position=root_position, data=root_value)
        root_update_packet = UpdatePacket.from_update(root_update)
        await websocket.send(root_update_packet.json())

        try:
            while True:
                data = await websocket.recv()
                try:
                    update_pkt = UpdatePacket.from_json(data)
                    update = UpdatePacket.to_update(update_pkt)
                    self.handle_incoming_update(update)
                except ValidationError:
                    continue
        except asyncio.CancelledError:
            pass
        except ConnectionClosed as e:
            pass
        except Exception as e:
            print(f"Error in handle_recieve: {e}")
        finally:
            if websocket in self.connections:
                self.connections.remove(websocket)

    async def start_recieve(self):
        async with serve(self.handle_recieve, "localhost", self.port) as server:
            await self.stop_event.wait()
            for websocket in self.connections:
                await websocket.close()
            self.connections.clear()
            server.close()

    def add_update(self, update: Update):
        json_update = UpdatePacket.from_update(update)
        self.update_queue.put_nowait(json_update)

    async def start_send(self):
        while not self.stop_event.is_set():
            try:
                update = await asyncio.wait_for(self.update_queue.get(), timeout=0.1)
                assert isinstance(update, UpdatePacket)
                for websocket in self.connections:
                    await websocket.send(update.json())
            except asyncio.TimeoutError:
                pass

    async def start(self):
        self.recv_task = asyncio.create_task(self.start_recieve())
        self.send_task = asyncio.create_task(self.start_send())

    async def shutdown(self):
        self.stop_event.set()
        if self.recv_task:
            await self.recv_task
        if self.send_task:
            await self.send_task
