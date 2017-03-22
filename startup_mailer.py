import subprocess
import smtplib
import socket
from email.mime.text import MIMEText
import time
import datetime

# Change to your own account information
to = ''

# Random email I created as the source
gmail_user = ''
gmail_password = ''

tries = 0

while True:
	if (tries > 60):
		exit()
	try:
		smtpserver = smtplib.SMTP('smtp.gmail.com', 587, timeout=30) # Server to use.
		break
	except Exception as e:
		tries = tries + 1
		time.sleep(1)

smtpserver.ehlo()
smtpserver.starttls()
smtpserver.ehlo

smtpserver.login(gmail_user, gmail_password)

today = datetime.date.today()

# Very Linux Specific
arg='ip route list'
p=subprocess.Popen(arg,shell=True,stdout=subprocess.PIPE)
data = p.communicate()
split_data = data[0].split()
ipaddr = split_data[split_data.index('src')+1]
my_ip = 'Your IP is %s' %  ipaddr

msg = MIMEText(my_ip)
msg['Subject'] = 'IP For RaspberryPi on %s' % today.strftime('%b %d %Y')
msg['From'] = gmail_user
msg['To'] = to

smtpserver.sendmail(gmail_user, [to], msg.as_string())

smtpserver.quit()
