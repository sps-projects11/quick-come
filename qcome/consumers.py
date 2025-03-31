import json
from channels.generic.websocket import AsyncWebsocketConsumer


class BookingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("booking_updates", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("booking_updates", self.channel_name)

    async def receive(self, text_data):
        # Handle incoming WebSocket message
        text_data_json = json.loads(text_data)
        message_type = text_data_json.get("type")

        if message_type == "send_booking_update":
            # If the message type is 'send_booking_update', handle it
            await self.send_booking_update(text_data_json)
        else:
            # Handle other types of messages, if any
            await self.send(text_data=json.dumps({
                "message": "Unknown message type"
            }))

    async def send_booking_update(self, event):
        # Extract booking data from the event
        booking_data = event.get("booking")  # Use get() to avoid KeyError
        if booking_data:
            # Send the booking update to the WebSocket
            await self.send(text_data=json.dumps({
                "message": "Booking updated",
                "booking": booking_data
            }))
        else:
            # Handle the case where 'booking' is missing, if needed
            await self.send(text_data=json.dumps({
                "message": "Booking update failed, no booking data available"
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
        # Get the user_id from the URL route (sent as a part of the WebSocket URL)
        self.user_id = self.scope['url_route']['kwargs']['user_id']  # Extract user_id
        
        # Create a unique group for each user
        self.group_name = f"user_{self.user_id}"

        # Join the unique group
        await self.channel_layer.group_add(
            self.group_name,  # Group name is user-specific
            self.channel_name  # The unique channel name of this connection
        )

        # Accept the WebSocket connection
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the unique group when the WebSocket is closed
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # Receive payment update from the server
    async def payment_update(self, event):
        # Log the event data to inspect its structure
        print("Received event:", event)

        # Use the payment data directly
        payment_data = event["payment"]

        # Send the payment update to the WebSocket client
        await self.send(text_data=json.dumps({
            "type": "payment_update",
            "payment": payment_data
        }))





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




