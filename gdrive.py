
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive as PDGoogleDrive

class GoogleDrive():
   
    def __init__(self):
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()

        self.drive = PDGoogleDrive(gauth)

    def get_file(self, id, base_path):

        file = self.drive.CreateFile({'id': id})
        file.FetchMetadata()
        
        filename = file["title"]
        
        path = base_path / filename

        file.GetContentFile(path)

        return path
