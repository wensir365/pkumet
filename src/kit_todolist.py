#!/usr/bin/env python3

import pickle
import mod_cli          as cli
from mod_color          import *

def go():
   print('Starting ... Toolkit/To-Do-List')

   ToDoList_file  = '../cfg/todolist.pkl'
   try:
      ToDoList = pickle.load(open(ToDoList_file,'rb'))
      print('Loading ... old to-do-list data')
   except:
      ToDoList = reset_todolist()
      print('Generating ... new to-do-list data')

   OldToDoList = ToDoList.copy()

   while True:
      ToDoScr = cli.selector( '>>> To-Do-List', ToDoList,
                              'Which one you want to remove?',
                              'Input the number of an item to be removed.' )
      query = ToDoScr.show_and_get()

      if    query==0:
         show_update(ToDoList,OldToDoList,start=3)
         if cli.yesno('Save current To-Do-List?'):
            pickle.dump(ToDoList, open(ToDoList_file,'wb'))
            print('OK! Saved.')
         print('')
         break

      elif  query==1:   # Append 1 item
         qa = cli.q_and_a('Description for a new item?')
         newjob   = qa.show_and_get()
         ToDoList.append(newjob)

      elif  query==2:   # Clean ALL
         if cli.yesno('Are you sure you want to CLEAN ALL items?'):
            ToDoList = reset_todolist()
         else:
            print('Canceled, I did nothing.')
            
      else:             # remove item
         print('%i. %s finished, removed.'%(query,c_red+ToDoList[query]+c_n))
         del ToDoList[query]
         print('')
   return

def reset_todolist():
   todolist = [   c_p+'Quit'+c_n,
                  c_p+'Append 1 item'+c_n,
                  c_p+'Clean ALL'+c_n       ]
   return todolist

def show_update(list1,list0,start=0):
   print('\nCurrent List (* for new items):\n')
   for i in range(start,len(list1)):
      if list1[i] in list0:   # old
         print('%4i. %s'%(i,list1[i]))
      else:
         print('%1s%3i. %s'%('*',i,list1[i]))
   print('')
