#!/usr/bin/env python3

'''
- RadioList
- FloatBox
- FloatRangeBox
- IntBox
- IntRangeBox
- YesNo
- YesNoDefault
- InputBox
- InputBoxSimple
- Password1Box
- Password2Box

- PrintList
- PrintMultilineText

- Separator
'''

import numpy as np
import getpass as gp
from mod_color import c_p,c_n,c_red

#################
def RadioList( title='', tag=[], desc=[], fkey=['q'],fdesc=['Quit'],
               question='Which one you prefer?', hint='',prompt='[Q] '):
   "单选列表"
   # Check
   Nlist = len(desc)
   Nf    = len(fkey)
   if tag==[] and Nlist>0:
      tag = ['']*Nlist
   if len(tag)!=len(desc):
      print('Warning: Length of tag and desc are not equal!!!')
      return None
   if len(fkey)!=len(fdesc):
      print('Warning: Length of fkey and fdesc are not equal!!!')
      return None
      
   # Title
   if len(title)>0:  print('\n'+c_p+'[ '+title.upper()+' ]'+c_n)
   print('')

   # Show List
   def showlist(tag,desc):
      try:
         tagmaxlen= max([len(i) for i in tag])
      except:
         tagmaxlen= 0
      for i in range(len(desc)):
         print('%5i  %s  %s'%(i,tag[i].center(tagmaxlen),desc[i]))
   showlist(tag,desc)

   # Show Function Keys
   try:
      tagmaxlen= max([len(i) for i in tag])
      emptytag = tagmaxlen*' '
   except:
      emptytag = ''
   for i in range(Nf):
      print((c_p+'%5s'+c_n+'  %s  %s')%(fkey[i],emptytag,fdesc[i]))
   print('')

   # Show Question
   cp = c_p+prompt+c_n
   bp = ' '*len(prompt)
   print(cp+question)

   # Get Answer
   if    Nlist==0: ansrange1 = ''
   elif  Nlist==1: ansrange1 = '0'
   elif  Nlist>1:  ansrange1 = '%i-->%i'%(0,Nlist-1)

   if len(ansrange1)>0:
      ansrange = ','.join([ansrange1]+fkey)
   else:
      ansrange = ','.join(fkey)
   if len(ansrange)>0:  ansrange = '('+ansrange+')'

   anslist  = [str(i) for i in range(Nlist)]

   while True: 
      answer = input(bp+ansrange+': ')
      if    answer in anslist:
         return int(answer)
      elif  answer in fkey:
         return answer
      elif  answer=='999':    # reserve for future extension
         print(bp+'Reserved option, so fat just show the current list:')
         showlist(tag,desc)
         pass
      else:
         if len(answer)>0:
            print(bp+'Sorry, '+c_red+answer+c_n+' is NOT a valid input.')
            #print(c_p+'Hint: '+c_n+hint)
            #print('')


#################
def CheckList():
   "多选列表"
   pass

#################
def FloatBox(question,prompt=''):
   "浮点数"
   cp = c_p+prompt+c_n
   bp = ' '*len(prompt)
   print(cp+question)
   while True:
      answer = input(bp+'Please input a float: ')
      try:
         z = float(answer)
         return z
      except:
         pass

#################
def FloatRangeBox(question,zrange=[-np.inf,np.inf],prompt=''):
   "浮点数，在一定范围内"
   zmin, zmax = zrange
   cp = c_p+prompt+c_n
   bp = ' '*len(prompt)
   print(cp+question)
   while True:
      answer = input(bp+'Please input a float in [%.2f,%.2f]: '%(zmin,zmax))
      try:
         z = float(answer)
         if zmin<=z<=zmax:
            return z
      except:
         pass

#################
def IntBox(question,prompt=''):
   "整数"
   cp = c_p+prompt+c_n
   bp = ' '*len(prompt)
   print(cp+question)
   while True:
      answer = input(bp+'Please input an integer: ')
      if answer.isnumeric():
         z = int(answer)
         return z

#################
def IntRangeBox(question,zrange=[-2147483648,2147483647],prompt=''):
   "整数，在一定范围内"
   zmin, zmax = zrange
   cp = c_p+prompt+c_n
   bp = ' '*len(prompt)
   print(cp+question)
   while True:
      answer = input(bp+'Please input an integer in [%i,%i]: '%(zmin,zmax))
      if answer.isnumeric():
         z = int(answer)
         if zmin<=z<=zmax:
            return z

#################
def YesNo(question,prompt=''):
   "Y/N 是或非"
   while True:
      print(c_p+prompt+c_n,end='')
      answer = input(question+' (yes or no): ')
      if answer.lower() in {'yes','y'}:   return True
      if answer.lower() in {'no','n'}:    return False

#################
def YesNoDefault(question,prompt='',default=False):
   "Y/N 是或非, 可指定默认"
   if default: dftstr = ' (yes or no, ENTER=yes): '
   else:       dftstr = ' (yes or no, ENTER=no): '

   while True:
      print(c_p+prompt+c_n,end='')
      answer = input(question+dftstr)
      if answer.lower() in {'yes','y'}:   return True
      if answer.lower() in {'no','n'}:    return False
      if answer=='': return default

#################
def InputBox(question,prompt='',hint=''):
   "随意输入一个str with a question"
   "Potential improve: 是否加入换行选项？是否加入对str长度限制？"
   cp = c_p+prompt+c_n
   bp = ' '*len(prompt)
   print(cp+question)
   while True:
      answer = input(bp+hint)
      if len(answer)>0: return answer

#################
def InputBoxSimple(prompt='',hint=''):
   "随意输入一个str"
   cp = c_p+prompt+c_n
   while True:
      answer = input(cp+hint)
      if len(answer)>0: return answer

#################
def Separator(char='-',repeat=50):
   "行分割线"
   print(char*repeat)

#################
def Password1Box(question='Password: '):
   "输入1个password"
   while True:
      answer = gp.getpass(question)
      if len(answer)>0: return answer

#################
def Password2Box(question='Password: '):
   "输入2个password, 必须完全一样才行"
   while True:
      answer1 = gp.getpass('[1/2] '+question)
      answer2 = gp.getpass('[2/2] '+question)
      if len(answer1)>0 and (answer1==answer2):
         star = answer1[0]+'*'*(len(answer1)-2)+answer1[-1]
         print('OK, the password is [%s]'%star)
         return answer1
      else:
         print('Two passwords you input are NOT identical, please try again...')

#################
def PrintList(li,index=[],tag=[],prompt='',title=''):
   "打印一个列表（可指定index）"
   print(prompt+title)
   N = len(li)

   if tag==[] and N>0:
      tag = ['']*N
   try:
      tagmaxlen= max([len(i) for i in tag])
   except:
      tagmaxlen= 0

   if    index==[]:  # Numbered index
      Ndigit = len(str(N-1))
      indexfmt = '%'+str(Ndigit)+'i'
      for i in range(N):
         print((prompt+indexfmt+'  %s  %s')%(i,tag[i].center(tagmaxlen),str(li[i])))
   elif  len(li)==len(index):
      for i in range(N):
         print(prompt+str(index[i])+' = '+str(li[i]))
   else:
      print('The length of strlist and taglist are NOT identical!')

#################
def PrintMultilineText(text,indent='',rindent='',highlight=''):
   "打印一个多行文本（可带统一两端缩进与语法高亮）"
   newtext = ''.join([indent+line+rindent+'\n' for line in text.splitlines(False)])
   if highlight!='': newtext = newtext.replace(highlight,c_red+highlight+c_n)
   print(newtext)
   return newtext
