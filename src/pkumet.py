#!/usr/bin/env python3

'''
PKU MetAssistant (北大气象助手)
Xinyu Wen
xwen@pku.edu.cn
Dept of Atmospheric & Oceanic Sciences, Peking Univ
Since May 2018

External Modules:
- numpy                 for array
- pandas                for named array
- xarray                for netCDF I/O
- matplotlib            for plotting
- mpl_toolkits.basemap  for map plotting
- colorama              for colorful ascii text
- wikipedia             for wikipedia API
- wolframalpha          for wolframalpha API
- weather               for yahoo weather API
- vlc                   for playing mp3 files
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

