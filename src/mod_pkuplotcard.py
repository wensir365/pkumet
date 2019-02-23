#!/usr/bin/env python3

import numpy                  as np
import xarray                 as xr
import pprint                 as pp
import mod_pkuplot            as pkuplot
import mod_pkucli             as cli

#################
class PlotCard():
   def __init__(self,FigureDict,Tag='',DataPath='../data/',PlotPath='../plot/'):
      self.F         = FigureDict
      self.Tag       = Tag          # prefix added to fout
      self.plotpath  = PlotPath
      self.datapath  = DataPath

      if len(self.Tag)>=1:
         self.fout   = self.plotpath+self.Tag+'.'+self.F['FileOut']
      else:
         self.fout   = self.F['FileOut']

      print('\n <PlotCard> ---> a FIG dictionary loaded:')
      print('')
      pp.pprint(self.F)
      print('')

   def makeplot(self):
      # ===== Read data
      Nfile = len(self.F['FileIn'])
      f     = []
      for i in range(Nfile):
         f.append(xr.open_dataset(self.datapath+self.F['FileIn'][i],decode_times=False))
      z        = eval(self.F['Compute'])

      # ===== Figure Type
      #  Pres-Lat-Lon / Lat-Lon
      if    self.F['TYPE'] in ('pres-lat-lon','lat-lon'):
         if self.F['TYPE']=='pres-lat-lon':
            z = z.sel(level=self.F['PresLev'])
         z = pkuplot.timeavg(z,self.F['Month'])
         pkuplot.plot2d_latlon(
            z, z.lon, z.lat, clev=eval(self.F['Levels']),
            country=self.F['CountryLine'],
            domain=self.F['Domain'], cm=self.F['ColorMap'],
            cbarstr='Unit: %s\nM=%0.2f, m=%0.2f'%(self.F['Unit'],np.max(z),np.min(z)),
            ti=self.F['FigTitle'], 
            fout=self.fout )

      #  Pres-Lat-Lon-Vec or Lat-Lon-Vec
      elif  self.F['TYPE'] in ('pres-lat-lon-vec','lat-lon-vec'):
         u,v   = z

         if self.F['TYPE']=='pres-lat-lon-vec':
            u  = u.sel(level=self.F['PresLev'])
         u  = pkuplot.timeavg(u,self.F['Month'])

         if self.F['TYPE']=='pres-lat-lon-vec':
            v  = v.sel(level=self.F['PresLev'])
         v  = pkuplot.timeavg(v,self.F['Month'])

         spd   = np.sqrt(u*u+v*v)

         pkuplot.plotvector_latlon(
            u,v,u.lon,u.lat,
            domain=self.F['Domain'], density=self.F['Density'], veclen=self.F['VecLen'],
            country=self.F['CountryLine'],
            cbarstr='%s\nM=%0.2f, m=%0.2f'%(self.F['Unit'],np.max(spd),np.min(spd)),
            ti=self.F['FigTitle'], 
            fout=self.fout )

      #  Pres-NP or Pres-SP or NP or SP
      elif  self.F['TYPE'] in ('pres-np','pres-sp','np','sp'):
         if self.F['TYPE'] in ('pres-np','pres-sp'):
            z = z.sel(level=self.F['PresLev'])
         z = z.sel(lat=slice(self.F['Domain'][1],self.F['Domain'][0]))
         z = pkuplot.timeavg(z,self.F['Month'])

         pkuplot.plot2d_polar(
            z, z.lon, z.lat, clev=eval(self.F['Levels']),
            country=self.F['CountryLine'],
            domain=self.F['Domain'], cm=self.F['ColorMap'],
            cbarstr='Unit: %s\nM=%0.2f, m=%0.2f'%(self.F['Unit'],np.max(z),np.min(z)),
            ti=self.F['FigTitle'], 
            fout=self.fout )

      #  Pres-NP-Vec or Pres-SP-Vec basemap在极区画矢量有严重问题！我也没办法
      elif  self.F['TYPE'] in ('pres-np-vec','pres-sp-vec'):
         u,v   = z

         u  = u.sel(level=self.F['PresLev'])
         u  = u.sel(lat=slice(self.F['Domain'][1],self.F['Domain'][0]))
         u  = pkuplot.timeavg(u,self.F['Month'])

         v  = v.sel(level=self.F['PresLev'])
         v  = v.sel(lat=slice(self.F['Domain'][1],self.F['Domain'][0]))
         v  = pkuplot.timeavg(v,self.F['Month'])

         spd   = np.sqrt(u*u+v*v)

         pkuplot.plotvector_polar(
            u,v,u.lon,u.lat,
            domain=self.F['Domain'], density=self.F['Density'], veclen=self.F['VecLen'],
            country=self.F['CountryLine'],
            cbarstr='%s\nM=%0.2f, m=%0.2f'%(self.F['Unit'],np.max(spd),np.min(spd)),
            ti=self.F['FigTitle'], 
            fout=self.fout )

      #  Lat-Pres (Zonal Mean)
      elif  self.F['TYPE']=='lat-pres':
         z = pkuplot.zonalavg(z,self.F['LonRange'])
         z = pkuplot.timeavg(z,self.F['Month'])
         z = z.sel(level=slice(self.F['LevRange'][0],self.F['LevRange'][1]))

         pkuplot.plot2d_contour(
            z.lat, z.level, z, ti=self.F['FigTitle'],
            add_contour=self.F['AddContour'], num_contours=self.F['NumContours'],
            xl='Latitude (Degrees North)',yl='Pressure (hPa)',yreverse=True,
            xticks=np.arange(-90,91,30),
            clev=eval(self.F['Levels']), cm=self.F['ColorMap'],
            cbarstr='Unit: %s\nM=%0.2f, m=%0.2f'%(self.F['Unit'],np.max(z),np.min(z)),
            fout=self.fout )

      #  Lon-Pres (Meridional Mean)
      elif  self.F['TYPE']=='lon-pres':
         z = pkuplot.meriavg(z,self.F['LatRange'])
         z = pkuplot.timeavg(z,self.F['Month'])
         z = z.sel(level=slice(self.F['LevRange'][0],self.F['LevRange'][1]))

         pkuplot.plot2d_contour(
            z.lon, z.level, z, ti=self.F['FigTitle'],
            add_contour=self.F['AddContour'], num_contours=self.F['NumContours'],
            xl='Longitude (Degrees East)',yl='Pressure (hPa)',yreverse=True,
            xticks=np.arange(0,361,30),
            clev=eval(self.F['Levels']), cm=self.F['ColorMap'],
            cbarstr='Unit: %s\nM=%0.2f, m=%0.2f'%(self.F['Unit'],np.max(z),np.min(z)),
            fout=self.fout )

      #  Lat-Time
      elif  self.F['TYPE']=='lat-time':
         z = pkuplot.zonalavg(z,self.F['LonRange'])
         if self.F['PresLev']>0:
            z = z.sel(level=self.F['PresLev'])
         z = z.transpose()
         xaxis = np.arange(1,13,1)

         pkuplot.plot2d_contour(
            xaxis, z.lat, z, ti=self.F['FigTitle'],
            add_contour=self.F['AddContour'], num_contours=self.F['NumContours'],
            xl='Time (Month)',yl='Latitude (Deg_North)',
            xticks=np.arange(1,13,1), yticks=np.arange(-90,91,30),
            clev=eval(self.F['Levels']), cm=self.F['ColorMap'],
            cbarstr='Unit: %s\nM=%0.2f, m=%0.2f'%(self.F['Unit'],np.max(z),np.min(z)),
            fout=self.fout )

      #  Lon-Time (Hovmueller)
      elif  self.F['TYPE']=='lon-time':
         z = pkuplot.meriavg(z,self.F['LatRange'])
         if self.F['PresLev']>0:
            z = z.sel(level=self.F['PresLev'])
         yaxis = np.arange(1,13,1)

         pkuplot.plot2d_contour(
            z.lon, yaxis, z, ti=self.F['FigTitle'],
            add_contour=self.F['AddContour'], num_contours=self.F['NumContours'],
            xl='Longitude (Deg_East)',yl='Time (month)',
            xticks=np.arange(0,361,30), yticks=yaxis,
            clev=eval(self.F['Levels']), cm=self.F['ColorMap'],
            cbarstr='Unit: %s\nM=%0.2f, m=%0.2f'%(self.F['Unit'],np.max(z),np.min(z)),
            fout=self.fout )

      #  Var-Time
      elif  self.F['TYPE']=='var-time':
         lats, lons = self.F['LatRange'], self.F['LonRange']
         if len(lats)==1 and len(lons)==1:
            z = z.sel(lat=lats[0],lon=lons[0],method='nearest')
         else:
            z = pkuplot.meriavg(z,lats)
            z = pkuplot.zonalavg(z,lons)
         if self.F['PresLev']>0:
            z = z.sel(level=self.F['PresLev'])
         xaxis = np.arange(1,13,1)

         pkuplot.plot1d_timeseries1(
            xaxis, z, ti=self.F['FigTitle'],
            xl='Time (Month)', xticks=xaxis,
            yl=self.F['VarStr']+' ('+self.F['Unit']+')',
            fout=self.fout )

      #  Others
      else:
         print('ncep1viewer/makeplot: an unknown FIGURE TYPE=',self.F['TYPE'])
         print('ncep1viewer/makeplot: 不能识别的 FIGURE TYPE=',self.F['TYPE'])


# This DataViewer is a generic framework expanded from NCEP1viewer,
# a simple 2-level implementation developed by Xinyu on April 2018.
# You can easily use this DataViewer framework as any dataset viewer in future,
# by just feeding DataInfo and FileList

#########
def DataViewer2(DataInfo, FileList):
   ID = DataInfo['Name']
   print('Starting ... Toolkit/'+ID)

   #print(Some important information from DataInfo)

   TitleList   = list( i['Title'] for i in FileList )
   while True:
      parfile  = cli.RadioList(  title='>>> '+ID, desc=TitleList,
                                 question='Which type of plot you want to check out?' )
      if parfile=='q':  # Quit NCEP_viewer
         print('')
         return
      else:
         currentscope = {}
         fname    = DataInfo['Path']+FileList[parfile]['File']
         f        = open(fname,'r')
         exec(f.read(),currentscope)
         f.close()
         Figures  = currentscope['FIG']

      CardList    = [ i['Description'] for i in Figures ]
      while True:
         want2c = cli.RadioList( title='>>> '+ID+' >>> '+FileList[parfile]['Title'],
                                 desc=CardList,
                                 question='Which plot you want to take a look at?' )
         if want2c=='q':  break
         else:
            onecard = PlotCard(Figures[want2c],Tag=FileList[parfile]['Tag'],
                               DataPath=DataInfo['Path'],PlotPath='../plot/')
            onecard.makeplot()

