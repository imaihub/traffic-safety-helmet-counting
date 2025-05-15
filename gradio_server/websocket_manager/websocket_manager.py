import asyncio
import threading

import websockets

from elements.utils import Logger


class WebSocketServer:
    def __init__(self) -> None:
        self.loop = asyncio.new_event_loop()
        self.logger = Logger.setup_logger()
        self.stop_event = asyncio.Event()
        self.client_connected_event = asyncio.Event()
        self.server = None
        self.response: str = ""
        self.stop = False

    def finish_connection(self) -> None:
        """
        Tell the client to stop receiving requests by setting a special response as the analysis is done.
        """
        self.response = "finished"

    async def websocket_handler(self, websocket) -> None:
        # Synchronous WebSocket handler running in its own event loop
        self.client_connected_event.set()
        while self.stop is False:
            while not self.response == "finished":
                if self.response:
                    await websocket.send(self.response)
                await asyncio.sleep(0.01)
            self.logger.info(msg="Sending the finished statement")
            await websocket.send("finished")
            self.response = None

    def set_response(self, response: str) -> None:
        """
        Set the response to be sent to the websocket client.
        """
        self.response = response

    async def serve(self) -> None:
        self.server = await websockets.serve(self.websocket_handler, "localhost", 5678)
        await self.stop_event.wait()
        self.logger.info("Attempting to close connection")
        self.server.close()
        self.logger.info("Closed connection")

    def start_websocket_server(self) -> None:
        """
        This function runs in a new thread and manages its own event loop.
        """
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.serve())

    def run_websocket_server(self) -> None:
        # Start the WebSocket server in a separate thread
        threading.Thread(target=self.start_websocket_server, daemon=True).start()
