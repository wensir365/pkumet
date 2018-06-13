#!/usr/bin/env python3

import calendar
import pickle
import pandas     as pd
import mod_cli    as cli
from   mod_color  import c_red,c_p,c_n

def go():
   print('Starting ... Toolkit/To-Do-List')

   TodoList_file  = '../cfg/todolist.pkl'
   try:
      TodoList = pickle.load(open(TodoList_file,'rb'))
      print(TodoList)
      print('Loading ... old to-do-list data')
   except:
      TodoList = reset_todolist()
      print('Generating ... new to-do-list data')

   while True:
      TodoScr = todo_selector( header   = '>>> To-Do-List',
                              itemlist = TodoList,
                              fkeydict = {   'q' : 'Quit',
                                             'a' : 'Add 1 item',
                                             'r' : 'Reset all',
                                             'd' : 'Delete 1 item',
                                             's' : 'Show all'        },
                              question = 'Which one you want to see the details?'   )
      query = TodoScr.show_and_get()

      if    query=='q':    # Quit (save)
         TodoScr.show()
         if cli.YesNo('Save current To-do List?'):
            for i in range(len(TodoList)):
               if TodoList.at[i,'status']=='N':
                  TodoList.at[i,'status'] = ''
            pickle.dump(TodoList, open(TodoList_file,'wb'))
            print('OK! Saved.')
         print('')
         return

      elif  query=='a':    # Add 1 item
         now = pd.to_datetime('now')

         newjob   = cli.InputBox('Adding a new item to current list ...',
                                       '    ','Step 1/4 - Job title: ' )
         newdet   = cli.InputBoxSimple('    ','Step 2/4 - Job details: ' )
         thismon  = calendar.month(now.year,now.month)
         cli.PrintMultilineText(thismon,indent='    ',rindent=' ',highlight=' %2i '%now.day)
         newend   = cli.InputBoxSimple('    ','Step 3/4 - Expired date/time: ' )
         newema   = cli.InputBoxSimple('    ','Step 4/4 - E-mail: ' )

         newitemlist = [newjob, newdet, 'N', now, pd.to_datetime(newend), newema]
         newitemname = ['job',  'details', 'status', 'start', 'end', 'email']

         newitem  = pd.DataFrame( [newitemlist], columns=newitemname )
         TodoList.index = TodoList.index+1
         TodoList = newitem.append(TodoList)

         cli.PrintList( newitemlist, index=newitemname, prompt='    ',
                        title='OK, I got the information from you for the new item:')

      elif  query=='r':    # Reset All
         if cli.YesNo('Are you sure you want to reset the list?'):
            TodoList = reset_todolist()
         else:
            print('Canceled, I did nothing.')

      elif  query=='d':    # Delete 1 item
         ans = cli.IntBox('Delete which one?',prompt='    ')
         TodoList.at[ans,'status'] = 'D'
         print('    OK, %s deleted.'%(c_red+str(ans)+' '+TodoList['job'][ans]+c_n))

      elif  query=='s':    # Show all
         print('Restart and show all ...')
            
      else:                # Show details
         print('    ----')
         print('    ITEM #%i'%query)
         print('    ----')
         print('    Job title   :', TodoList['job'][query])
         print('    Job details :', TodoList['details'][query])
         print('    Expired on  :', TodoList['end'][query])
         print('    Created on  :', TodoList['start'][query])
         print('    E-mail      :', TodoList['email'][query])
         print('    ----')


class todo_selector():

   def __init__(  self,itemlist,
                  header='',
                  fkeydict={'q':'Quit'},
                  question='Which item you prefer?',
                  hint='Please input a number or q (for quit)'):
      self.header = header
      self.item   = itemlist
      self.fkey   = fkeydict
      self.ques   = question
      self.hint   = hint
      self.N      = len(itemlist)
      self.Nfkey  = len(fkeydict)
      self.anslist_item = [ str(i) for i in range(self.N) ]
      self.anslist_fkey = list(fkeydict.keys())

   def show(self):
      print('\n'+self.header+'\n')
      for i in range(self.N):
         tmp = self.item.loc[i]
         print('%5i %1s %-11s %s'%(i, tmp.status, GetDateTime(tmp.end), tmp.job))
      print('')

   def show_and_get(self):
      print('\n'+self.header+'\n')
      for i in range(self.N):
         tmp = self.item.loc[i]
         if tmp.status=='D' or tmp.status=='E':
            continue
         else:
            print('%5i %1s %-11s %s'%(i, tmp.status, GetDateTime(tmp.end), tmp.job))
      for i in self.fkey:
         print((c_p+'%5s'+c_n+' %1s %-11s %s')%(i,'','',self.fkey[i]))
      print('')
      print(c_p+'[Q] '+c_n+self.ques)
      while True: 
         answer = input(c_p+'[A] '+c_n)
         if    answer in self.anslist_item:
            return int(answer)
         elif  answer in self.anslist_fkey:
            return answer
         elif  answer=='999':  self.show()
         else:
            if len(answer)>0:
               print('Sorry, '+c_red+answer+c_n+' is an invalid input.')
               print(c_p+'[H] '+c_n+self.hint)
               print('')


def reset_todolist():
   TodoList = pd.DataFrame(columns=('job','details','status','start','end','mailto'))
   TodoList = TodoList.append(
               {  'job'       : 'Hello! A new to-do list is ready for YOU!',
                  'details'   : 'You may Add/Delete/Edit/Reset the list anytime',
                  'status'    : 'N',   # 'N'=New, 'D'=Deleted, 'E'=Expired, ''=Normal
                  'start'     : pd.to_datetime('now'),
                  'end'       : '',
                  'mailto'    : '' }, ignore_index=True)
   return TodoList

def GetDateTime(x):
   try:
      return x.strftime('[%h%d/%Hh]')
   except:
      return '[unlimited]'

