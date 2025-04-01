import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

class Gmailsend:
    def __init__(self,sender_mail:str,sender_token:str,sender_name:str):
        self.sender_mail=sender_mail
        self.sender_token=sender_token
        self.sender_name = sender_name

    def sending_email(self,subject:str,pdf_file_path:str,body:str,recipient_email:str, attachment_file_name:str)->str:  
        message = MIMEMultipart()
        message["From"] = f"{self.sender_name} <{self.sender_mail}>"
        message["To"] = recipient_email
        message["Subject"] =subject
        attachment_info= f"attachment; filename={attachment_file_name}"
        # Attach pdf file
        try:
                
            with open(pdf_file_path, "rb") as attachment:
                pdf_attachment = MIMEApplication(attachment.read(), _subtype="pdf")
                pdf_attachment.add_header("Content-Disposition", attachment_info)
                message.attach(pdf_attachment)
            message.attach(MIMEText(body, "plain"))      
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                op=server.login(self.sender_mail, self.sender_token)
                server.sendmail(self.sender_mail, recipient_email, message.as_string())
            return "Email sent successfully."
        except FileNotFoundError as error:
            return f"File not found error: {pdf_file_path} file not exists."    
        
        except Exception as err:
            return "This is error %s and email not sent to %s" % (str(err),str(recipient_email))
