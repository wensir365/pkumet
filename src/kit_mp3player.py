#!/usr/bin/env python3

import os
import vlc
import mod_cli                as cli

def go():
   print('Starting ... Toolkit/MP3_Player')

   mp3path  = '../mp3/'
   filelist = os.listdir(mp3path)

   playlist = ['Quit']
   playlist = playlist + filelist
   
   PlayScrn = cli.selector(
               '>>> MP3_player',
               playlist,
               'Which song you want to play?',
               'Just input a number within %i >>> %i'%(0,len(playlist)-1) )

   while True:
      nowsong  = PlayScrn.show_and_get()

      if    nowsong==0:
         try:
            NOW.stop()
            del NOW
            print('Stop playing, and quit...')
            print('')
            break
         except:
            print('')
            break

      else:
         try:
            NOW.stop()
            del NOW
            print('')
            print('Stop an old player')
            print('Start a new player:',playlist[nowsong])
         except:
            print('')
            print('Start a new player:',playlist[nowsong])

         NOW = vlc.MediaPlayer(mp3path+playlist[nowsong])
         NOW.play()

   return

