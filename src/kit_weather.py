#!/usr/bin/env python3

import weather    as wea
import mod_pkucli as cli
from mod_color    import *

def go():
   print('Starting ... Toolkit/Yahoo_Weather')

   my = wea.Weather(unit=wea.Unit.CELSIUS)

   run = True
   while run:
      print('')
      query = cli.InputBox('Which city you want to check w/ Yahoo Weather?','[Q] ','Name of city (q for Quit): ')
      if query in {'0','q','bye','quit','exit'}:
         run = False
         print('')
      else:
         try:
            print('    '+'OK, searching '+c_p+query+c_n+' ...\n')
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
            print('Temp       : ',condition.temp,           'Celsius')
            print('Pressure   : ',atmosphere['pressure'],   '(Issue Here! psi/mb?)')
            print('Humidity   : ',atmosphere['humidity'],   '%')
            print('Visibility : ',atmosphere['visibility'], 'km')
            print('Wind SPD   : ',wind.speed,               'km/h')
            print('Wind DIR   : ',wind.direction,           'DegreesNorth')
            print('Sunrise    : ',astronomy['sunrise'])
            print('Sunset     : ',astronomy['sunset'])

            print('\n=== Forecast ===')
            ruler = '%15s%8s%8s%8s%30s'
            print(ruler%('Date','Day','Tmax','Tmin','Weather'))

            forecasts   = loc.forecast
            for i in forecasts:
               print(ruler%(i.date,i.day,i.high,i.low,i.text))

         except:
            print('\nSorry, cannot successfully retrieve data for %s from Yahoo Weather.'
                  %(c_red+query+c_n))
   return

