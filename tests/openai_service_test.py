import unittest
import time
import sys
import pathlib
import tkinter as tk
import matplotlib.pyplot as plt
from unittest.mock import Mock
from dotenv import load_dotenv

load_dotenv()
sys.path.append(str(pathlib.Path(__file__).parent.parent))
sys.path.append(str(pathlib.Path(__file__).parent.parent / "prompts"))
sys.path.append(str(pathlib.Path(__file__).parent.parent / "dao"))

from service.open_ai import OpenAIService

class TestOpenAIService(unittest.TestCase):
    def setUp(self):
        self.service = OpenAIService()

    def test_execute_conversation(self):
        questions = ["Qual foi a quantidade de casos de Dengue em Araguari no periodo 01/01/2023 e 01/02/2023?",]
        widget = Mock()
        times = []
        for question in questions:
            start_time = time.time()
            response = self.service.execute_conversation(question, widget)
            end_time = time.time()

            elapsed_time = end_time - start_time
            times.append(elapsed_time)

            print(f"Tempo para a resposta da pergunta '{question}': {elapsed_time} segundos")

            print("Response: ", response)
            self.assertIsNone(response)

        plt.bar(questions, times)
        plt.xlabel('Perguntas')
        plt.ylabel('Tempo (segundos)')
        plt.title('Tempo para cada pergunta')
        plt.xticks(rotation=90)
        plt.show()

if __name__ == '__main__':
    unittest.main()