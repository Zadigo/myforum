from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async


class NotificationConsumer(AsyncJsonWebsocketConsumer):
    @database_sync_to_async
    def get_user_notifications(self, user):
        return list(user.notifications.all().values())

    async def connect(self):
        await self.accept()

        # Add the user to a notification group based on their user ID
        user = self.scope['user']
        print(user)
        if user.is_authenticated:
            await self.channel_layer.group_add(
                f"notifications_{user.id}",
                self.channel_name
            )

    async def disconnect(self, close_code):
        # Remove the user from the notification group
        user = self.scope['user']
        if user.is_authenticated:
            await self.channel_layer.group_discard(
                f"notifications_{user.id}",
                self.channel_name
            )

    async def receive_json(self, content, **kwargs):
        action = content.get('action')

        if action == 'idle_connect':
            pass
