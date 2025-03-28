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



class BookingListAllConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """Join the WebSocket group 'booking_updates'."""
        await self.channel_layer.group_add("booking_updates", self.channel_name)
        await self.accept()
        print("✅ Worker connected to WebSocket")

    async def disconnect(self, close_code):
        """Leave the WebSocket group on disconnect."""
        await self.channel_layer.group_discard("booking_updates", self.channel_name)
        print("❌ Worker disconnected from WebSocket")

    async def receive(self, text_data):
        """Receive messages from frontend and broadcast updates."""
        data = json.loads(text_data)
        booking_id = data.get("booking_id")
        new_status = data.get("new_status")

        if booking_id and new_status:
            print(f"🔄 Broadcasting Booking Update: {booking_id} -> {new_status}")
            await self.channel_layer.group_send(
                "booking_updates",
                {
                    "type": "send_booking_update",
                    "message": "Booking status updated",
                    "booking_id": booking_id,
                    "new_status": new_status
                }
            )

    async def send_booking_update(self, event):
        """Send real-time updates to all connected clients."""
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "booking_id": event["booking_id"],  # The booking that was updated
            "new_status": event["new_status"],  # The new status
        }))
    
    async def booking_update(self, event):
        """Receive and send the service update to all connected clients."""
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "booking_id": event["booking_id"],  # The booking that was updated
            "services": event["services"],  # The updated services list
        }))

class PaymentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("payments", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("payments", self.channel_name)

    async def payment_update(self, event):
        payment_data = json.loads(event["payment"])
        await self.send(text_data=json.dumps({"type": "payment_update", "data": payment_data}))




class WorkerUpdateConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("worker_updates", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("worker_updates", self.channel_name)

    async def send_worker_update(self, event):
        await self.send(text_data=json.dumps(event["data"]))

        

class GarageBillConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("garage_bills", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("garage_bills", self.channel_name)

    async def bill_update(self, event):
        bill_data = json.loads(event["bill"])
        await self.send(text_data=json.dumps({"type": "bill_update", "data": bill_data}))




