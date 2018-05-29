#!/usr/bin/env python3

from mod_color          import *

#################
class selector():
   "多项选择器：最终一定返回多项选择的编号，严谨而安全"

   def __init__(self,header,itemlist,question,hint):
      self.header = header
      self.item   = itemlist
      self.q      = question
      self.hint   = hint
      self.N      = len(itemlist)

   def show(self):
      print('')
      for i in range(self.N):
         print('%4i. %s'%(i,self.item[i]))
      print('')

   def show_and_get(self):
      print('\n'+self.header+'\n')
      for i in range(self.N):
         print('%4i. %s'%(i,self.item[i]))
      print('')
      print(c_p+'[Q] '+c_n+self.q)
      ok = False
      while not(ok):
         answer = input(c_p+'[A] '+c_n+'(%i->%i) '%(0,self.N-1))
         if answer in list( str(i) for i in range(self.N) ): ok=True
         elif answer=='999':  self.show()
         else:
            if len(answer)>0:
               print('Sorry, '+c_red+answer+c_n+' is an invalid input.')
               print(c_p+'[H] '+c_n+self.hint)
               print('')
            '''
            else: # just ENTER
               print('Sorry, you input NOTHING.')
               print(c_p+'[H] '+c_n+self.hint)
               print('')
            '''
      return int(answer)


#################
class q_and_a:
   "问答器：最终返回任何答案(不做内容安全判定，简单且极其自由的输入器)"

   def __init__(self,question):
      self.Q = question
      self.A = ''

   def show_and_get(self):
      while True:
         print('')
         print(c_p+'[Q] '+c_n+self.Q)
         result = input(c_p+'[A] '+c_n)
         if len(result)>0: return result


#################
def yesno(question):
   print(question)
   while True:
      answer = input('[yes] or [no] ? ')
      if answer.lower() in {'yes','y'}:   return True
      if answer.lower() in {'no','n'}:    return False

