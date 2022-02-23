import smtplib, ssl
from abc import ABCMeta, abstractmethod
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from email.utils import COMMASPACE, formatdate
from email.mime.application import MIMEApplication
from os.path import basename

def settypeConnection(email_secrets:dict):
    global secrets
    secrets = email_secrets

class IConex(metaclass=ABCMeta):

    # def getUrl():
    #     ""
    def getUser():
        ""
    def getPassword():
        ""
    def getOutput():
        ""
    def getMsg():
        ""

class EmailConex(IConex):

    def __init__(self):
        self.msg = MIMEMultipart()
        self.output = "smtp.office365.com"
        self.port = 587
        # self.username = "<>@pifpaf.com.br"
        # self.password = "#"
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

    # # Create a Secrets Manager client
    # session = boto3.session.Session()
    # client = session.client(
    #     service_name='secretsmanager',
    #     region_name=region_name
    # )

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
            
class ConexEmail():

    def getConex(email_secrets:dict):
        try:
            settypeConnection(email_secrets)
            return EmailConex()
        except AssertionError as _e:
            print(_e)