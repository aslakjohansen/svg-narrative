from bs4 import BeautifulSoup

def set_display (e, display):
    # read
    style = e.attrs['style'].split(';')
    props = {}
    for i in range(len(style)):
        elements = style[i].split(':')
        if len(elements)!=2: continue
        props[elements[0]] = elements[1]
    
    # modify
    props['display'] = display
    
    # write
    e.attrs['style'] = ';'.join(map(lambda k: '%s:%s'%(k, props[k]), props.keys()))

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
        if type(ids)==str:
            ids = [ids]
        for identifier in ids:
            e = self.root.find(id=identifier)
            set_display(e, 'none')
    
    def show (self, ids):
        if type(ids)==str:
            ids = [ids]
        for identifier in ids:
            e = self.root.find(id=identifier)
            set_display(e, 'display')
    
    def set_text (self, identifier, text):
        e = self.root.find(id=identifier)
        e.string.replace_with(text)
    
    def check_ids (self, idmap, silent=False):
        result = True
        
        for key in idmap:
            value = idmap[key]
            e = self.root.find(id=value)
            if not silent: print('Value "%s" of key "%s"%s found'%(value, key, " not" if e==None else ""))
            if key==None: result = False
        
        return result

ids = {
    'tickbox1': 'path819',
    'tickbox2': 'path819-3',
    'tickbox3': 'path819-6',
    'tickbox2text': 'tspan846',
    'tickbox2text': 'text848',
    'tickbox3text': 'tspan850',
    'box': 'path817',
    'boxtext': 'flowPara860',
}

m = Model("../var/test1.svg")
m.check_ids(ids)
m.hide(ids['tickbox1'])
m.store("test1.svg")
m.show([ids['tickbox1']])
m.store("test2.svg")
m.set_text(ids['tickbox2text'], "Red")
m.set_text(ids['boxtext'], "Once upon a time in a land far far away ...")
m.store("test3.svg")
