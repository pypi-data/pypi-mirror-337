import sys
class Fetchcontent:
    def __init__(self):
        pass
    def fetch_the_files(self,file_path):
        try:    
            fo=open(file_path,"r")
            body_content=fo.read()
            fo.close() 
            return body_content
        except FileNotFoundError as err:
            return "File Not Found"

def main(file_path:str):
    fo=Fetchcontent()
    print(f"body content: {fo.fetch_the_files(file_path=file_path)}")

if __name__=="__main__":
    try:
        file_path=sys.argv[1]
        main(file_path=file_path)
    except IndexError:
        print("Please provide the arguments")
    
