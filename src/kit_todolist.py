#!/usr/bin/env python3

import copy
import calendar
import pickle
import pandas     as pd
import mod_pkucli as cli
from   mod_color    import c_red,c_p,c_n
from   mod_pkuclass import Note,SameNote

prompt   = '    '

def go():
   print('Starting ... Toolkit/To-Do-List')

   TodoList_path  = '../cfg/'
   TodoList_file  = 'todolist.pkl'

   # INIT
   try:
      TodoList = pickle.load(open(TodoList_path+TodoList_file,'rb'))
      print('Loading ... todo-list data from '+TodoList_path+TodoList_file)
   except:
      TodoList = TODOLIST()
      print('Generating ... a new todo-list')

   TodoListBak = copy.deepcopy(TodoList)

   # MainLoop
   while True:
      TodoList.CheckAllExpire()  # Checking overdue records in each loop

      query = cli.RadioList(  title = '>>> To-Do List',
                              tag   = TodoList.listwDue(),
                              desc  = TodoList.listwTitle(),
                              fkey  = ['a','d','e','l','c','m','s','q'],
                              fdesc = ['Add ......... 增加一条新日程',
                                       'Delete ...... 完成日程后删除',
                                       'Edit ........ 修改日程',
                                       'List ........ 查看日程列表',
                                       'Calendar .... 查看年历',
                                       'Management .. 管理其它列表',
                                       'Save ........ 保存',
                                       'Quit ........ 退出'],
                              question='Which one you want to see the details?'  )

      if    query=='q':    # Quit (save)
         if not(SameTodoList(TodoListBak,TodoList)):
            if cli.YesNo('Save current To-do List?',prompt=prompt):
               pickle.dump(TodoList, open(TodoList_path+TodoList_file,'wb'))
               print(prompt+'OK! Saved.')
            print()
         return

      elif  query=='a':    # Add 1 item
         # -1- title
         print(prompt+'Adding a new item to current list ...')
         newjob   = input(prompt+'Step 1/4 - Job title: ')
         # -2- details
         newdet   = input(prompt+'Step 2/4 - Job details: ')
         if newdet=='EOF':
            newdet=''
            MultiLine=False
         else:
            MultiLine=True
         while MultiLine:
            line  = input(prompt+'                        ')
            if line=='EOF':   break
            newdet   = newdet + '\n' + line
         # -3- due date/time
         now      = pd.Timestamp('now')
         thismon  = calendar.month(now.year,now.month)
         cli.PrintMultilineText(thismon,indent=prompt,rindent=' ',highlight=' %2i '%now.day)
         newend   = input(prompt+'Step 3/4 - Expired date/time: ')
         if newend!='': newend=pd.Timestamp(newend)
         # -4- email
         newema   = input(prompt+'Step 4/4 - E-mail: ')
         if newema=='': newema = 'me'
         newema   = [ i.strip() for i in newema.split(',') ]

         newitem  = Note()
         newitem.Make(  Title=newjob, Text=newdet,
                        DTdue=newend, Email=newema   )
         print('\n'+prompt+'OK, I got all the information for the new item.')
         PrintItem(newitem)
         TodoList.Add(newitem)

      elif  query=='d':    # Delete 1 item
         ans = cli.IntRangeBox('Delete which one?',[0,TodoList.Nlistw()-1],prompt=prompt)
         TodoList.Finish(TodoList.listw[ans])

      elif  query=='e':    # Edit 1 item
         ans = cli.IntRangeBox('Edit which one?',[0,TodoList.Nlistw()-1],prompt=prompt)
         oldnote  = TodoList.listw[ans]
         newnote  = oldnote
         # -0- current one
         print(prompt+'Current Item:')
         PrintItem(oldnote)
         print(prompt+'Please input new text, or just type [Enter] to keep the old information:')
         # -1- title
         newjob   = input(prompt+'Step 1/4 - Job title: ')
         if newjob!='': newnote.Title = newjob
         # -2- details
         newdet   = input(prompt+'Step 2/4 - Job details: ')
         if newdet=='EOF':
            newdet=''
            MultiLine=False
         else:
            MultiLine=True
         while MultiLine:
            line  = input(prompt+'                        ')
            if line=='EOF':   break
            newdet   = newdet + '\n' + line
         if newdet!='': newnote.Text = newdet
         # -3- due date/time
         now      = pd.Timestamp('now')
         thismon  = calendar.month(now.year,now.month)
         cli.PrintMultilineText(thismon,indent=prompt,rindent=' ',highlight=' %2i '%now.day)
         newend   = input(prompt+'Step 3/4 - Expired date/time: ')
         if newend!='': newnote.DTdue = pd.Timestamp(newend)
         # -4- email
         newema   = input(prompt+'Step 4/4 - E-mail: ')
         if newema!='': newnote.Email = [ i.strip() for i in newema.split(',') ]
         # -5- update
         TodoList.Edit(oldnote,newnote)

      elif  query=='l':    # List all
         print(prompt+'List all ...')
      
      elif  query=='m':    # Management
         while True:
            query2   = cli.RadioList(  title = '>>> To-Do List >>> Management',
                                       fkey  = ['i','sw','sd','se','md','me','rw','rd','re','r','q'],
                                       fdesc = ['Information of 3 lists (Working, Deleted, Expired)',
                                                'Show Working list',
                                                'Show Deleted list',
                                                'Show Expired list',
                                                'Move an item from Deleted list back to working list',
                                                'Move an item from Expired list back to working list',
                                                'Reset Working list',
                                                'Reset Deleted list',
                                                'Reset Expired list',
                                                'Reset All',
                                                'Quit'],
                                       question='Which one you want to perform?'  )
            if query2=='q':      # Quit
               break

            elif  query2=='i':   # Information
               print(prompt+'Number of items in 3 lists:')
               print(prompt+'----')
               print(prompt+'Working List =', TodoList.Nlistw())
               print(prompt+'Deleted List =', TodoList.Nlistf())
               print(prompt+'Expired List =', TodoList.Nliste())

            elif  query2=='sw':  # Show Working list
               if TodoList.listwTitle()!=[]:
                  cli.PrintList( TodoList.listwTitle(),tag=TodoList.listwDue(),
                                 prompt=prompt,title='List of Working Jobs:'     )
               else:
                  print(prompt+'Empty! No Working records found!')

            elif  query2=='sd':  # Show Deleted list
               if TodoList.listfTitle()!=[]:
                  cli.PrintList( TodoList.listfTitle(),tag=TodoList.listfDue(),
                                 prompt=prompt,title='List of Deleted Jobs:'     )
               else:
                  print(prompt+'Empty! No DELETED records found!')

            elif  query2=='se':  # Show Expired list
               if TodoList.listeTitle()!=[]:
                  cli.PrintList( TodoList.listeTitle(),tag=TodoList.listeDue(),
                                 prompt=prompt,title='List of Expired Jobs:'     )
               else:
                  print(prompt+'Empty! No EXPIRED records found!')
            
            elif  query2=='md':  # Move an item from Deleted to Working
               if TodoList.listfTitle()!=[]:
                  which = cli.RadioList(
                     title = '>>> To-Do List >>> Management >>> Move an item from DELETED to WORKING',
                     tag   = TodoList.listfDue(),
                     desc  = TodoList.listfTitle(),
                     question = 'Move which one back to WORKING list?')
                  if which=='q': print(prompt+'Canceled.')
                  else:          TodoList.ActiveFromFinish(which)
               else:
                  print(prompt+'Empty! No DELETED records found!')

            elif  query2=='me':  # Move an item from Expired to Working
               if TodoList.listeTitle()!=[]:
                  which = cli.RadioList(
                     title = '>>> To-Do List >>> Management >>> Move an item from EXPIRED to WORKING',
                     tag   = TodoList.listeDue(),
                     desc  = TodoList.listeTitle(),
                     question = 'Move which one back to WORKING list?')
                  if which=='q': print(prompt+'Canceled.')
                  else:          TodoList.ActiveFromExpire(which)
               else:
                  print(prompt+'Empty! No EXPIRED records found!')

            elif  query2=='rw':  # Reset Working list
               if cli.YesNo(prompt+'Are you sure to reset WORKING LIST w/ %i records?'
                              %TodoList.Nlistw()):
                  TodoList.ResetW()
               else:
                  print(prompt+'Canceled, I did nothing.')

            elif  query2=='rd':  # Reset Deleted list
               if cli.YesNo(prompt+'Are you sure to reset DELETED LIST w/ %i records?'
                              %TodoList.Nlistf()):
                  TodoList.ResetF()
               else:
                  print(prompt+'Canceled, I did nothing.')

            elif  query2=='re':  # Reset Expired list
               if cli.YesNo(prompt+'Are you sure to reset EXPIRED LIST w/ %i records?'
                              %TodoList.Nliste()):
                  TodoList.ResetE()
               else:
                  print(prompt+'Canceled, I did nothing.')

            elif  query2=='r':  # Reset All
               if cli.YesNo(prompt+'Are you sure you want to reset ALL 3 LISTs?'):
                  TodoList.ResetAll()
               else:
                  print(prompt+'Canceled, I did nothing.')

      elif  query=='s':    # Save
         if not(SameTodoList(TodoListBak,TodoList)):
            pickle.dump(TodoList, open(TodoList_path+TodoList_file,'wb'))
            print(prompt+'OK! Saved.')
            TodoListBak = copy.deepcopy(TodoList)
         else:
            print(prompt+'No updates, NO NEED to save so far.')

      elif  query=='c':    # Calendar
         now      = pd.Timestamp('now')
         thismon  = calendar.prcal(now.year)

      else:                # Show details
         print(prompt+'ITEM #%i'%query)
         PrintItem(TodoList.listw[query])
         if cli.YesNoDefault('E-mail this message to your mailbox?',prompt=prompt,default=False):
            TodoList.listw[query].Send()
         #tmp = input(prompt+'Press [Enter] to continue ...')

def PrintItem(note):
   prompt = '    '
   print(prompt+'----')
   print(prompt+'Job title   :', note.Title)

   lines = note.Text.splitlines()
   print(prompt+'Job details :', lines[0])
   for i in lines[1:]:  print('                 ', i)

   print(prompt+'Created on  :', note.DTcreat)
   print(prompt+'Expired on  :', note.DTdue)
   print(prompt+'E-mail      :', note.Email)
   print(prompt+'----')

def GetDateTime(x):  # x - pd.Timestamp的时间章类型
   try:
      return x.strftime('%h%d/%a/%H:%M')
   except:
      # Demo 'Jun02/Th/13:30'
      return 'N/A'

class TODOLIST:
   prompt   = '    '
   def __init__(self):
      self.listw = []   # List of currently Working jobs
      self.listf = []   # List of Finished jobs
      self.liste = []   # List of Expired jobs

   def listwTitle(self):
      return [ i.Title for i in self.listw ]

   def listfTitle(self):
      return [ i.Title for i in self.listf ]

   def listeTitle(self):
      return [ i.Title for i in self.liste ]

   def Nlistw(self):
      return len(self.listw)

   def Nlistf(self):
      return len(self.listf)

   def Nliste(self):
      return len(self.liste)

   def listwDue(self):
      return [ GetDateTime(i.DTdue) for i in self.listw ]
      
   def listfDue(self):
      return [ GetDateTime(i.DTdue) for i in self.listf ]
      
   def listeDue(self):
      return [ GetDateTime(i.DTdue) for i in self.liste ]

   def Data(self):
      return ( self.listw,
               self.listf,
               self.liste  )

   def DataCopy(self):
      return ( copy.deepcopy(self.listw),
               copy.deepcopy(self.listf),
               copy.deepcopy(self.liste)  )

   def ResetAll(self):
      self.ResetW()
      self.ResetF()
      self.ResetE()
      print(prompt+'All 3 lists reset!')

   def ResetW(self):
      self.listw.clear()
      print(prompt+'List WORKING reset!')

   def ResetF(self):
      self.listf.clear()
      print(prompt+'List DELETED reset!')

   def ResetE(self):
      self.liste.clear()
      print(prompt+'List EXPIRED reset!')

   def Add(self,newnote):
      self.listw.append(newnote)

   def Edit(self,note1,note2):
      which = self.listw.index(note1)
      self.listw[which] = note2
      print(prompt+c_red+note2.Title+c_n,'was UPDATED.')
      PrintItem(note2)

   def Finish(self,anote):
      self.listf.append(anote)
      self.listw.remove(anote)
      print(prompt+c_red+anote.Title+c_n,'was DELETED.')
      PrintItem(anote)

   def Expire(self,anote):
      self.liste.append(anote)
      self.listw.remove(anote)

      print()
      print(prompt+c_red+'WARNING!! OVERDUE JOB FOUND!!'+c_n)
      print(prompt+c_red+anote.Title+c_n,'was EXPIRED, Due on',anote.DTdue)
      PrintItem(anote)

   def CheckAllExpire(self):
      now   = pd.Timestamp('now')
      overduelist = []
      for tmp in self.listw:
         if tmp.DTdue!='' and tmp.DTdue < now:  # an overdue note found!
            overduelist.append(tmp)
      for tmp in overduelist:
         self.Expire(tmp)

   def ActiveFromFinish(self,i):
      tmp   = self.listf[i]
      self.listf.remove(self.listf[i])

      tmp.Renew()
      tmp.RemoveDue()
      print(prompt+c_red+tmp.Title+c_n,'was re-activated.')
      self.Add(tmp)

   def ActiveFromExpire(self,i):
      tmp   = self.liste[i]
      self.liste.remove(self.liste[i])

      tmp.Renew()
      tmp.RemoveDue()
      print(prompt+c_red+tmp.Title+c_n,'was re-activated.')
      self.Add(tmp)

def SameTodoList(a,b):
   same = True
   if len(a.listw)!=len(b.listw):   same = False
   if len(a.listf)!=len(b.listf):   same = False
   if len(a.liste)!=len(b.liste):   same = False
   if same:
      for i in range(a.Nlistw()):
         if not(SameNote(a.listw[i],b.listw[i])):  same = False
      for i in range(a.Nlistf()):
         if not(SameNote(a.listf[i],b.listf[i])):  same = False
      for i in range(a.Nliste()):
         if not(SameNote(a.liste[i],b.liste[i])):  same = False
   return same
   
