#!/usr/bin/env python3

import matplotlib
matplotlib.use('Agg')

import mod_cli                as cli
import numpy                  as np
import xarray                 as xr
import mpl_toolkits.basemap   as bm
import matplotlib.pyplot      as plt

import par_maplatlon          as figll

def go():
   print('Starting ... Toolkit/NCEP_viewer')

   CatList = [ 'Quit NCEP_viewer',
               'Lat-Lon maps',
               'Northern Hemisphere / Arctic maps        (N/A)',
               'Southern Hemisphere / Antarctica maps    (N/A)',
               'Lat-Pressure / Lat-Height plots          (N/A)',
               'Lon-Pressure / Lon-Height plots          (N/A)',
               'Variable-Month / Seasonal-cycle plots    (N/A)',
               'Lat-Month / Seasonal-cycle plots         (N/A)',
               'Lon-Month / Seasonal-cycle plots         (N/A)'        ]
   
   CatScrn = cli.selector(
               '>>> NCEP_viewer',
               CatList,
               'Which type of plot you want to check out?',
               'Just input a number within %i >>> %i'%(0,len(CatList)-1) )

   while True:
      PlotCat  = CatScrn.show_and_get()

      # === Category
      if    PlotCat==0:                            # Quit NCEP_viewer
         print('')
         break
      elif  PlotCat==1:    Figures  = figll.FIG    # Lat-Lon
      elif  PlotCat==2:    break                   # NH
      elif  PlotCat==3:    break                   # SH
      elif  PlotCat==4:    break                   # Lat-Pres
      elif  PlotCat==5:    break                   # Lon-Pres
      elif  PlotCat==6:    break                   # Var-Month
      elif  PlotCat==7:    break                   # Lat-Month
      elif  PlotCat==8:    break                   # Lon-Month
      else:
         print('go: unknown category %i'%PlotCat)

      # === Into current CAT: Setup plots
      DescList    = ['Quit to upper level'] + list( i['Description'] for i in Figures )
      WhichPlot   = cli.selector(
                     '>>> NCEP_viewer >>> '+CatList[PlotCat],
                     DescList,
                     'Which plot you want to take a look at?',
                     'Just input a number within %i >>> %i'%(0,len(DescList)-1)  )

      # === Into current CAT: Choose and Plotting
      while True:
         want2c = WhichPlot.show_and_get()
         if want2c==0:  break
         else:
            plot = ncep1viewer(PlotCat, Figures[want2c-1])
            plot.makeplot()
   return


#################
class ncep1viewer():
   def __init__(self,Category,FigureDict):
      self.Cat       = Category
      self.F         = FigureDict
      self.plotpath  = '../plot/'
      self.datapath  = '../data/'

      print('\n <ncep1viewer> ---> a FIG dictionary loaded:')
      print('')
      print(self.F)
      print('')

   def makeplot(self):
      # ===== Read data
      Nfile = len(self.F['FileIn'])
      f     = []
      for i in range(Nfile):
         f.append(xr.open_dataset(self.datapath+self.F['FileIn'][i],decode_times=False))
      z        = eval(self.F['Compute'])

      # ===== Figure Category
      #  Lat-Lon
      if    self.Cat    == 1: 
         if    self.F['TYPE']=='pres-lat-lon':
            z = z.sel(level=self.F['PresLev'])
            z = z.isel(time=self.F['Month']-1)
            plot2d_latlon(z, z.lon, z.lat, clev=eval(self.F['Levels']),
               country=self.F['CountryLine'],
               domain=self.F['Domain'], cm=self.F['ColorMap'],
               cbarstr='Unit: %s\nM=%0.2f, m=%0.2f'%(self.F['Unit'],np.max(z),np.min(z)),
               ti=self.F['FigTitle'], fout=self.plotpath+str(self.Cat)+'.'+self.F['FileOut'])

         elif  self.F['TYPE']=='lat-lon':
            z = z.isel(time=self.F['Month']-1)
            plot2d_latlon(z, z.lon, z.lat, clev=eval(self.F['Levels']),
               country=self.F['CountryLine'],
               domain=self.F['Domain'], cm=self.F['ColorMap'],
               cbarstr='Unit: %s\nM=%0.2f, m=%0.2f'%(self.F['Unit'],np.max(z),np.min(z)),
               ti=self.F['FigTitle'], fout=self.plotpath+str(self.Cat)+'.'+self.F['FileOut'])

         elif  self.F['TYPE']=='pres-lat-lon-vec':
            u,v   = z
            u     = u.sel(level=self.F['PresLev'])
            u     = u.isel(time=self.F['Month']-1)
            v     = v.sel(level=self.F['PresLev'])
            v     = v.isel(time=self.F['Month']-1)
            spd   = np.sqrt(u*u+v*v)
            plotvector_latlon(u,v,u.lon,u.lat,
               domain=self.F['Domain'], density=self.F['Density'], veclen=self.F['VecLen'],
               country=self.F['CountryLine'],
               cbarstr='%s\nM=%0.2f, m=%0.2f'%(self.F['Unit'],np.max(spd),np.min(spd)),
               ti=self.F['FigTitle'], fout=self.plotpath+str(self.Cat)+'.'+self.F['FileOut'])

      #  NH
      elif  self.Cat    == 2: pass

      #  SH
      elif  self.Cat    == 3: pass

      #  Lat-Pres
      elif  self.Cat    == 4: pass

      #  Lon-Pres
      elif  self.Cat    == 5: pass

      #  Var-Month
      elif  self.Cat    == 6: pass

      #  Lat-Month
      elif  self.Cat    == 7: pass

      #  Lon-Month
      elif  self.Cat    == 8: pass

      else:
         print('makeplot: 不能识别的Category')

      return


#################
def plotvector_latlon(U2d,V2d,lon1d,lat1d,density=2,veclen=10,minshaft=2,
                      addcy=False,domain=[-90,90,0,360],res='c',lat23=False,country=False,
                      cbarstr='',ti='',fout='figure.pdf'):

   # Defined and open papersize
   papersize_letter  = (11,8.5)
   papersize_a4      = (11.7,8.27)     # default
   plt.figure(figsize=papersize_a4)

   # Base map
   m = bm.Basemap( projection='cyl',resolution=res,
                   llcrnrlat=domain[0],urcrnrlat=domain[1],
                   llcrnrlon=domain[2],urcrnrlon=domain[3])

   # Draw latitude lines
   m.drawparallels(np.arange(-90,91,30),
                   color='gray',dashes=[1,99999],linewidth=0.1,labels=[1,0,0,0])
   m.drawparallels([0],color='black',dashes=[99999,1],linewidth=0.2)
   if lat23: m.drawparallels([23.5,90-23.5,-23.5,-90+23.5],
                             color='black',dashes=[1,1],linewidth=0.1)

   # Draw longitude lines
   m.drawmeridians(np.arange(0,361,30),
                   color='gray',dashes=[1,99999],linewidth=0.1,labels=[0,0,0,1])
   m.drawmeridians([180,],color='black',dashes=[99999,1],linewidth=0.2)

   # Draw coast and country lines
   m.drawcoastlines()
   if country: m.drawcountries()

   # Prepare lon2d & lat2d
   if addcy: data2d,lon1d = bm.addcyclic(data2d,lon1d)
   lon2d,lat2d = np.meshgrid(lon1d,lat1d)

   # Plotting
   itv = density
   fig = m.quiver(lon2d[::itv,::itv],lat2d[::itv,::itv],U2d[::itv,::itv],V2d[::itv,::itv],
                  latlon=True, minshaft=minshaft)
   lgd = plt.quiverkey(fig,0.92,-0.1, veclen,'%i %s'%(veclen,cbarstr), labelpos='S')

   # Title
   plt.title(ti+'\n',fontsize=18)

   # Marking Max/Min points
   data2d = np.sqrt(U2d*U2d+V2d*V2d)
   maxj,maxi = np.unravel_index(np.argmax(data2d), data2d.shape)
   minj,mini = np.unravel_index(np.argmin(data2d), data2d.shape)

   lonmax,latmax  = lon1d[maxi],lat1d[maxj]
   lonmin,latmin  = lon1d[mini],lat1d[minj]

   m.scatter(lonmax,latmax,s=600,marker='o',color='k',edgecolors='w')
   m.scatter(lonmin,latmin,s=600,marker='o',color='k',edgecolors='w')

   # Add text
   plt.text(lonmax,latmax,'M',fontsize=12,ha='center',va='center',color='w')
   plt.text(lonmin,latmin,'m',fontsize=12,ha='center',va='center',color='w')

   # Save & close
   plt.savefig(fout)
   #plt.show()
   plt.close()

   # Ending message
   print('\n <plotvector_latlon> ---> the figure was saved into: %s \n'%fout)
   return


#################
def plot2d_latlon(data2d,lon1d,lat1d,clev=[],addcy=True,
                  domain=[-90,90,0,360],res='c',lat23=False,country=False,
                  cm='jet',cbarstr='',ti='',fout='figure.pdf'
                  ):
   '''
   =========================================================================================================
   PLOT 2D DATA ON A LAT-LON MAP

   Apr 2018
   Xinyu Wen, xwen@pku.edu.cn, Peking Univ
   ---------------------------------------------------------------------------------------------------------
   Argument    Default        Description                      Example
   ---------------------------------------------------------------------------------------------------------
   data2d      REQUIRED       Data you want to plot            like Z500(lat,lon)
   lon1d,lat1d REQUIRED       Longitude and latitude
   clev        []             Color levels                     like np.arange(-40,41,5) or list(range(...))
   addcy       True           Want to add a cyclic lon?
   domain      [-90,90,0,360] Domain to plot                   like [Lat_s,Lat_n,Lon_w,Lon_e]
   res         'c'            Map resolution
   lat23       False          Want to draw 南北回归线和极圈线
   country     False          Want to draw country lines
   cm          'jet'          Colormap you want to use
   cbarstr     ''             String besides the colorbar      like 'Celsius'
   ti          ''             Title of the plot
   fout        'figure.pdf'   Filename for figure saving
   =========================================================================================================
   '''

   # Defined and open papersize
   papersize_letter  = (11,8.5)
   papersize_a4      = (11.7,8.27)     # default
   plt.figure(figsize=papersize_a4)

   # Base map
   m = bm.Basemap( projection='cyl',resolution=res,
                     llcrnrlat=domain[0],urcrnrlat=domain[1],
                     llcrnrlon=domain[2],urcrnrlon=domain[3])

   # Draw latitude lines
   m.drawparallels(np.arange(-90,91,30),
                   color='gray',dashes=[1,9999],linewidth=0.1,labels=[1,0,0,0])
   m.drawparallels([0],color='black',dashes=[9999,1],linewidth=0.2)
   if lat23: m.drawparallels([23.5,90-23.5,-23.5,-90+23.5],
                             color='black',dashes=[1,1],linewidth=0.1)

   # Draw longitude lines
   m.drawmeridians(np.arange(0,361,30),
                   color='gray',dashes=[1,9999],linewidth=0.1,labels=[0,0,0,1])
   m.drawmeridians([180,],color='black',dashes=[9999,1],linewidth=0.2)

   # Draw coast and country lines
   m.drawcoastlines()
   if country: m.drawcountries()

   # Prepare lon2d & lat2d
   if addcy: data2d,lon1d = bm.addcyclic(data2d,lon1d)
   lon2d,lat2d = np.meshgrid(lon1d,lat1d)

   # Plotting
   if len(clev)>0:
      fig = m.contourf(lon2d,lat2d,data2d,clev,latlon=True,cmap=cm)
   else:
      fig = m.contourf(lon2d,lat2d,data2d,     latlon=True,cmap=cm)

   # Colorbar
   cbar = m.colorbar(fig,size='2%')
   cbar.set_label(cbarstr)

   # Title
   plt.title(ti+'\n',fontsize=18)

   # Marking Max/Min points
   maxj,maxi = np.unravel_index(np.argmax(data2d), data2d.shape)
   minj,mini = np.unravel_index(np.argmin(data2d), data2d.shape)

   lonmax,latmax  = lon1d[maxi],lat1d[maxj]
   lonmin,latmin  = lon1d[mini],lat1d[minj]

   m.scatter(lonmax,latmax,s=600,marker='o',color='k',edgecolors='w')
   m.scatter(lonmin,latmin,s=600,marker='o',color='k',edgecolors='w')

   # Add text
   plt.text(lonmax,latmax,'M',fontsize=12,ha='center',va='center',color='w')
   plt.text(lonmin,latmin,'m',fontsize=12,ha='center',va='center',color='w')

   # Save & close
   plt.savefig(fout)
   #plt.show()
   plt.close()

   # Ending message
   print('\n <plot2d_latlon> ---> the figure was saved into: %s \n'%fout)
   return

