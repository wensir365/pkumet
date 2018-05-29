#!/usr/bin/env python3

import os
import kit_todolist
import kit_ncepviewer
import kit_wikipedia
import kit_wolframalpha
#import kit_weather
#import kit_mp3player

from mod_color import *
c_h   = c_blue2

cmddict = {
   'quit'   : ['q','bye','quit','exit','byebye','bi','by','zaijian','88','拜拜'],
   'clear'  : ['c','clear','clean','cls','清屏'],
   'help'   : ['h','help','man','ls','ll','帮助'],
          }

kitdict = {
   'todo'   : ['t','to','todo','to-do'],
   'ncep'   : ['n','ncep','ncep/ncar','ncep-ncar','ncep1','再分析'],
   'wiki'   : ['wi','wiki','wikipedia','维基'],
   'wolf'   : ['wo','wolf','wolfram','wolframalpha','math','mathematica'],
#   'weather': ['we','wea','weather','天气'],
#   'mp3'    : ['m','mp3','music','音乐'],
          }

def do_help():
   print(c_h+'Command:'+c_n)
   print('   h/help/man    Help                                查看帮助')
   print('   c/clear/cls   Clear screen                        清屏')
   print('   ![cmd]        Excute OS/shell command             执行外层系统命令')
   print('   q/bye/quit/88 Quit                                退出')
   print(c_h+'Toolkit:'+c_n)
   print('   todo          To-Do List                          要做的事')
   print('   ncep          NCEP/NCAR 1981-2010 Climatology     NCEP1气候态图集')
   print('   wiki          Wikipedia                           伟大的维基百科搜索引擎')
   print('   wolf          WolframAlpha                        数学世界的搜索引擎')
#   print('   weather       Yahoo! Weather                      雅虎天气频道信息')
#   print('   mp3           MP3 Player                          听听音乐，轻松片刻 :-)')
   print('')
   
def do_quit():
   print(c_h+'Have a nice day! Bye~'+c_n)
   print('')

def do_clear():
   os.system('clear')

def do_oscmd(s):
   s = s[1:]
   try:     os.system(s)
   except:  print('运行系统命令出错!')


####################
def core_process(s):
   # cmd: Quit?
   if s.lower()   in cmddict['quit']:
      do_quit()
      return False

   # cmd: Clear?
   elif s.lower() in cmddict['clear']:
      do_clear()

   # cmd: Help?
   elif s.lower() in cmddict['help']:
      do_help()

   # cmd: OS/Shell command?
   elif s[0]=='!':
      do_oscmd(s)

   # toolkit: To-Do List?
   elif s.lower() in kitdict['todo']:
      kit_todolist.go()

   # toolkit: NCEP viewer?
   elif s.lower() in kitdict['ncep']:
      kit_ncepviewer.go()

   # toolkit: Wikipedia?
   elif s.lower() in kitdict['wiki']:
      kit_wikipedia.go()

   # toolkit: WolframAlpha?
   elif s.lower() in kitdict['wolf']:
      kit_wolframalpha.go()

   # toolkit: YahooWeather?
   #elif s.lower() in kitdict['weather']:
   #   kit_weather.go()

   # toolkit: MP3?
   #elif s.lower() in kitdict['mp3']:
   #   kit_mp3player.go()

   # NO process
   else:
      print('Don\'t know your input:', c_red+s+c_n)
      print('What can I do for you? (h for help)')
      print('')

   return True


#################
def service(num):
   while True:
      # Input
      a_request = input(c_h + '[%i]'%num + c_n + ' ? ')

      # PROCESS input
      if len(a_request)>0:
         keeprunning = core_process(a_request)
         return keeprunning
   
