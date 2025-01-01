# Project-Empyrean
 Personal use Weather Forecaster

A simple python tkinter app that sends requests to the National Weather Service API to retreive and display the hourly and extended forecasts for specified locations. Location data is saved locally on the user's computer using inputed latitude and longitude coordinates and is only sent to the NWS API.

Further UI improvements to come.

### Hourly View

In the hourly view, Empyrean displays a short detailed description of the forecast and creates two plots showing the temperature and chance of rain for the rest of the day.

![ ](/previews/v0.5%20LA_hourly_data.png)

### Extended View

Currently displays the extended forecast in a Treeview widget that supports collapsible headers to allow better visual control of what information is being displayed.

![ ](/previews/v0.5%20LA_extended_data.png)

# Attribution

> TODO: add license.md

Themes:

- https://github.com/RobertJN64/TKinterModernThemes

Icons:

- "weather-icons" https://github.com/erikflowers/weather-icons
- "Popout" https://www.flaticon.com/free-icons/pop-out created by Freepik - Flaticon
- "Download" https://www.flaticon.com/free-icons/obtain  created by meaicon - Flaticon

# UI Previews (by version)

## v0.5

The view after adding your first location:

![ ](/previews/v0.5%20LA_no_data.png)

The forecast views after fetching the forecasts for today:

![ ](/previews/v0.5%20LA_hourly_data.png)

![ ](/previews/v0.5%20LA_extended_data.png)

Supports multiple locations:

![ ](/previews/v0.5%20two%20locations.png)

## v0.4

![hourly preview](/previews/v0.4%20hourly_preview.png)

![extended preview](/previews/v0.4%20extended_preview.png)
