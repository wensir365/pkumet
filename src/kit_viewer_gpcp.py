#!/usr/bin/env python3

from mod_pkuplotcard import DataViewer2

DataInfo = {
      'Name'   : 'GPCP_v2.3',
      'Years'  : ('1979','Present'),
      'Res'    : '2.5x2.5',
      'Link'   : '',
      'Path'   : '../data/gpcp_2.3/'
           }

FileList = [
   {  'Tag'    : 'GPCP.Lat-Lon',
      'File'   : 'par_maplatlon.py',
      'Title'  : 'Map: Lat-Lon'        },
   {  'Tag'    : 'GPCP.Lat-Mon',
      'File'   : 'par_latt.py',
      'Title'  : 'Seasonal cycle: Lat-Month' },
   {  'Tag'    : 'GPCP.Var-Mon',
      'File'   : 'par_vart.py',
      'Title'  : 'Seasonal cycle: Variable-Month' },
           ]

#########
def go():
   DataViewer2(DataInfo, FileList)

