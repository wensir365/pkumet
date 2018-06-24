#!/usr/bin/env python3

from mod_pkuplotcard import DataViewer2

DataInfo = {
      'Name'   : 'GPCC_v7',
      'Years'  : ('1979','Present'),
      'Res'    : '0.25x0.25',
      'Link'   : '',
      'Path'   : '../data/gpcc_7/'
           }

FileList = [
   {  'Tag'    : 'GPCC.Lat-Lon',
      'File'   : 'par_maplatlon.py',
      'Title'  : 'Map: Lat-Lon'        },
   {  'Tag'    : 'GPCC.Lat-Mon',
      'File'   : 'par_latt.py',
      'Title'  : 'Seasonal cycle: Lat-Month' },
   {  'Tag'    : 'GPCC.Var-Mon',
      'File'   : 'par_vart.py',
      'Title'  : 'Seasonal cycle: Variable-Month' },
           ]

#########
def go():
   DataViewer2(DataInfo, FileList)

