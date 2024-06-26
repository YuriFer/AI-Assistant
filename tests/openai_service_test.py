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
        tempo_total = 0
        question = "Como é trasmitida a Dengue?"
        widget = Mock()
        times = []
        for vezes in range(30):
            start_time = time.time()
            response = self.service.execute_conversation(question, widget)
            end_time = time.time()

            elapsed_time = end_time - start_time
            times.append(elapsed_time)

            print(f"Tempo para a resposta da pergunta '{question}': {elapsed_time} segundos")

            self.assertIsNone(response)
            tempo_total += elapsed_time

        print(f"Tempo médio para a resposta da pergunta '{question}': {tempo_total/30} segundos")
            

if __name__ == '__main__':
    unittest.main()