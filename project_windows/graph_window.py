from project_windows.window import Window
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import pandas as pd

class GraphWindow(Window):
    def __init__(self, data:dict):
        super().__init__(title="Gráfico de Casos Específicos", dimension="650x550")

        data_frame = pd.DataFrame(data)

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(data_frame['weeks'][::-1], data_frame['cases_est'][::-1], marker='o', label='Casos Estimados', color='blue')
        ax.plot(data_frame['weeks'][::-1], data_frame['cases'][::-1], marker='o', label='Casos Reais', color='red')

        ax.set_title(f'Casos Estimados x Casos Reais por Semana - População: {int(data["population"])}')
        ax.set_xlabel('Semanas')
        ax.set_ylabel('Número de Casos')
        ax.legend()

        ax.grid(True)

        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(side="top", fill="both", expand=1)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def on_closing(self):
        self.window_exist = False
        self.destroy()

