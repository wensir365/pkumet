#!/usr/bin/env python3

import os
import wikipedia        as wiki
import mod_cli          as cli
from mod_color          import *

def go():
   print('Starting ... Toolkit/Wikipedia')

   qa = cli.q_and_a('Please input some key words to check w/ Wikipedia (q|0 for Quit)?')

   run = True
   while run:
      query = qa.show_and_get()
      if query in {'0','q','bye','quit','exit'}:
         run = False
         print('')
      else:
         try:
            result   = wiki.summary(query)
            print('\n%s'%result)
            if cli.yesno('\nText To Speech (TTS)?'):
               try:
                  print('Press CTRL+C to stop ...')
                  os.system('say "%s"'%result)
               except:
                  print('Sorry, this function ONLY works for Mac OS system so far.')
                  
         except:
            print('\nSorry, didn\'t find any info for %s from Wikipedia auto-suggestion system.'
                  %(c_red+query+c_n))
   return

