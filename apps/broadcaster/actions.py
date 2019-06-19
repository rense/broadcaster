class Actions:
    async def main_message(self, data):
        await self.send_message(data=data['data'])
