#!/usr/bin/env python3

from mod_pkuplotcard import DataViewer2

DataInfo = {
      'Name'   : 'NOAA_OLR',
      'Years'  : ('1979','Present'),
      'Res'    : '1x1',
      'Link'   : '',
      'Path'   : '../data/noaa-olr/'
           }

FileList = [
   {  'Tag'    : 'NOAAOLR.Lat-Lon',
      'File'   : 'par_maplatlon.py',
      'Title'  : 'Map: Lat-Lon'        },
   {  'Tag'    : 'NOAAOLR.Lat-Mon',
      'File'   : 'par_latt.py',
      'Title'  : 'Seasonal cycle: Lat-Month' },
           ]

#########
def go():
   DataViewer2(DataInfo, FileList)

