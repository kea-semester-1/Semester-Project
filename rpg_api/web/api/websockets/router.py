from fastapi import APIRouter, WebSocket
from rpg_api.utils import dtos
import json
from pydantic import BaseModel

websocket_router = APIRouter()


class ChatConnectionManager:
    def __init__(self) -> None:
        self.active_connections: dict[str, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, location: str) -> None:
        await websocket.accept()
        if location not in self.active_connections:
            self.active_connections[location] = []
        self.active_connections[location].append(websocket)

    def disconnect(self, websocket: WebSocket, location: str) -> None:
        if location in self.active_connections:
            self.active_connections[location].remove(websocket)
            if not self.active_connections[location]:
                del self.active_connections[location]

    async def broadcast(self, message: str, location: str) -> None:
        if location in self.active_connections:
            for connection in self.active_connections[location]:
                await connection.send_text(message)


class PlayerLocation(BaseModel):
    x: int
    y: int


class Player(BaseModel):
    id: str
    location: PlayerLocation


class PlayerConnectionManager:
    def __init__(self) -> None:
        self.active_players: dict[str, Player] = {}
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(self, player_id: str, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_players[player_id] = Player(
            id=player_id, location=PlayerLocation(x=0, y=0)
        )
        self.active_connections[player_id] = websocket

    def disconnect(self, player_id: str) -> None:
        if player_id in self.active_players:
            del self.active_players[player_id]
        if player_id in self.active_connections:
            del self.active_connections[player_id]

    async def broadcast(self, message: str, player_id: str) -> None:
        for pid, websocket in self.active_connections.items():
            if pid != player_id:  # Avoid sending the message back to the sender
                await websocket.send_text(message)


manager = ChatConnectionManager()


@websocket_router.websocket("/ws/{location}/{client_id}")
async def websocket_endpoint(
    websocket: WebSocket, location: str, client_id: str
) -> None:
    await manager.connect(websocket, location)
    try:
        while True:
            data = await websocket.receive_text()
            # Send message only to clients in the same location
            await manager.broadcast(data, location)
    except Exception as e:
        manager.disconnect(websocket, location)


player_manager = PlayerConnectionManager()


@websocket_router.websocket("/ws/location/{player_id}")
async def player_location_websocket(websocket: WebSocket, player_id: str) -> None:
    print(player_id)
    await player_manager.connect(player_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)

            if message["type"] == "updateLocation":
                # Update player location
                new_location = message["location"]
                player = player_manager.active_players.get(player_id)
                if player:
                    player.location.x = new_location["x"]
                    player.location.y = new_location["y"]

                # Broadcast new location to other players
                await player_manager.broadcast(data, player_id)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        player_manager.disconnect(player_id)
