#!/usr/bin/env python3

import wolframalpha  as wolf
import mod_cli       as cli
from mod_color       import *

def go():
   print('Starting ... Toolkit/WolframAlpha')

   AppID    = 'K2U2TH-TR74L9WEH3'   # "MetAssistant" App ID, don't use it illegally!
   MyWolf   = wolf.Client(AppID)

   qa = cli.q_and_a('Please input some key words to check w/ WolframAlpha (q|0 for Quit)?')

   run = True
   while run:
      query = qa.show_and_get()
      if query in {'0','q','bye','quit','exit'}:
         run = False
         print('')
      else:
         try:
            result   = MyWolf.query(query)
            result2  = next(result.results).text
            print('\n%s'%result2)
         except:
            print('\nSorry, didn\'t find any info for %s from WolframAlpha.'
                  %(c_red+query+c_n))
   return

