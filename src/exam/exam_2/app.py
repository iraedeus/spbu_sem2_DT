import asyncio

from src.exam.exam_2.view import Window


class App:
    async def exec(self) -> None:
        self.window = Window(asyncio.get_event_loop())
        await self.window.show()


if __name__ == "__main__":
    asyncio.run(App().exec())
