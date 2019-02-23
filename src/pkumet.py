#!/usr/bin/env python3

'''
PKU MetAssistant (北大气象助手)
Xinyu Wen
xwen@pku.edu.cn
Dept of Atmospheric & Oceanic Sciences, Peking Univ
Since May 2018

External Modules:
- numpy                 conda(Default)		for array
- pandas                conda(Default)		for named array
- xarray                conda(xarray)		for netCDF I/O
- netcdf4					conda(netcdf4)		for above-version4-netCDF I/O
- matplotlib            conda(Default)		for plotting
- mpl_toolkits.basemap  conda(basemap)		for map plotting
- colorama              conda(Default)		for colorful ascii text
- wikipedia             pip(wikipedia)		for wikipedia API
- wolframalpha          pip(wolframalpha)	for wolframalpha API
- weather               pip(weather-api)	for yahoo weather API
- vlc                   pip(python-vlc)	for playing mp3 files
'''

import mod_service

if __name__=='__main__':

   # init
   print('----------------')
   print('  MetAssistant  ')
   print('----------------')
   print('What can I do for you? (h for help)')

   # main loop
   ii = 0
   running = True
   while running:
      ii+=1
      running = mod_service.service(ii)

   # ending

