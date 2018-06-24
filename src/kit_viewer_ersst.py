#!/usr/bin/env python3

from mod_pkuplotcard import DataViewer2

DataInfo = {
      'Name'   : 'ERSST_v5',
      'Years'  : ('1850','Present'),
      'Res'    : '2x2',
      'Link'   : '',
      'Path'   : '../data/ersst_5/'
           }

FileList = [
   {  'Tag'    : 'ERSST.Lat-Lon',
      'File'   : 'par_maplatlon.py',
      'Title'  : 'Map: Lat-Lon'        },
   {  'Tag'    : 'ERSST.Lat-Mon',
      'File'   : 'par_latt.py',
      'Title'  : 'Seasonal cycle: Lat-Month' },
           ]

#########
def go():
   DataViewer2(DataInfo, FileList)

