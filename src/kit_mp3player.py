#!/usr/bin/env python3

import os
import vlc
import mod_pkucli    as cli

def go():
   print('Starting ... Toolkit/MP3_Player')

   mp3path  = '../mp3/'
   filelist = os.listdir(mp3path)

   while True:
      nowsong  = cli.RadioList(  title='MP3 files at '+mp3path,
                                 desc=filelist,
                                 fkey=['p','c','s','q'],
                                 fdesc=['Pause','Continue','Stop','Stop and quit'],
                                 question='Which song you want to play?' )

      # Stop and Quit
      if    nowsong=='q':
         try:
            NOW.stop()
            del NOW
            print('Stop playing, and quit ...')
            print('')
            break
         except:
            print('')
            break

      # Stop
      elif  nowsong=='s':
         try:
            NOW.stop()
            del NOW
            print('Stop playing')
         except:
            print('Nothing to stop ...')

      # Pause
      elif  nowsong=='p':
         try:
            NOW.pause()
            print('Pause playing')
         except:
            print('Nothing to pause ...')

      # Continue
      elif  nowsong=='c':
         try:
            NOW.play()
            print('Continue playing')
         except:
            print('Nothing to continue ...')

      # Play a song
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

