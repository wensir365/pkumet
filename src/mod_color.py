#!/usr/bin/env python3

import colorama as cr

# My text colors
#cr.init()      # init for colorama, need only for Windows, where to put cr.deinit()?

c_blue   = cr.Fore.BLUE    + cr.Style.BRIGHT
c_blue2  = cr.Fore.BLUE
c_red    = cr.Fore.RED     + cr.Style.BRIGHT
c_cyan   = cr.Fore.CYAN    + cr.Style.BRIGHT
c_cyan2  = cr.Fore.CYAN
c_yellow = cr.Fore.YELLOW  + cr.Style.BRIGHT
c_green  = cr.Fore.GREEN   + cr.Style.BRIGHT
c_magenta= cr.Fore.MAGENTA + cr.Style.BRIGHT
c_magenta2= cr.Fore.MAGENTA
c_n      = cr.Style.RESET_ALL
c_black  = cr.Style.BRIGHT

c_p      = c_magenta2 # Present
