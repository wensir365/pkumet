#!/usr/bin/env python3
#==================================
# Classes
# Xinyu Wen, Peking Univ, Jun 2018
#
# - Note
#==================================

import   copy
import   pandas         as pd
from     mod_pkuemail   import EmailSender

###########
class Note:
   "Note类"

   def __init__(self):
      "初始化"
      self.Tag     = ''  #   Short string in SAFE mode   必须是一个安全字符集字符串
      self.Title   = ''  # * Long string                 可以有空格的任意字符串
      self.Text    = ''  # * Multi-line text
      self.Author  = ''  #   Name
      self.Email   = ''  #   Email to contact
      self.DTcreat = ''  # * Date/Time for creating current object
      self.DTdue   = ''  #   Date/Time for closing  current object
      self.Marker  = ''  #   Reserved, for future use
      self.Comment = ''  #   Reserved, for future use

      # Timestamp for DTcreat
      self.DTcreat   = pd.Timestamp('now')

   def Renew(self):
      self.DTcreat   = pd.Timestamp('now')

   def RemoveDue(self):
      self.DTdue     = ''

   def Make(self, Title,Text,                            # <--- Must have
                  Tag='',Author='',Email='',DTdue=''):   # <--- Optional
      "通过调用函数构建Note"
      self.Title     = Title
      self.Text      = Text
      
      if Tag!='':    self.Tag    = Tag
      if Author!='': self.Author = Author
      if Email!='':  self.Email  = Email
      if DTdue!='':  self.DTdue  = pd.Timestamp(DTdue)

   def Input(self):
      "通过屏幕输入Note"
      print('Please answer some questions to creat a note:')
      print('-----')
      self.Tag       = input('Tag     : ')
      self.Author    = input('Author  : ')
      self.Email     = input('Email   : ')
      self.DTdue     = pd.Timestamp(input('DTdue   : '))
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
      print('Please answer some questions to creat a note:')
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

   def Print(self):
      "打印Note"
      #print('Note:')
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
   
   def PrintEmail(self):
      "生成Note的电子邮件文本"
      e  =   'Title   : '+self.Title
      e += '\nMailto  : '+', '.join(self.Email)
      e += '\nDTcreat : '+GetDateTime(self.DTcreat)
      e += '\nDTdue   : '+GetDateTime(self.DTdue)
      e += '\n'
      e += '\n---- Full Text ----\n'
      e += self.Text
      e += '\n-------------------\n'
      e += '\nYours,\nPKU-Met'
      return e

   def PrintSP(self):
      "打印Note, 简版, 只打印Title和Text"
      #print('Note:')
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
      mailsubject = '[PKU-Met/TodoList] '+self.Title
      m.SetupEmail(copy.deepcopy(self.Email),mailsubject,self.PrintEmail())
      m.Send()


##################
def GetDateTime(x):  # x - pd.Timestamp的时间章类型
   try:
      return x.strftime('%h%d/%a/%H:%M')
   except:
      # Demo 'Jun02/Th/13:30'
      return 'N/A'

##################
def SameNote(a,b):
   same = True
   if a.Tag       != b.Tag:      same = False
   if a.Title     != b.Title:    same = False
   if a.Text      != b.Text:     same = False
   if a.Author    != b.Author:   same = False
   if a.Email     != b.Email:    same = False
   if a.DTcreat   != b.DTcreat:  same = False
   if a.DTdue     != b.DTdue:    same = False
   if a.Marker    != b.Marker:   same = False
   if a.Comment   != b.Comment:  same = False
   return same
