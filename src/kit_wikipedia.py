#!/usr/bin/env python3

import os
import wikipedia        as wiki
import mod_pkucli       as cli
from mod_color          import *

def go():
   print('Starting ... Toolkit/Wikipedia')

   run = True
   while run:
      cli.Separator()#print('')
      query = cli.InputBox('What you want to check w/ Wikipedia?','[Q] ','Keywords (q for Quit): ')
      if query in {'0','q','bye','quit','exit'}:
         run = False
         print('')
      else:
         try:
            print('    '+'OK, searching '+c_p+query+c_n+' ...\n')
            result   = wiki.summary(query)
            print(result)
            if cli.YesNoDefault('\nText To Speech (TTS)?'):
               print('Press CTRL+C to stop ...')
               os.system('say "%s"'%result)
         except:
            print('\nSorry, didn\'t find any info for %s from Wikipedia auto-suggestion system.'
                  %(c_red+query+c_n))
   return

