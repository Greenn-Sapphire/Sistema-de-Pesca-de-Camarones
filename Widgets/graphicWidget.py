from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import customtkinter as ctk
import matplotlib
matplotlib.use('TkAgg')

from functions import Data

class GraphicFrame(ctk.CTkFrame):
    def __init__(self, master, df, xaxis, yaxis, graphictype):
        super().__init__(master)

        if 'fig' in locals():
            self.frame.destroy()
        # the figure that will contain the plot
        fig = plt.figure(figsize = (12, 5))

        subplot = fig.add_subplot(111)
        #https://matplotlib.org/stable/plot_types/index.html
        match graphictype:
            case 'bar':
                subplot.bar(df[xaxis], df[yaxis])
            case 'boxplot':
                subplot.boxplot(df[xaxis], df[yaxis])
            case 'hist':
                subplot.hist(df[xaxis], df[yaxis])
            case 'pie':
                subplot.pie(df[xaxis], df[yaxis])
            case 'scatter':
                subplot.scatter(df[xaxis], df[yaxis])
        plt.xticks(rotation = 90, fontsize = 8)

        # creating the Tkinter canvas
        # containing the Matplotlib figure
        canvas = FigureCanvasTkAgg(fig, master = self)  
        canvas.draw()

        # placing the canvas on the Tkinter window
        canvas.get_tk_widget().pack(expand = True, fill = 'y')

        # creating the Matplotlib toolbar
        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()

        # placing the toolbar on the Tkinter window
        canvas.get_tk_widget().pack()