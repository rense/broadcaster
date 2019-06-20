from settings import (
    ACTION_MESSAGE,
    ACTION_CONNECTS,
    ACTION_DISCONNECTS
)


class Actions:

    async def main_message(self, data):
        await self.send_message(
            action=ACTION_MESSAGE,
            data=data['data']
        )

    async def main_connects(self, data):
        await self.send_message(
            action=ACTION_CONNECTS,
            data=data['data']
        )

    async def main_disconnects(self, data):
        await self.send_message(
            action=ACTION_DISCONNECTS,
            data=data['data']
        )
