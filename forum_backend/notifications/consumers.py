from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from notifications.api.serializers import NotificationSerializer


class NotificationConsumer(AsyncJsonWebsocketConsumer):
    @database_sync_to_async
    def get_user_notifications(self, user):
        if not user.is_authenticated:
            return []

        serializer = NotificationSerializer(
            user.notification_set.all(),
            many=True
        )
        return serializer.data

    async def connect(self):
        await self.accept()

        # Add the user to a notification group based on their user ID
        user = self.scope['user']

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

        if action == 'poll':
            await self.send_json({
                'action': 'polled',
                'notifications': await self.get_user_notifications(self.scope['user'])
            })
