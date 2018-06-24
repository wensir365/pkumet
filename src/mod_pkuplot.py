#!/usr/bin/env python3

# Plotting functions with python3 + matplotlib + basemap
# Xinyu Wen, Peking Univ, June 2018

import numpy                  as np
import mpl_toolkits.basemap   as bm
import matplotlib.pyplot      as plt

# List of Functions
'''
def timeavg(x,month):
def zonalavg(x,lons):
def meriavg(x,lats):

def plot2d_latlon(data2d,lon1d,lat1d)
def plotvector_latlon(U2d,V2d,lon1d,lat1d)
def plot2d_polar( data2d,lon1d,lat1d)
def plotvector_polar( U2d,V2d,lon1d,lat1d)
def plot2d_contour(x1d,y1d,z2d)
def plot1d_timeseries1(x,y)
'''


#=================#
#///// TOOLS \\\\\#
#=================#

#################
def timeavg(x,month):
   monthpick   = {   'DJF': [0,1,11],
                     'MAM': [2,3,4],
                     'JJA': [5,6,7],
                     'SON': [8,9,10]   }
   print(' <timeavg> ---> performing time average: ',month)
   print('')

   if    month=='ANN':  # ANN mean
      y  = np.mean(x,axis=0)
   elif  month=='DJF':  # DJF
      y  = np.mean(x[monthpick['DJF'],...],axis=0)
   elif  month=='MAM':  # MAM
      y  = np.mean(x[monthpick['MAM'],...],axis=0)
   elif  month=='JJA':  # JJA
      y  = np.mean(x[monthpick['JJA'],...],axis=0)
   elif  month=='SON':  # SON
      y  = np.mean(x[monthpick['SON'],...],axis=0)
   else:          # Single month, 1-12:Jan-Dec
      y = x.isel(time=month-1)
   return y


#################
def zonalavg(x,lons):
   print(' <zonalavg> ---> performing zonal average ', lons[0],'->',lons[1])
   print('')
   y  = np.mean(x.sel(lon=slice(lons[0],lons[1])),axis=-1)
   return y


#################
def meriavg(x,lats):
   print(' <meridionalavg> ---> performing meridional average ', lats[0],'->',lats[1])
   print('')

   lat = x.lat
   if    (lat[1]-lat[0])>0:
      y  = np.mean(x.sel(lat=slice(lats[0],lats[1])),axis=-2)
   elif  (lat[1]-lat[0])<0:
      y  = np.mean(x.sel(lat=slice(lats[1],lats[0])),axis=-2)
   else:
      print('<meriavg>: Unknown latitudes')
   return y



#==========================#
#///// PLOT FUNCTIONS \\\\\#
#==========================#

#################
def plot2d_latlon(data2d,lon1d,lat1d,clev=[],addcy=True,
                  domain=[-90,90,0,360],res='c',lat23=False,country=False,
                  cm='jet',cbarstr='',ti='',fout='figure.pdf',
                  maxminmarker=False,
                  ):
   '''
   =================================================================================================
   PLOT 2D DATA ON A LAT-LON MAP

   Apr 2018
   Xinyu Wen, xwen@pku.edu.cn, Peking Univ
   -------------------------------------------------------------------------------------------------
   Argument    Default        Description                      Example
   -------------------------------------------------------------------------------------------------
   data2d      REQUIRED       Data you want to plot            Z500(lat,lon)
   lon1d,lat1d REQUIRED       Longitude and latitude
   clev        []             Color levels                     np.arange(-40,41,5); list(range(...))
   addcy       True           Want to add a cyclic lon?
   domain      [-90,90,0,360] Domain to plot                   [Lat_s,Lat_n,Lon_w,Lon_e]
   res         'c'            Map resolution
   lat23       False          Want to draw 南北回归线和极圈线
   country     False          Want to draw country lines
   cm          'jet'          Colormap you want to use
   cbarstr     ''             String besides the colorbar      'Celsius'
   ti          ''             Title of the plot
   fout        'figure.pdf'   Filename for figure saving
   =================================================================================================
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
   if maxminmarker:
      maxj,maxi = np.unravel_index(np.argmax(data2d), data2d.shape)
      minj,mini = np.unravel_index(np.argmin(data2d), data2d.shape)

      lonmax,latmax  = lon1d[maxi],lat1d[maxj]
      lonmin,latmin  = lon1d[mini],lat1d[minj]

      if not((maxi,maxj,mini,minj)==(0,0,0,0)):
         # Marker
         m.scatter(lonmax,latmax,s=600,marker='o',color='k',edgecolors='w')
         m.scatter(lonmin,latmin,s=600,marker='o',color='k',edgecolors='w')
         # Add text
         plt.text(lonmax,latmax,'M',fontsize=12,ha='center',va='center',color='w')
         plt.text(lonmin,latmin,'m',fontsize=12,ha='center',va='center',color='w')

   # Save & close
   plt.savefig(fout)
   plt.show()
   plt.close()

   # Ending message
   print('\n <plot2d_latlon> ---> the figure was saved into: %s \n'%fout)
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
   plt.show()
   plt.close()

   # Ending message
   print('\n <plotvector_latlon> ---> the figure was saved into: %s \n'%fout)
   return


#################
def plot2d_polar( data2d,lon1d,lat1d,clev=[],addcy=True,
                  domain=[20,90,0,360],res='c',lat23=False,country=False,
                  cm='jet',cbarstr='',ti='',fout='figure.pdf'
                  ):

   # Defined and open papersize
   papersize_letter  = (11,8.5)
   papersize_a4      = (11.7,8.27)
   plt.figure(figsize=papersize_a4)

   # Base map
   if domain[0]==-90:
      proj = 'spaeqd'
      latbound = domain[1]
      caseid = 'SP'

   if domain[1]==90:
      proj = 'npaeqd'
      latbound = domain[0]
      caseid = 'NP'

   m = bm.Basemap(   projection=proj,resolution=res,
                     boundinglat=latbound, lon_0=domain[2] )

   # Draw latitude lines
   m.drawparallels(np.arange(-90,91,30),color='black',dashes=[5,3],linewidth=0.2)
   if lat23: m.drawparallels([23.5,90-23.5,-23.5,-90+23.5],
                             color='white',dashes=[9999,1],linewidth=0.5)

   # Draw longitude lines
   m.drawmeridians(np.arange(0,361,30),color='black',dashes=[5,3],linewidth=0.2,
                   labels=[True,True,True,True])
   m.drawmeridians([0,90,180,270],color='black',dashes=[9999,1],linewidth=0.5)

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
   cbar = m.colorbar(fig,size='3%',pad='10%')
   cbar.set_label(cbarstr)

   # Title
   plt.title(ti+'\n',fontsize=18)

   # Marking Max/Min points
   maxj,maxi = np.unravel_index(np.argmax(data2d), data2d.shape)
   minj,mini = np.unravel_index(np.argmin(data2d), data2d.shape)

   lonmax,latmax  = lon1d[maxi],lat1d[maxj]
   lonmin,latmin  = lon1d[mini],lat1d[minj]

   m.scatter(lonmax,latmax,s=600,marker='o',color='k',edgecolors='w',latlon=True)
   m.scatter(lonmin,latmin,s=600,marker='o',color='k',edgecolors='w',latlon=True)

   # Add text
   lonmax,latmax  = m(lonmax,latmax)
   lonmin,latmin  = m(lonmin,latmin)
   plt.text(lonmax,latmax,'M',fontsize=12,ha='center',va='center',color='w')
   plt.text(lonmin,latmin,'m',fontsize=12,ha='center',va='center',color='w')

   # Save & close
   plt.savefig(fout)
   plt.show()
   plt.close()

   # Ending message
   print('\n <plot2d_polar> ---> the figure was saved into: %s \n'%fout)
   return


#################
def plotvector_polar( U2d,V2d,lon1d,lat1d,density=2,veclen=10,minshaft=2,
                      addcy=False,domain=[-90,90,0,360],res='c',lat23=False,country=False,
                      cbarstr='',ti='',fout='figure.pdf'):

   # Defined and open papersize
   papersize_letter  = (11,8.5)
   papersize_a4      = (11.7,8.27)     # default
   plt.figure(figsize=papersize_a4)

   # Base map
   if domain[0]==-90:
      proj = 'spaeqd'
      latbound = domain[1]
      caseid = 'SP'

   if domain[1]==90:
      proj = 'npaeqd'
      latbound = domain[0]
      caseid = 'NP'

   m = bm.Basemap(   projection=proj,resolution=res,
                     boundinglat=latbound, lon_0=domain[2] )

   # Draw latitude lines
   m.drawparallels(np.arange(-90,91,30),color='black',dashes=[5,3],linewidth=0.2)
   if lat23: m.drawparallels([23.5,90-23.5,-23.5,-90+23.5],
                             color='white',dashes=[9999,1],linewidth=0.5)

   # Draw longitude lines
   m.drawmeridians(np.arange(0,361,30),color='black',dashes=[5,3],linewidth=0.2,
                   labels=[True,True,True,True])
   m.drawmeridians([0,90,180,270],color='black',dashes=[9999,1],linewidth=0.5)

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

   m.scatter(lonmax,latmax,s=600,marker='o',color='k',edgecolors='w',latlon=True)
   m.scatter(lonmin,latmin,s=600,marker='o',color='k',edgecolors='w',latlon=True)

   # Add text
   lonmax,latmax = m(lonmax,latmax)
   lonmin,latmin = m(lonmin,latmin)
   plt.text(lonmax,latmax,'M',fontsize=12,ha='center',va='center',color='w')
   plt.text(lonmin,latmin,'m',fontsize=12,ha='center',va='center',color='w')

   # Save & close
   plt.savefig(fout)
   plt.show()
   plt.close()

   # Ending message
   print('\n <plotvector_latlon> ---> the figure was saved into: %s \n'%fout)
   return


#################
def plot2d_contour(x1d,y1d,z2d, 
                   add_contour=False, num_contours=8,
                   xticks=[],yticks=[],
                   ti='Title', xl='X', yl='Y',
                   yreverse=False,xreverse=False,
                   clev=[], cm='jet', cbarstr='',
                   fout='figure.pdf'):
   
   # Defined and open papersize
   papersize_letter  = (11,8.5)
   papersize_a4      = (11.7,8.27)
   papersize_my      = (14,6)
   plt.figure(figsize=papersize_my)

   # Plotting
   if len(clev)>0:
      fig = plt.contourf(x1d,y1d,z2d,clev,cmap=cm)
   else:
      fig = plt.contourf(x1d,y1d,z2d,cmap=cm)
   
   if add_contour:
      cs  = plt.contour(x1d,y1d,z2d,num_contours,colors='k',linewidths=1)
      plt.clabel(cs,fontsize=10,inline=1,fmt='%1.0f')

   # Ticks
   if xticks!=[]: plt.xticks(xticks)
   if yticks!=[]: plt.yticks(yticks)

   # Reverse X or Y
   if xreverse: plt.gca().invert_xaxis()
   if yreverse: plt.gca().invert_yaxis()

   # Colorbar
   cbar = plt.colorbar(fig)
   cbar.set_label(cbarstr)

   # Title
   plt.title(ti,fontsize=18)
   plt.xlabel(xl,fontsize=16)
   plt.ylabel(yl,fontsize=16)

   # Marking Max/Min points
   maxj,maxi = np.unravel_index(np.argmax(z2d), z2d.shape)
   minj,mini = np.unravel_index(np.argmin(z2d), z2d.shape)

   #plt.scatter(x1d[maxi],y1d[maxj],s=600,marker='o',color='k',edgecolors='w')
   #plt.scatter(x1d[mini],y1d[minj],s=600,marker='o',color='k',edgecolors='w')

   # Add text
   plt.text(x1d[maxi],y1d[maxj],'M',fontsize=26,ha='center',va='center',color='w')
   plt.text(x1d[mini],y1d[minj],'m',fontsize=26,ha='center',va='center',color='w')

   # Save & close
   plt.savefig(fout)
   plt.show()
   plt.close()

   # Ending message
   print('\n <plot2d_contour> ---> the figure was saved into: %s \n'%fout)
   return


#################
def plot1d_timeseries1( x,y,style='b-o',lw=2,
                        xl='X',yl='Y',
                        xlim=[],ylim=[],ylog=False,
                        xticks=[],yticks=[],
                        ti='Plot Title',figsize=(9,4.5),fout="plot_ts.pdf"):

   plt.figure(figsize=figsize)

   plt.plot(x,y,style,linewidth=lw)

   plt.title(ti)
   plt.xlabel(xl)
   plt.ylabel(yl)

   # Range of X and Y
   showsigma   = 2.0    # 2 Sigma
   showmargin  = 0.1    # 10% of y_range

   y_mean   = np.mean(y)
   y_sigma  = np.std(y)
   y_max    = np.max(y)
   y_min    = np.min(y)
   y_range  = y_max-y_min

   xlim     = (np.min(x)-0.5,np.max(x)+0.5)
   #ylim     = (y_mean-showsigma*y_sigma,y_mean+showsigma*y_sigma)
   ylim     = (y_min-showmargin*y_range, y_max+showmargin*y_range)
   if xlim: plt.xlim(xlim[0],xlim[1])
   if ylim: plt.ylim(ylim[0],ylim[1])
   if ylog: plt.yscale('log')

   # Ticks
   if xticks!=[]: plt.xticks(xticks)
   if yticks!=[]: plt.yticks(yticks)

   plt.savefig(fout)
   plt.show()
   plt.close()

   # Ending message
   print('\n <plot1d_timeseries1> ---> the figure was saved into: %s \n'%fout)
   return
