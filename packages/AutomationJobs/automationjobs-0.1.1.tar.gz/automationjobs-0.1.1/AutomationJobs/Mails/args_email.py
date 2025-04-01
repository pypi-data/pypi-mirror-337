from AutomationJobs.Mails.process_email import ProcessEmail

import argparse

class ToShareMail:
    def __init__(self,sender_mail:str,sender_token:str,sender_name:str, subject:str, file_content_path:str,recipient_emails_path:str, pdf_file_path:str,attachment_file_name:str):
        self.sender_mail=sender_mail
        self.sender_token=sender_token
        self.sender_name=sender_name
        self.subject=subject
        self.file_content_path=file_content_path
        self.recipient_emails_path=recipient_emails_path
        self.pdf_file_path=pdf_file_path
        self.attachment_file_name=attachment_file_name
        self.process_email=ProcessEmail(sender_mail=sender_mail,sender_token=sender_token,sender_name=sender_name)
    
    def process(self):
        self.process_email.processing_email_content(subject=self.subject, file_content_path=self.file_content_path,recipient_emails_path=self.recipient_emails_path, pdf_file_path=self.pdf_file_path,attachment_file_name=self.attachment_file_name)

def run_process():
    # Set up argparse to handle command-line arguments
    parser = argparse.ArgumentParser(description="Send an email with a PDF attachment and content from a file.")
    
    # Add arguments for each parameter you want to pass through command-line
    parser.add_argument('--sender_mail', type=str, required=True, help="Sender's email address")
    parser.add_argument('--sender_token', type=str, required=True, help="Sender's email token")
    parser.add_argument('--sender_name', type=str, required=True, help="Sender's name")
    parser.add_argument('--subject', type=str, required=True, help="Subject of the email")
    parser.add_argument('--file_content_path', type=str, required=True, help="Path to the file containing the content of the email")
    parser.add_argument('--recipient_emails_path', type=str, required=True, help="Path to the file containing recipient email addresses")
    parser.add_argument('--pdf_file_path', type=str, required=True, help="Path to the PDF file")
    parser.add_argument('--attachment_file_name', type=str, required=True, help="Name of the attachment file")

    # Parse the arguments from the command line
    args = parser.parse_args()

    # Now use these arguments in your code
    s = ToShareMail(
        sender_mail=args.sender_mail,
        sender_token=args.sender_token,
        sender_name=args.sender_name,
        subject=args.subject,
        file_content_path=args.file_content_path,
        recipient_emails_path=args.recipient_emails_path,
        pdf_file_path=args.pdf_file_path,
        attachment_file_name=args.attachment_file_name
    )
    s.process()



