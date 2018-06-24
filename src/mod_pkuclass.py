#!/usr/bin/env python3
#==================================
# Classes
# Xinyu Wen, Peking Univ, Jun 2018
#==================================

import   pandas         as pd
from     mod_pkuemail   import EmailSender

class Note:
   "Note类"
   Tag      = ''  #   Short string in safe mode   必须是一个安全字符集字符串
   Title    = ''  # * Long string                 可以有空格的任意字符串
   Text     = ''  # * Multi-line text
   Author   = ''  #   Name
   Email    = ''  #   Email to contact
   DTcreat  = ''  # * Date/Time for creating current object
   DTdue    = ''  #   Date/Time for closing  current object

   def __init__(self):
      "初始化Note的时间章"
      self.DTcreat   = pd.to_datetime('now')

   def Make(self, Title,Text,                   # <--- Must have
                  Tag='',Author='',Email='',    # <--- Optional
                  DTdue=''):                    # <--- Optional
      "通过调用函数构建Note"
      self.Tag       = Tag
      self.Title     = Title
      self.Text      = Text
      self.Author    = Author
      self.Email     = Email
      if DTdue!='':
         self.DTdue  = pd.to_datetime(DTdue)

   def MakeSP(self, Title,Text):                # <--- Must have
      "通过调用函数构建Note, 简版, 只需Title和Text"
      self.Title     = Title
      self.Text      = Text

   def Input(self):
      "通过屏幕输入Note"
      print('Please answer to build a note:')
      print('-----')
      self.Tag       = input('Tag     : ')
      self.Author    = input('Author  : ')
      self.Email     = input('Email   : ')
      self.DTdue     = pd.to_datetime(input('DTdue   : '))
      print('-----')
      self.Title     = input('Title   : ')
      print(                 'Text    : ')
      self.Text      = ''
      while True:
         line = input()
         if line=='EOF':   break
         if self.Text=='':
            self.Text = line
         else:
            self.Text = self.Text + '\n' + line
      print('-----')
      print('A note built.')

   def InputSP(self):
      "通过屏幕输入Note, 简版, 只需输入Title和Text"
      print('Please answer to build a note:')
      print('-----')
      self.Title     = input('Title   : ')
      print(                 'Text    : ')
      self.Text      = ''
      while True:
         line = input()
         if line=='EOF':   break
         self.Text = self.Text + line +'\n'
      print('-----')
      print('A note built.')

   def Print(self):
      "打印Note"
      print('Note:')
      print('-----')
      print('Tag     :',self.Tag)
      print('Author  :',self.Author)
      print('E-mail  :',self.Email)
      print('DTcreat :',self.DTcreat)
      print('DTdue   :',self.DTdue)
      print('-----')
      print('Title   :',self.Title)
      print('Text    :')
      if self.Text[-1]=='\n':
         print(self.Text,end='')
      else:
         print(self.Text)
      print('-----')

   def PrintSP(self):
      "打印Note, 简版, 只打印Title和Text"
      print('Note:')
      print('-----')
      print('Title   :',self.Title)
      print('Text    :')
      if self.Text[-1]=='\n':
         print(self.Text,end='')
      else:
         print(self.Text)
      print('-----')

   def Send(self):
      "把当前Note发送Email"
      if self.Email=='':
         print("Current self.Email is EMPTY! Please set it up before sending E-mail.")
         return False
      m = EmailSender()
      m.SetupEmail(self.Email,self.Title,self.Text)
      m.Send()
