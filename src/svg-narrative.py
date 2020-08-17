from bs4 import BeautifulSoup

class Model:
    def __init__ (self, filename: str):
        self.filename = filename
        with open(filename) as fo:
            self.root = BeautifulSoup(''.join(fo.readlines()), features = 'xml')
    
    def store (self, filename):
        lines = [str(self.root)]
        with open(filename, 'w') as fo:
            fo.writelines(lines)
    

m = Model("../var/test1.svg")
m.store("test1.svg")

