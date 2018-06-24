#!/usr/bin/env python3

from mod_pkuplotcard import DataViewer2

DataInfo = {
      'Name'   : 'NCEP1',
      'Years'  : ('1948','Present'),
      'Res'    : '2x2',
      'Link'   : '',
      'Path'   : '../data/ncep1/'
           }

FileList = [
   {  'Tag'    : 'NCEP1.Lat-Lon',
      'File'   : 'par_maplatlon.py',
      'Title'  : 'Map: Lat-Lon'        },
   {  'Tag'    : 'NCEP1.NH',
      'File'   : 'par_mapnp.py',
      'Title'  : 'Map: Arctic / NH'    },
   {  'Tag'    : 'NCEP1.SH',
      'File'   : 'par_mapsp.py',
      'Title'  : 'Map: Antarctica / SH'},
   {  'Tag'    : 'NCEP1.Lat-Pres',
      'File'   : 'par_latp.py',
      'Title'  : 'Cross-section: Lat-Pressure / Lat-Height' },
   {  'Tag'    : 'NCEP1.Lon-Pres',
      'File'   : 'par_lonp.py',
      'Title'  : 'Cross-section: Lon-Pressure / Lon-Height' },
   {  'Tag'    : 'NCEP1.Lat-Mon',
      'File'   : 'par_latt.py',
      'Title'  : 'Seasonal cycle: Lat-Month' },
   {  'Tag'    : 'NCEP1.Lon-Mon',
      'File'   : 'par_lont.py',
      'Title'  : 'Seasonal cycle: Lon-Month (i.e. Hovmueller diagram)'  },
   {  'Tag'    : 'NCEP1.Var-Mon',
      'File'   : 'par_vart.py',
      'Title'  : 'Seasonal cycle: Variable-Month' },
           ]

#########
def go():
   DataViewer2(DataInfo, FileList)

