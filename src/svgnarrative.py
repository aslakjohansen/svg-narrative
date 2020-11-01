from bs4 import BeautifulSoup

def set_style_attr (e, key, value):
    if not 'style' in e.attrs: e.attrs['style'] = ''
    
    # read
    style = e.attrs['style'].split(';')
    props = {}
    for i in range(len(style)):
        elements = style[i].split(':')
        if len(elements)!=2: continue
        props[elements[0]] = elements[1]
    
    # modify
    if value==None:
        if key in props: del props[key]
    else:
        props[key] = value
    
    # write
    e.attrs['style'] = ';'.join(map(lambda k: '%s:%s'%(k, props[k]), props.keys()))

def set_stroke_color (e, color):
    if e.name=='g':
        for child in e.children:
            if child!=None:
                set_stroke_color(child, color)
    elif e.name in ['path', 'rect', 'text', 'ellipse']:
        set_style_attr(e, 'stroke', color)
    else:
        print('Warning: Don\'t know how to set stroke color for tag type "%s"' % e.name)

def set_end_marker (e, marker):
    set_style_attr(e, 'marker-end', marker)

def set_fill_color (e, color):
    set_style_attr(e, 'fill', color)

def set_display (e, display):
    set_style_attr(e, 'display', display)

def highlight (e, color):
    if e.name=='path':
        set_stroke_color(e, color)
    elif e.name=='rect':
        set_stroke_color(e, color)
    elif e.name=='text':
        set_fill_color(e, color)
    elif e.name=='g':
        for child in e.children:
            highlight(child, color)
    else:
        print('Error: Don\'t know how to highlight "%s". Skipping ...' % e.name)

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
            values = idmap[key]
            if type(values)!=list:
                values = [values]
            for value in values:
                e = self.root.find(id=value)
                if not silent: print('Value "%s" of key "%s"%s found'%(value, key, " not" if e==None else ""))
                if e==None: result = False
        
        return result
    
    def fill (self, ids, color):
        if type(ids)==str:
            ids = [ids]
        for identifier in ids:
            e = self.root.find(id=identifier)
            set_fill_color(e, color)
    
    def stroke (self, ids, color):
        if type(ids)==str:
            ids = [ids]
        for identifier in ids:
            e = self.root.find(id=identifier)
            set_stroke_color(e, color)
    
    def highlight (self, ids, highlight_color):
        if type(ids)==str:
            ids = [ids]
        for identifier in ids:
            e = self.root.find(id=identifier)
            highlight(e, highlight_color)
    
    def lowlight (self, ids):
        pass
    
    def set_end_marker (self, ids, marker):
        if type(ids)==str:
            ids = [ids]
        for identifier in ids:
            e = self.root.find(id=identifier)
            set_end_marker(e, marker)

if __name__ == "__main__":
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
