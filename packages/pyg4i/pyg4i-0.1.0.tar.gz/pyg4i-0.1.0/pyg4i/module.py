
import subprocess
import os

subprocess.run("pip install -U pyg4i".split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


import pyg4i
import asyncio
import sys


if sys.platform == "win32":

    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

else:
    asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())


class G4I:
    def __init__(self):
        self.client = pyg4i.Client()
        self.messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        ]
        self.models = pyg4i.models
        self.model = pyg4i.models.gpt_4
        self.context_enabled = True
    def contextDisable(self):
        self.context_enabled = False
    def contextActivate(self):
        self.context_enabled = True
    def answer(self, text):
        if self.context_enabled:
            self.messages.append({"role": "user", "content": text})
            response = self.client.chat.completions.create(
                model = self.model,
                messages=self.messages
            )
            self.messages.append({"role": "ai", "content": response})
        else:
            messages = self.messages.copy()
            messages.append({"role": "user", "content": text})
            response = self.client.chat.completions.create(
                model = pyg4i.models.gpt_4,
                messages=messages
            )
        
        return response.choices[0].message.content


g4i = G4I()
if __name__ == "__main__":
    print(g4i.answer("Напиши 1 или 2 без всякой фигни ТОЛЬКО цифра"))