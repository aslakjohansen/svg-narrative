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
    
    def hide (self, ids):
        for identifier in ids:
            e = self.root.find(id=identifier)
            
            # read
            style = e.attrs['style'].split(';')
            props = {}
            for i in range(len(style)):
                elements = style[i].split(':')
                if len(elements)!=2: continue
                props[elements[0]] = elements[1]
            
            # modify
            props['display'] = 'none'
            
            # write
            e.attrs['style'] = ';'.join(map(lambda k: '%s:%s'%(k, props[k]), props.keys()))
            
            print(e)
    
    def show (self, ids):
        pass
    
    def settext (self, identifier):
        pass

ids = {
    'tickbox1': 'path819',
    'tickbox2': 'path819-3',
    'tickbox3': 'path819-6',
    'tickbox1text': 'text844',
    'tickbox2text': 'text848',
    'tickbox3text': 'text852',
    'box': 'path817',
    'boxtext': 'flowRoot854',
}

m = Model("../var/test1.svg")
m.hide([ids['tickbox1']])
m.store("test1.svg")
