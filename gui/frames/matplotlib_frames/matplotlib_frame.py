"""Module for isolating matplotlib temperature plot."""
import TKinterModernThemes as TKMT

class PlotData():
    """"""
    def __init__(self):
        self.x_axis = [ ]
        self.x_axis_labels = [ ]
        self.y_axis = [ ]

class MatPlotLibFrame(TKMT.WidgetFrame):
    """_summary_

    Args:
        TKMT (_type_): _description_
    """
    def __init__(self, master, name, plotname, row=0, col=0):
        super().__init__(master, name)
        self.labelframe = self.master.addLabelFrame(plotname, row=row, col=col)
        self.canvas, self.fig, self.ax, self.background, self.accent = self.labelframe.matplotlibFrame(plotname)
        self.plotdata = PlotData()
