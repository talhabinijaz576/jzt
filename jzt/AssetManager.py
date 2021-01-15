import requests
import datetime
import ast
import os


class AssetManager:
    
    url="https://commandcenter.jazeetech.com/getAsset/"
    token_file = str(os.path.join(os.getenv('PROGRAMDATA'), "jazee_orchestrator", "token.txt"))
    token = None
    access_key=None
    
    def __init__(self, access_key=None, token_file=None, url=""):
        
        if(access_key!=None):
            self.access_key = access_key
        if(token_file!=None):
            self.token_file = token_file
        if(len(url)!=0):
            self.url = url
         
        if(os.path.exists(self.token_file)):
            self.token = open(self.token_file, 'r').readlines()[0].strip()
        if(len(self.token)<10):
            self.token = None
            
        if(self.token==None and self.access_key==None):
            raise Exception("Please provide access key for unregistered device")
            
            
    def getAsset(self, name=""):

        if(self.access_key!=None):
            request_url = self.url+"?asset={0}&key={1}".format(name, self.access_key)
        elif(self.token!=None):
            request_url = self.url+"?asset={0}&token={1}".format(name, self.token)
        response = requests.get(request_url)
        if(response.status_code==200):
            response = response.content.decode('ascii')
            response = ast.literal_eval(response)

            success = response["success"]=="True"    
            if(success):
                try:
                    asset_type = response["type"]
                    if(asset_type == "text"):
                        text = response["text"]
                        return text
                        
                    elif(asset_type == "number"):
                        number = float(response["number"])
                        return number
                        
                    elif(asset_type == "credential"):
                        username = response["username"]
                        password = response["password"]
                        return (username, password)
                except Exception as e:
                    #print(e)
                    message = "Somthing went wrong"
                    raise Exception(message)
                    
            else:
                message = response["message"]
                raise Exception(message)
            
        else:
            message = "Connection could not be established. Please check your internet connection."
            raise Exception(message)
            
            
    





