import asyncio
from typing import Any, Callable

from ..abc.listener import AbstractListenerMixin
from ..abc.queue import AbstractQueueMixin
from ..models import Listener, BaseFilter, QueueHandler, Queue
from ..exceptions import (
    FilterException,
    ListenerAlreadyExistsError,
    NotFoundHandlerException,
)


class ListenerMixin(AbstractListenerMixin, AbstractQueueMixin):
    __listeners: list[Listener] = []

    @property
    def listeners(self) -> list[Listener]:
        return self.__listeners

    def listener(self, queue_name: str, *filters: BaseFilter):
        """Add a listener to the queue."""

        def decorator(func: Callable[..., Any]):
            listener_exists = False
            for listener in self.listeners:
                if listener.queue_name == queue_name:
                    for handler in listener.handlers:
                        if handler.func.__name__ == func.__name__:
                            raise ListenerAlreadyExistsError(
                                f"Listener {func.__name__} already exists."
                            )
                    listener.handlers.append(QueueHandler(func, list(filters)))
                    listener_exists = True
                    break

            if not listener_exists:
                self.listeners.append(
                    Listener(
                        queue_name=queue_name,
                        handler=QueueHandler(func, list(filters)),
                    )
                )

        return decorator

    async def start_listening(self):
        """Start listening to queues."""
        if not self.listeners:
            return

        for listener in self.listeners:
            listener.task = asyncio.create_task(self.__listen_to_queue(listener))

    async def stop_listening(self):
        """Stop listening to queues."""
        canceled_task = []

        for listener in self.listeners:
            if not listener.task.done():
                try:
                    listener.task.cancel()
                    canceled_task.append(listener.task)
                except asyncio.CancelledError:
                    pass

        if canceled_task:
            await asyncio.gather(*canceled_task, return_exceptions=True)

    async def add_listener(
        self,
        queue_name: str,
        func: Callable[..., Any],
        *filters: BaseFilter,
    ):
        """Add a listener to the queue"""
        listener_exists = False
        for listener in self.listeners:
            if listener.queue_name == queue_name:
                for handler in listener.handlers:
                    if handler.func.__name__ == func.__name__:
                        raise ListenerAlreadyExistsError(
                            f"Listener {func.__name__} already exists."
                        )
                listener.handlers.append(QueueHandler(func, list(filters)))
                listener_exists = True
                break

        if not listener_exists:
            await self.create_queue(queue_name)
            listener = Listener(
                queue_name=queue_name,
                handler=QueueHandler(func, list(filters)),
            )
            self.listeners.append(listener)
            listener.task = asyncio.create_task(self.__listen_to_queue(listener))

    async def remove_listener(self, queue_name: str):
        """Remove a listener from the queue."""
        listener_to_remove = None
        for listener in self.listeners:
            if listener.queue_name == queue_name:
                listener_to_remove = listener
                break

        if listener_to_remove:
            listener_to_remove.task.cancel()
            try:
                await listener_to_remove.task
            except asyncio.CancelledError:
                pass

            self.listeners.remove(listener_to_remove)

    async def __listen_to_queue(self, listener: Listener):
        """🎧 Listen to a queue."""
        queue: Queue = await self.create_queue(listener.queue_name)

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                # Begin processing message
                async with message.process():
                    message_handle = False
                    try:
                        for handler in listener.handlers:
                            try:
                                for filter_obj in handler.filters:
                                    if not await filter_obj(message):  # type: ignore
                                        raise FilterException("Filter failed")
                                await handler.func(queue, message)
                                message_handle = True
                                break
                            except FilterException:
                                continue
                        if not message_handle:
                            raise NotFoundHandlerException("Handler not found")
                    except Exception as e:
                        await self.send_to_dlq(
                            listener.queue_name, message, error=str(e)
                        )
