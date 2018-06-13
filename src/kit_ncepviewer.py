#!/usr/bin/env python3

import mod_cli                as cli
import numpy                  as np
import xarray                 as xr
import pprint                 as pp
import mod_pkuplot            as pkuplot

import par_maplatlon          as figll
import par_mapnp              as fignp
import par_mapsp              as figsp
import par_latp               as figlatp
import par_lonp               as figlonp
import par_latt               as figlatt
import par_lont               as figlont
import par_vart               as figvart

def go():
   print('Starting ... Toolkit/NCEP_viewer')

   CatList = [ 'Map: Lat-Lon',
               'Map: Arctic / NH',
               'Map: Antarctica / SH',
               'Cross-section: Lat-Pressure / Lat-Height',
               'Cross-section: Lon-Pressure / Lon-Height',
               'Seasonal cycle: Lat-Month',
               'Seasonal cycle: Lon-Month (i.e. Hovmueller diagram)',
               'Seasonal cycle: Variable-Month', ]

   while True:
      PlotCat  = cli.RadioList(  title='>>> NCEP_viewer', desc=CatList,
                                 question='Which type of plot you want to check out?' )

      # === Category
      if    PlotCat=='q':                          # Quit NCEP_viewer
         print('')
         return
      elif  PlotCat==0:    Figures  = figll.FIG    # Lat-Lon
      elif  PlotCat==1:    Figures  = fignp.FIG    # NH
      elif  PlotCat==2:    Figures  = figsp.FIG    # SH
      elif  PlotCat==3:    Figures  = figlatp.FIG  # Lat-Pres
      elif  PlotCat==4:    Figures  = figlonp.FIG  # Lon-Pres
      elif  PlotCat==5:    Figures  = figlatt.FIG  # Lat-Month
      elif  PlotCat==6:    Figures  = figlont.FIG  # Lon-Month
      elif  PlotCat==7:    Figures  = figvart.FIG  # Var-Month
      else:
         print('go: unknown category %i'%PlotCat)

      # === Into current CAT: Setup
      DescList    = [ i['Description'] for i in Figures ]

      # === Into current CAT: Choose and Plotting
      while True:
         want2c = cli.RadioList( title='>>> NCEP_viewer >>> '+CatList[PlotCat],
                                 desc=DescList,
                                 question='Which plot you want to take a look at?' )
         if want2c=='q':  break
         else:
            plot = ncep1viewer(PlotCat, Figures[want2c])
            plot.makeplot()


#################
class ncep1viewer():
   def __init__(self,Category,FigureDict):
      self.Cat       = Category
      self.F         = FigureDict
      self.plotpath  = '../plot/'
      self.datapath  = '../data/'

      print('\n <ncep1viewer> ---> a FIG dictionary loaded:')
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
            fout=self.plotpath+'Cat'+str(self.Cat)+'.'+self.F['FileOut'] )

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
            fout=self.plotpath+'Cat'+str(self.Cat)+'.'+self.F['FileOut'] )

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
            fout=self.plotpath+'Cat'+str(self.Cat)+'.'+self.F['FileOut'] )

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
            fout=self.plotpath+'Cat'+str(self.Cat)+'.'+self.F['FileOut'] )

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
            fout=self.plotpath+'Cat'+str(self.Cat)+'.'+self.F['FileOut'] )

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
            fout=self.plotpath+'Cat'+str(self.Cat)+'.'+self.F['FileOut'] )

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
            fout=self.plotpath+'Cat'+str(self.Cat)+'.'+self.F['FileOut'] )

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
            fout=self.plotpath+'Cat'+str(self.Cat)+'.'+self.F['FileOut'] )

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
            fout=self.plotpath+'Cat'+str(self.Cat)+'.'+self.F['FileOut'] )

      #  Others
      else:
         print('ncep1viewer/makeplot: an unknown FIGURE TYPE=',self.F['TYPE'])
         print('ncep1viewer/makeplot: 不能识别的 FIGURE TYPE=',self.F['TYPE'])

