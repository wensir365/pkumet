#!/usr/bin/env python3
# This is the dictionary, a built-in type in python, 
# to describe figure's parameters to be generated by PKUNCEPVIEWER
# by X. Wen, Peking Univ, Apr 2018

'''
Notes
ID :        402001
            40      - Type: 40 = Variable-Time
              20    - Month: 20 = 12-month, one by one
                01  - figure number
LatRange :  [-5,5]   - Equatorial mean
            [0,90]   - Northern Hemisphere mean
            [-90,90] - Southern Hemisphere mean
LonRange :  [0,360]     - Zonal mean
            [0,180]     - Eastern Hemisphere zonal mean
            [100,120]   - Eastern China zonal mean
'''

FIG = [

######################
# Section 1.         #
######################
# Copy and paste below 15 lines
{  'ID'           : 402001                               ,  # Basic
   'TYPE'         : 'var-time'                           ,
   'Description'  : 'SAT at Beijing'                     ,
   'DescriptionC' : '北京的地表温度SAT'                  ,
   'FigTitle'     : 'Surface Air Temperature\nBeijing'   ,  # Key info
   'FileIn'       : ['ncep1/air.2m.mon.ltm.nc',]         ,
   'Compute'      : 'f[0].air-273.15'                    ,
   'LatRange'     : [40]                                 ,
   'LonRange'     : [120]                                ,
   'PresLev'      : 0                                    ,
   'VarStr'       : 'SAT'                                ,
   'Unit'         : 'Celsius'                            ,
   'FileOut'      : 'ncep1_anncycle_SAT_Beijing.pdf'     }  # Output
,#########################################################

# Copy and paste below 15 lines
{  'ID'           : 402002                               ,  # Basic
   'TYPE'         : 'var-time'                           ,
   'Description'  : 'SAT over East China'                ,
   'DescriptionC' : '中国东部地区的地表温度SAT'          ,
   'FigTitle'     : 'Surface Air Temperature\n90E-120E, 20N-40N',  # Key info
   'FileIn'       : ['ncep1/air.2m.mon.ltm.nc',]         ,
   'Compute'      : 'f[0].air-273.15'                    ,
   'LatRange'     : [20,40]                              ,
   'LonRange'     : [90,120]                             ,
   'PresLev'      : 0                                    ,
   'VarStr'       : 'SAT'                                ,
   'Unit'         : 'Celsius'                            ,
   'FileOut'      : 'ncep1_anncycle_SAT_EastChina.pdf'   }  # Output
,#########################################################

]
