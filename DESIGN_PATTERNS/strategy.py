from abc import ABC, abstractmethod

ALLOWED_EXENSIONS = ['html', 'pdf', 'json', 'xml', 'text']

class AbstractRenderer(ABC):
    @abstractmethod
    def render(self):
        pass

class HTMLRenderer(AbstractRenderer):
    def render(self):
        print("Rendering HTML File")

class PDFRenderer(AbstractRenderer):
    def render(self):
        print("Rendering PDF File")

class JsonRenderer(AbstractRenderer):
    def render(self):
        print("Rendering Json File")

class XMLRenderer(AbstractRenderer):
    def render(self):
        print("Rendering XML File")

class TXTRenderer(AbstractRenderer):
    def render(self):
        print("Rendering TXT File")

class FileHandler:
    def __init__(self, file_name):
        self.filename =file_name

    @classmethod
    def create(cls, filename):
        if filename.split('.')[-1] not in ALLOWED_EXENSIONS:
            print("File not allowed")
        return cls(filename)
    
    def render(self):
        dict = {
            'html' : HTMLRenderer,
            'pdf' : PDFRenderer,
            'json' : JsonRenderer,
            'xml' : XMLRenderer,
            'txt' : TXTRenderer
        }
        handler = dict[self.filename.split('.')[-1]]
        return handler().render()
    
f1 = FileHandler.create('my.pdf')
f1.render()