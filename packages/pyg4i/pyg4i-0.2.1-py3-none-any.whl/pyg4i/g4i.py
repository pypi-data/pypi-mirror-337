import subprocess
import g4f
import asyncio
import sys
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Установка pyg4i
try:
    subprocess.run("pip install -U pyg4i".split(), check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
except subprocess.CalledProcessError as e:
    logging.error(f"Ошибка установки pyg4i: {e}")

# Настройка цикла событий для Windows
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
else:
    asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())


class G4I:
    """Класс для взаимодействия с моделью g4f."""

    def __init__(self):
        """Инициализация клиента и переменных состояния."""
        self.client = g4f.Client()
        self.messages = list()
        self.model = g4f.models.gpt_4
        self.context_enabled = True

    def toggle_context(self, enable: bool) -> None:
        """Включить или отключить контекст.

        Args:
            enable (bool): True для включения контекста, False для отключения.
        """
        self.context_enabled = enable

    def clear_context(self) -> None:
        """Очистить историю сообщений."""
        self.messages = list()

    def get_response(self, user_input: str) -> str:
        """Получить ответ от модели на основе пользовательского ввода.

        Args:
            user_input (str): Ввод пользователя.

        Returns:
            str: Ответ модели.
        """
        if self.context_enabled:
            self.messages.append({"role": "user", "content": user_input})

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.messages
            )
            ai_message = response.choices[0].message.content
            if self.context_enabled:
                self.messages.append({"role": "ai", "content": ai_message})
            return ai_message
        except Exception as e:
            logging.error(f"Ошибка при получении ответа: {e}")
            return "Произошла ошибка при получении ответа."


g4i = G4I()


def answer(text: str) -> str:
    """Функция для получения ответа от модели.

    Args:
        text (str): Ввод пользователя.

    Returns:
        str: Ответ модели.
    """
    return g4i.get_response(text)


def clear_context() -> None:
    """Функция для очистки контекста."""
    g4i.clear_context()


def context_disable() -> None:
    """Функция для отключения контекста."""
    g4i.toggle_context(False)


def context_activate() -> None:
    """Функция для активации контекста."""
    g4i.toggle_context(True)