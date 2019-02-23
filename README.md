# PKU-Met
PKU-Met is a project with the full name of "PKU MetAssistant", which is a python-based assistant designed for meterologists, oceanographers, and Earth scientists. It features:

   - Dataset Viewer for
     1 NCEP/NCAR Reanalysis
	  2 CMAP
	  3 GPCP
	  4 GPCC
	  5 ERSST
	  6 NOAA/OLR
   - To-Do List
   - Wikipedia
   - WolframAlpha
   - Yahoo! Weather (offline, code frozen)
   - MP3 Player (offline, code forzen)

## Packages Requirement
   - numpy                 for array                   conda(Default)
   - pandas                for named array             conda(Default)
   - xarray                for netCDF I/O              conda(xarray)
   - netcdf4               for v4-above netCDF I/O     conda(netcdf4)
   - matplotlib            for plotting                conda(Default)
   - mpl_toolkits.basemap  for map plotting            conda(basemap)
   - colorama              for colorful ascii text     conda(Default)
   - wikipedia             for wikipedia API           pip(wikipedia)
   - wolframalpha          for wolframalpha API        pip(wolframalpha)
   - weather-api           for yahoo weather API       pip(weather-api)
   - python-vlc            for playing mp3 files       pip(python-vlc)

## Revision History

  - 2019-02-23: BIG improvements, locked as the final version using Command Line Interface (CLI). Moving to use webs.
  - 2018-06-14: 2nd version, got matured for NCEP1, including 8 categories of plots. Need to revise to-do list function.
  - 2018-05-29: 1st version, prototype on my Macbook Air, simple CLI, simply implementing all functions.
