#!/usr/bin/env python3

import mod_service

if __name__=='__main__':

   # init
   print('----------------')
   print('  MetAssistant  ')
   print('----------------')
   print('What can I do for you? (h for help)')

   # main loop
   ii = 0
   running = True
   while running:
      ii+=1
      running = mod_service.service(ii)

   # ending

