#!/usr/bin/env python3

import wolframalpha  as wolf
import mod_pkucli    as cli
from mod_color       import *

def go():
   print('Starting ... Toolkit/WolframAlpha')

   AppID    = 'K2U2TH-TR74L9WEH3'   # "MetAssistant" App ID, don't use it illegally!
   MyWolf   = wolf.Client(AppID)

   run = True
   while run:
      print('')
      query = cli.InputBox('What you want to check w/ WolframAlpha?','[Q] ','Keywords (q for Quit): ')
      if query in {'0','q','bye','quit','exit'}:
         run = False
         print('')
      else:
         try:
            print('    '+'OK, searching '+c_p+query+c_n+' ...\n')
            result   = MyWolf.query(query)
            result2  = next(result.results).text
            print(result2)
         except:
            print('\nSorry, didn\'t find any info for %s from WolframAlpha.'
                  %(c_red+query+c_n))
   return

