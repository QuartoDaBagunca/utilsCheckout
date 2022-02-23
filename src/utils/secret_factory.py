import smtplib, ssl
from abc import ABCMeta, abstractmethod
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import COMMASPACE, formatdate
from email.mime.application import MIMEApplication
from os.path import basename
import json

def settypeConnection(new_secrets, IdSecret):
    global secrets
    secrets = json.loads(new_secrets.get_secret_value(
        SecretId=IdSecret)['SecretString'])

class IConex(metaclass=ABCMeta):

    def getUser():
        ""
    def getPassword():
        ""
class JDBCConex(IConex):

    def __init__(self):
        self.username = secrets["user"]
        self.password = secrets["password"]
        self.url = secrets["url"]
        self.database = secrets["database"]
        self.driver = secrets["driver"]
        self.port = secrets["port"]

    def getPort(self):
        return self.port

    def getUser(self):
        return self.username

    def getPassword(self):
        return self.password

    def getDriver(self):
        return self.driver
    
    def getDatabase(self):
        return self.database
    
    def getUrl(self):
        return self.url

    def getProperties(self):
        return {
                "user" : secrets['user'],
                "password" : secrets['password'],
                "driver" :  secrets["driver"]
                }

class EmailConex(IConex):

    def __init__(self):
        self.msg = MIMEMultipart()
        self.output = "smtp.office365.com"
        self.port = 587
        self.username = secrets["username"]
        self.password = secrets["password"]

    def getPort(self):
        return self.port

    def getUser(self):
        return self.username

    def getPassword(self):
        return self.password

    def getOutput(self):
        return self.output
    
    def getMsg(self):
        return self.msg    

    def envio_email(self, to_addrs, subject, text, cc=None):           
            self.msg['Subject'] = subject
            self.msg['From'] = self.username
            self.msg['To'] = to_addrs
            self.msg['Cc'] = cc
            self.msg['Date'] = formatdate(localtime=True)
            self.msg.attach(MIMEText(text))
            
            context = ssl.create_default_context()
            
            try:
                with smtplib.SMTP(self.output, self.port) as server:
                    server.ehlo()
                    server.starttls(context=context)
                    server.login(self.username, self.password)
                    if cc != None:
                        server.sendmail(self.msg['From'], cc.split(",") + [to_addrs], self.msg.as_string())
                    else:
                        server.sendmail(self.msg['From'], self.msg['To'], self.msg.as_string())
            except Exception as e:
                print(e)
                pass
            
class NewConex():

    def getConex(self, type_conex:str, secrets:dict, IdSecret:str):
        try:
            settypeConnection(secrets, IdSecret)
            if type_conex == 'email':
                return EmailConex()
            else:
                return JDBCConex()
        except AssertionError as _e:
            print(_e)