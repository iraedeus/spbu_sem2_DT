import asyncio
from tkinter import *
from tkinter import ttk
import tkinter.scrolledtext as scrolledtext
import tkinter as tk
from model import *


class App:
    async def exec(self):
        self.window = Window(asyncio.get_event_loop())
        await self.window.show()


class Window():
    def __init__(self, loop):
        self.loop = loop
        self.root = Tk()
        self.root.geometry("1200x700")
        self.init_buttons()
        self.init_text_labels()

    def init_buttons(self):
        self.btn_new = ttk.Button(self.root, text="Новые цитаты",
                                  command=lambda: self.loop.create_task(self.handle_new()))
        self.btn_random = ttk.Button(self.root, text="Случайные цитаты",
                                     command=lambda: self.loop.create_task(self.handle_random()))
        self.btn_best = ttk.Button(self.root, text="Лучшие цитаты",
                                   command=lambda: self.loop.create_task(self.handle_best()))

        self.btn_new.place(relheight=0.1, relwidth = 0.2, relx=0.7, rely=0.2)
        self.btn_random.place(relheight=0.1, relwidth = 0.2, relx=0.7, rely=0.4)
        self.btn_best.place(relheight=0.1, relwidth = 0.2, relx=0.7, rely=0.6)

    def init_text_labels(self):
        self.text_frame = scrolledtext.ScrolledText(height=30, width=70, relief="solid", borderwidth=1)
        self.text_frame.place(rely = 0.1, relx = 0.05)

    async def handle_new(self):
        quotes = await get_new()
        self.init_text_labels()
        for quote in quotes:
            self.text_frame.insert(1.0, quote + "\n\n\n")

    async def handle_best(self):
        quotes = await get_best()
        self.init_text_labels()
        for quote in quotes:
            self.text_frame.insert(1.0, quote + "\n\n\n")

    async def handle_random(self):
        quotes = await get_random()
        self.init_text_labels()
        for quote in quotes:
            self.text_frame.insert(1.0, quote + "\n\n\n")

    async def show(self):
        while True:
            self.root.update()
            await asyncio.sleep(0)


asyncio.run(App().exec())