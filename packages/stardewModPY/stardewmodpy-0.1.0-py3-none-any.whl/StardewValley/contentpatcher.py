from .manifest import Manifest


class ContentData:
    def __init__(self):
        self.Action = self.__class__.__name__
        self.json={
            "Action":self.Action
        }

class Include(ContentData):
    def __init__(self, FromFile:str):
        super().__init__()
        self.json["FromFile"]=FromFile

class Load(ContentData):
    def __init__(self, LogName:str, Target:str, FromFile:str):
        super().__init__()
        self.json["LogName"]=LogName
        self.json["Target"]=Target
        self.json["FromFile"]=FromFile

class EditData(ContentData):
    def __init__(self, LogName:str, Target:str, Fields:dict={}, Entries:dict={}):
        super().__init__()
        self.json["LogName"]=LogName
        self.json["Target"]=Target
        self.json["Fields"]=Fields
        self.json["Entries"]=Entries

class EditImage(ContentData):
    def __init__(self, LogName:str, FromFile:str, FromArea:dict, ToArea:dict):
        super().__init__()
        self.json["LogName"]=LogName
        self.json["FromFile"]=FromFile
        self.json["FromArea"]=FromArea
        self.json["ToArea"]=ToArea

class ContentPatcher:
    def __init__(self, manifest:Manifest):
        self.Manifest=manifest
        self.Manifest.ContentPackFor={
            "UniqueID": "Pathoschild.ContentPatcher"
        }

        self.contentFile={
            "Format": "2.5.0",
            "Changes": []
        }

        self.contentFiles={}
    
    def registryContentData(self, contentData:Load|EditData|EditImage, contentFile:str="content", newFile:bool=True):
        if contentFile=="content":
            self.contentFile["Changes"].append(contentData.json)
        else:
            if newFile:
                self.contentFiles[contentFile]={
                    "Changes":[

                    ]
                }
            self.contentFiles[contentFile]["Changes"].append(contentData.json)
    
    
    


class contentNewFile:
    def __init__(self):
        self.content={
            "Changes": []
        }

