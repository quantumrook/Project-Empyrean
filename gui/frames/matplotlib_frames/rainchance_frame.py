"""Module for isolating matplotlib rain chance plot."""

from gui.frames.matplotlib_frames.matplotlib_frame import MatPlotLibFrame, PlotData
from utils.structures.datetime import TODAY
from utils.structures.forecast.empyrean.forecast import EmpyreanForecast

class RainChanceData(PlotData):
    """Helper class to contain all the rain chance data used in generating the corresponding
    plot.
    """
    def __init__(self):
        super().__init__()
        self.rain = [ ]

class RainChanceFrame(MatPlotLibFrame):
    """An extension of the MatPlotLibFrame class that specifically generates a rain chance
    vs time plot.
    """
    def __init__(self, master, name, plotname, row, col):
        super().__init__(master, name, plotname, row, col)
        self.plotdata = RainChanceData()

    def prepare_data(self, hourly_forecast: EmpyreanForecast):
        """Callback used when the forecast display frame has its forecast data updated.
        """
        is_first_hour = True
        for forecast in hourly_forecast.forecasts:
            if forecast.start.date == TODAY.date:
                hour = int(forecast.start.hour().split(":")[0])
                if hour > 0 and is_first_hour:
                    self.plotdata.x_axis_labels.append(hour)
                    is_first_hour = False
                if hour % 4 == 0:
                    self.plotdata.x_axis_labels.append(hour)
                self.plotdata.x_axis.append(hour)
                rain = int(forecast.content.rainChance.get_value())
                self.plotdata.rain.append(rain)
        self._setup_plots_frame()

    def _setup_plots_frame(self) -> None:
        """Helper function for generating matplotlib plots of forecast data.
        """
        self.ax.plot(self.plotdata.x_axis, self.plotdata.rain)

        self.ax.set_xticks(self.plotdata.x_axis_labels)
        self.ax.set_ylabel("% Chance of Rain")
