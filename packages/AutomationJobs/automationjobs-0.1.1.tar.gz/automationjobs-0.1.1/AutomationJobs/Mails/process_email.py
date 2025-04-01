from AutomationJobs.Mails.fetch_file_info import Fetchcontent
from AutomationJobs.Mails.sending_an_email import Gmailsend

class ProcessEmail:
    def __init__(self,sender_mail:str,sender_token:str,sender_name:str):
        self.file_content=Fetchcontent()
        self.gmail_send= Gmailsend(sender_mail=sender_mail,sender_token=sender_token,sender_name=sender_name)
    
    def processing_email_content(self,subject:str, file_content_path:str,recipient_emails_path:str, pdf_file_path:str,attachment_file_name:str):
        recipient_emails=self.file_content.fetch_content_in_lines(recipient_emails_path)
        file_content=self.file_content.fetch_content_file(file_content_path)
        print(f"recipient_emails:{recipient_emails}")
        for each_email in recipient_emails:
            print(self.gmail_send.sending_email(subject=subject,pdf_file_path=pdf_file_path,body=file_content,recipient_email=each_email,attachment_file_name=attachment_file_name))
            

        
        
    