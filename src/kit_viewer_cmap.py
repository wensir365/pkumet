#!/usr/bin/env python3

from mod_pkuplotcard import DataViewer2

DataInfo = {
      'Name'   : 'CMAP',
      'Years'  : ('1979','Present'),
      'Res'    : '2.5x2.5',
      'Link'   : '',
      'Path'   : '../data/cmap/'
           }

FileList = [
   {  'Tag'    : 'CMAP.Lat-Lon',
      'File'   : 'par_maplatlon.py',
      'Title'  : 'Map: Lat-Lon'        },
   {  'Tag'    : 'CMAP.Lat-Mon',
      'File'   : 'par_latt.py',
      'Title'  : 'Seasonal cycle: Lat-Month' },
   {  'Tag'    : 'CMAP.Var-Mon',
      'File'   : 'par_vart.py',
      'Title'  : 'Seasonal cycle: Variable-Month' },
           ]

#########
def go():
   DataViewer2(DataInfo, FileList)

