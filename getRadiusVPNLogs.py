from datetime import datetime #imports libaries
import sys
import os, os.path
#import lxml shouldn't need this anymore
import smtplib
import platform
from email.mime.text import MIMEText


userFlag = '<User-Name data_type="1">'                                 #tag for username
userFlagEnd = '</User-Name>'
timeStampFlag = '<Timestamp data_type="4">'                            #tag for date/time
timeStampFlagEnd = '</Timestamp>'
IPFlag = '<Tunnel-Client-Endpt data_type="1">'                         #tag for connecting IP address
IPFlagEnd = '</Tunnel-Client-Endpt>'

users = ''
times = ''
IPs = ''

userhome = os.path.expanduser('~')
desktop = userhome + '\Desktop\\'


def readNewFile(path):                                                   #open latest log file
     fileName = path + "\\" + max(os.listdir(path))
     log = open(fileName, 'r') #opens the last file 
     print fileName + " determined to be latest file" #prints the last open file
     return log
     
def parseLog(log, users, times, IPs):                                    #parse out needed properties
     while True:
          line = log.readline()
          for item in line.split(userFlagEnd):                           # grab users
               if userFlag in item:               
                    #users += item [ item.find(userFlag)+len(userFlag) : ]
                     users += item [ item.find(userFlag)+len(userFlag) : ] + ","  #finds the username and the length
          for item in line.split(timeStampFlagEnd):
               if timeStampFlag in item:
                    #times += item [ item.find(timeStampFlag)+len(timeStampFlag) : ]
                    times += item [ item.find(timeStampFlag)+len(timeStampFlag) : ]+ "," #finds the time
          for item in line.split(IPFlagEnd):
               if IPFlag in item:
                    #IPs += item [ item.find(IPFlag)+len(IPFlag) : ]
                    IPs += item [ item.find(IPFlag)+len(IPFlag) : ]+ ","
               
          if line == '':
               log.close()
               print "User data captured"
               return users, times, IPs

def formatFile(users, times, IPs): #put everything in array
     usersL = users.split(',') #puts commas in between each user
     timesL = times.split(',')
     IPsL = IPs.split(',')     
     x=0
     newFile = open(desktop + 'temp_email.txt','w') #creates a temp file
     newFile.write("REPORT DATE: " + str(datetime.now())) #writes the current time in temp file
     newFile.write("=" * 100+"\n")
     while x < len(usersL):         
          newFile.write("\n" + usersL[x] + "\n " +timesL[x] + "\n" + IPsL[x]+"\n") 
          x+=1
     newFile.close()
     print "Formatting file for email..."

def sendEmail (desktop): #Creates and sends an email 
     print "Sending email"
     fp = open(desktop + 'temp_email.txt', 'rb')
     # Create a text/plain message
     msg = MIMEText(fp.read())
     fp.close()

     me = 'notifications@neurocogtrials.com'	 #receiver's email
     you = 'ryan.fitzpatrick@neurocogtrials.com' #your email          

     msg['Subject'] = 'VPN Usage For ' + str(datetime.now())
     msg['From'] = me
     msg['To'] = you

     # Send the message via our own SMTP server, but don't include the
     # envelope header.
     s = smtplib.SMTP('smtp.sendgrid.net', 25)				  #host and port number for smtp server
     s.login('<username goes here>', '<password goes here>')  #generalize this for credentials to any SMTP server
     s.sendmail(me, [you], msg.as_string())
     s.quit()
     print "SUCCESS!"
     
log = readNewFile("U:\RadiusLogs")
users, times, IPs = parseLog(log, users, times, IPs)
formatFile(users, times, IPs)
sendEmail(desktop)
os.remove(desktop + 'temp_email.txt')
raw_input()
sys.exit()

