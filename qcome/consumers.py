import json
from channels.generic.websocket import AsyncWebsocketConsumer


class BookingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("booking_updates", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("booking_updates", self.channel_name)

    async def send_booking_update(self, event):
        """ Handle the event sent from BookingCreateView """
        await self.send(text_data=json.dumps({
            "message": "Booking updated",
            "booking": event["booking"]  # ✅ Correct key
        }))


class WorkerAssignmentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("worker_updates", self.channel_name)
        await self.accept()
        await self.send(text_data=json.dumps({"message": "Connected to worker updates!"}))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("worker_updates", self.channel_name)

    async def send_worker_update(self, event):
        """ Handles the WebSocket event sent from AssignedWorkerCreateView """
        await self.send(text_data=json.dumps(event["data"]))

