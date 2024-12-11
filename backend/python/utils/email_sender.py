
import smtplib
from email.mime.text import MIMEText
# from enoder import decode_string

# subject = "daily update"
# body = "This is your daily update"
# sender = "jem_022190@binalatongan.edu.ph"  
# recipients = ["jemcarlo46@gmail.com"", "recipient2@gmail.com"]



def my_send_email(subject, body, sender, recipients, password):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(sender, password)
       smtp_server.sendmail(sender, recipients, msg.as_string())
    print("Message sent!")



# subject = "daily update"
# body = "This is your daily update"
# sender = "jem_022190@binalatongan.edu.ph"  
# recipients = ["jemcarlo46@gmail.com", "recipient2@gmail.com"]

# try:
#    sender=decode_string("kfn`1332:1Acjobmbupohbo/fev/qi")
#    password = decode_string("t{ey!jcfi!uq{k!xnxq")
   
#    send_email(subject, body, sender, recipients, password)

#    print("Message sent!")
# except:
   # print("Failed to send email")
