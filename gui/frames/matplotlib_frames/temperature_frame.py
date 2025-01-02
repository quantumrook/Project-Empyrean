"""Module for isolating matplotlib temperature plot."""

from gui.frames.matplotlib_frames.matplotlib_frame import MatPlotLibFrame, PlotData
from utils.structures.datetime import TODAY
from utils.structures.forecast.empyrean.forecast import EmpyreanForecast

class TemperatureData(PlotData):
    """Helper class to contain all the temperature data used in generating the corresponding
    plot.
    """
    def __init__(self):
        super().__init__()
        self.temps = [ ]
        self.windchills = [ ]

class TemperatureFrame(MatPlotLibFrame):
    """An extension of the MatPlotLibFrame class that specifically generates a temperature
    vs time plot.
    """
    def __init__(self, master, name, plotname, row, col):
        super().__init__(master, name, plotname, row, col)
        self.plotdata = TemperatureData()

    @staticmethod
    def __calculate_windchill(temperature: int, wind_speed: int) -> int:
        """Helper method for calculating the temperature when accounting for windchill

        Args:
            temperature (int): the surface temperature
            wind_speed (int): the surface windspeed

        Returns:
            int: the temperature when accounting for the windchill
        """
        if temperature >= 50 or wind_speed == 0:
            return temperature
        windchill = 35.74+(0.6215*temperature)
        windchill -= (35.75*pow(wind_speed, 0.16))
        windchill += (0.4275*temperature*pow(wind_speed, 0.16))
        windchill = round(windchill)
        if windchill > temperature:
            return temperature #TODO Check why this is necessary
        return windchill

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
                temp = int(forecast.content.temperature.get_value())
                self.plotdata.temps.append(temp)
                chill = self.__calculate_windchill(
                    temp,
                    forecast.content.wind.speedHigh.get_value()
                )
                self.plotdata.windchills.append(chill)
        self._setup_plots_frame()

    def _setup_plots_frame(self) -> None:
        """Helper function for generating matplotlib plots of forecast data.
        """
        self.ax.plot(self.plotdata.x_axis, self.plotdata.windchills)
        self.ax.plot(self.plotdata.x_axis, self.plotdata.temps, c='white')
        self.ax.legend(['Windchill', 'Temperature'])

        self.ax.set_xticks(self.plotdata.x_axis_labels)
        self.ax.set_ylabel('\N{DEGREE SIGN}'+'F')
