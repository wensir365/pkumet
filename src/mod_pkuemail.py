#!/usr/bin/env python3
#==================================
# E-mail Sender
# Xinyu Wen, Peking Univ, Jan 2018
#==================================

import smtplib
from email.mime.multipart  import MIMEMultipart
from email.mime.text       import MIMEText
from email.mime.base       import MIMEBase
from email import encoders

##################
class EmailSender:
   '''
	----------------------------------------------------------------------------------------------------

   ===============
   A) OOP 使用方法
   ===============

   from mod_pkuemail import EmailSender

   1. 初始化
   m = EmailSender()
   m = EmailSender('mail.163.com',25,'wensir365','wxy2k')

   2. 如果需要，加载配置文件里的SMTP设置
   m.LoadConfig('../cfg/pkumet.cfg')

   3. 准备Email内容
   m.SetupEmail('w@w.com','How are you','...email body string...',flist='readme.txt')
   m.SetupEmail(['w@w.com','y@y.com'],'How are you','...email body string...',flist=['1.txt','2.txt'])
   m.SetupEmail('w@w.com','How are you','...email body string...',BCC='secret@s.com')

   4. 发送
   m.Send()

   =================
   B) 命令行直接运行
   =================
   ./mod_pkuemail.py 回车
   之后按照提示输入内容即可

	----------------------------------------------------------------------------------------------------
   '''

   cfgfile  = '../cfg/pkumet.cfg'
   default  = {
      'server'    : 'mail.pku.edu.cn',
      'port'      : 25,
      'account'   : 'xwen@pku.edu.cn',
      'password'  : 'wenxinyu2018'
              }
   todict   = {  'me'  : 'wensir365@163.com',
              }

   def __init__(self,   server   = default['server'],
                        port     = default['port'],
                        account  = default['account'],
                        password = default['password'],
                        todict   = todict):
      self.SMTPserver   = server
      self.SMTPport     = port
      self.SMTPid       = account
      self.SMTPpw       = password
      self.TOdict       = todict

   def LoadConfig(self,fn=cfgfile):
      current  = {}
      f        = open(fn,'r')
      exec(f.read(),current)
      My       = current['MyPKUMET']
      del f,current

      self.SMTPserver   = My['SMTP_server']
      self.SMTPport     = My['SMTP_port']
      self.SMTPid       = My['SMTP_account']
      self.SMTPpw       = My['SMTP_password']
      self.TOdict       = My['TO_dict']

   def tofilter(self):
      for i in range(len(self.To)):
         if self.To[i] in self.TOdict.keys():
            self.To[i] = self.TOdict[self.To[i]]

   def SetupEmail(self,To,Subject,Body,flist=[],BCC=[]):
      self.From      = self.SMTPid
      self.To        = To
      self.BCC       = BCC
      self.Subject   = Subject
      self.Body      = Body
      self.AttachList= flist

      # Make sure they are list type
      if type(To)    is str: self.To         = [To]
      if type(BCC)   is str: self.BCC        = [BCC]
      if type(flist) is str: self.AttachList = [flist]

      # TO filter
      self.tofilter()
         
      # Plain text
      self.msg             = MIMEMultipart()
      self.msg['From']     = self.SMTPid
      self.msg['To']       = ";".join(self.To)
      self.msg['Subject']  = self.Subject
      self.msg.attach(MIMEText(self.Body, 'plain'))

      # Attachment, if any
      if len(self.AttachList)>0:
         for fn in self.AttachList:
            attachment  = open(fn, "rb")
            part  = MIMEBase('application', 'octet-stream')
            part.set_payload((attachment).read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', "attachment; filename= %s" % fn)
            self.msg.attach(part)

      # Finalized text, the one to go!
      self.FinalText = self.msg.as_string()

   def Send(self):
      self.server = smtplib.SMTP(self.SMTPserver, self.SMTPport)
      self.server.starttls()
      self.server.login(self.SMTPid,self.SMTPpw)

      # TO
      for to in self.To:
         try:
            self.server.sendmail(self.From, to, self.FinalText)
            print("Successfully send email to --->", to)
         except:
            print("Failed to send email to --->", to)

      # BCC
      if len(self.BCC)>0:
         for to in self.BCC:
            try:
               self.server.sendmail(self.From, to, self.FinalText)
               print("Successfully BCC email to --->", to)
            except:
               print("Failed to BCC email to --->", to)

      self.server.quit()


########################
if __name__=='__main__':
   print('===================================')
   print('     欢迎使用PKU/EmailSender       ')
   print('           June, 2018              ')
   print('         xwen@pku.edu.cn           ')
   print('-----------------------------------')
   print('* 用分号分隔邮件地址或附件文件     ')
   print('* 单独一行中输入EOF来结束正文的输入')
   print('===================================')

   TO    = input('To         : ')
   if TO=='me': TO=me
   TO    = TO.split(';')

   SUB   = input('Subject    : ')

   print(        'Body       :')
   print(        '---')
   TXT = ''
   while True:
      b = input()
      if b=='EOF':
         print('---')
         break
      else:
         TXT = TXT+b+'\n'

   ATT   = input('Attachment : ')
   ATT   = ATT.split(';')

   m = EmailSender()
   if len(ATT)==1 and ATT[0]=='':
      m.SetupEmail(TO,SUB,TXT)
   else:
      m.SetupEmail(TO,SUB,TXT,ATT)

   m.Send()
