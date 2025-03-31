from __future__ import annotations

from datetime import datetime
from typing import Any, Callable, Union
import asyncio

from .update import Position, Update, UpdatePacket
from .update_server import UpdateServer

Indexable = Union[dict, list]


class Object:
    position: Position
    object_server: ObjectServer

    def __init__(self, object_server: ObjectServer, position: Position):
        self.position = position
        self.object_server = object_server

    def __getitem__(self, name: str) -> Any:
        position = self.position + name
        value = self.object_server.get_at_position(position)
        if value is Indexable:
            return Object(self.object_server, self.position + name)
        else:
            return value

    def __setitem__(self, name: str, value: Any) -> None:
        position = self.position + name
        self.object_server.set_at_position(position, value)
        update = Update(timestamp=datetime.now(),
                        position=position, data=value)
        self.object_server.add_update(update)


class ObjectServer:
    add_update_to_server: Callable[[Update], None]

    def __init__(self, data={}):
        self.data = data
        self.update_server = UpdateServer(
            get_at_position=self.get_at_position,
            handle_incoming_update=self.handle_incoming_update,
        )
        self.root = Object(object_server=self, position=Position([]))
        self._started = False

    async def start(self):
        if not self._started:
            await self.update_server.start()
            self._started = True

    async def stop(self):
        if self._started:
            await self.update_server.shutdown()
            self._started = False

    def __del__(self):
        if self._started:
            asyncio.create_task(self.stop())

    def __repr__(self):
        return self.data.__repr__()

    def get_at_position(self, position: Position) -> Any:
        if position.depth() == 0:
            return self.data
        current = self.data
        for key in position[:-1]:
            current = current[key]
        return current[position[-1]]

    def handle_incoming_update(self, update: Update):
        self.set_at_position(update.position, update.data)

    def set_at_position(self, position: Position, value: Any):
        current = self.data
        for key in position[:-1]:
            try:
                current = current[key]
            except KeyError:
                current[key] = {}
                current = current[key]
        current[position[-1]] = value

    def set_at_position_update(self, position: Position, value: Any):
        self.set_at_position(position, value)
        self.add_update(Update(timestamp=datetime.now(),
                        position=position, data=value))

    def add_update(self, update: Update) -> None:
        print("Calling add_update")
        self.update_server.add_update(update)

    def __getitem__(self, name: str) -> Any:
        return self.root[name]

    def __setitem__(self, name: str, value: Any) -> None:
        self.root[name] = value
