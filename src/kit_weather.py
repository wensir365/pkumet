#!/usr/bin/env python3

import weather    as wea
import mod_cli    as cli
from mod_color    import *

def go():
   print('Starting ... Toolkit/Yahoo_Weather')

   my = wea.Weather(unit=wea.Unit.CELSIUS)

   qa = cli.q_and_a('Which city you want to check w/ Yahoo Weather (q|0 for Quit)?')

   run = True
   while run:
      query = qa.show_and_get()
      if query in {'0','q','bye','quit','exit'}:
         run = False
         print('')
      else:
         try:
            loc   = my.lookup_by_location(query)

            print('\n=== Current Weather===')
            title       = loc.title
            atmosphere  = loc.atmosphere
            wind        = loc.wind
            astronomy   = loc.astronomy
            condition   = loc.condition

            print(title)
            print(condition.date)
            print('')

            print('Weather    : ',condition.text)
            print('Temp       : ',condition.temp)
            print('Pressure   : ',atmosphere['pressure'])
            print('Humidity   : ',atmosphere['humidity'])
            print('Visibility : ',atmosphere['visibility'])
            print('Wind SPD   : ',wind.speed)
            print('Wind DIR   : ',wind.direction)
            print('Sunrise    : ',astronomy['sunrise'])
            print('Sunset     : ',astronomy['sunset'])

            print('\n=== Forecast ===')
            ruler = '%15s%8s%8s%8s%30s'
            print(ruler%('Date','Day','Tmax','Tmin','Weather'))

            forecasts   = loc.forecast
            for i in forecasts:
               print(ruler%(i.date,i.day,i.high,i.low,i.text))

         except:
            print('\nSorry, didn\'t find any info for %s from Yahoo Weather.'
                  %(c_red+query+c_n))
   return

