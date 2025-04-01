import sys
class Fetchcontent:
    def __init__(self):
        pass
    def fetch_content_file(self,file_path:str)->str:
        try:    
            fo=open(file_path,"r")
            body_content=fo.read()
            fo.close() 
            return body_content
        except FileNotFoundError as err:
            print("File Not Found")
        return 
    
    def fetch_content_in_lines(self,file_path:str)->str:
        try:    
            fo=open(file_path,"r")
            temp_data=fo.readlines()
            fo.close()
            l_emails=[]
            for each in temp_data:
                temp1=each.rstrip(" ")
                temp2=temp1.lstrip(" ")
                temp3=temp2.strip("\n")
                l_emails.append(temp3)
            return l_emails
        except FileNotFoundError as err:
            print("File Not Found")
        return 
    

