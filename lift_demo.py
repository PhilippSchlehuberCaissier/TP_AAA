from IPython.display import SVG
import re, os, hashlib
from spot.impl import twa_run
from spot.aux import str_to_svg

def floor(y, lvl, var):
    r = var['req'][lvl]
    here = var['p']==lvl
    cabin = var['cabin']
    t = var['t']
    f = '<rect y="{0}" width="40" height="30" fill="#ff{1}" stroke="black"/>'.format(y, '4' if here else 'e')
    if lvl == t:
        f += '<rect x="3" y="{0}" width="34" height="4" fill="#0a0" />'.format(y + 3)
    if here and cabin==2:
        door = '''
<rect x="5" y="{0}" width="20" height="20" fill="#aeb" stroke="#444" />
<line x1="12" y1="{2}" x2="12" y2="{0}" stroke="#444" />
<polygon points="5,{1} 12,{2} 25,{2} 25,{1}" fill="#fff" stroke="#444" />'''.format(y+9, y+29, y+25)
    else:
        door = '''
<rect x="5" y="{0}" width="10" height="20" fill="#eee" stroke="#444" />
<rect x="15" y="{0}" width="10" height="20" fill="#eee" stroke="#444" />'''.format(y+9)
    but = '<circle cx="33" cy="{0}" r="3" fill="#{1}00" />'.format(y+20, 'f' if r else '0')
    return f + door + but

def decode(s):
    var = { 'req': [0,0,0,0] }
    exec(s.replace(',', ';').replace('.', '_'), var)
    return ('<svg width="40" height="120" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">\n' +
            floor(90, 0, var) +
            floor(60, 1, var) +
            floor(30, 2, var) +
            floor(0, 3, var) + "</svg>")

def fix_graph(txt):
    if not os.access('cache', os.F_OK):
        os.mkdir('cache', 0o755)
    match = re.compile(r'\[label=[<"]req.*[">]\]')
    items = re.findall(match, txt)
    for item in items:
        s = item[8:]
        s = re.sub('<br/>.*', '', s)
        s = re.sub('\\\\n.*', '', s)
        svg = '<?xml version="1.0" encoding="utf-8"?>\n' + decode(s)
        encoded = svg.encode('utf-8')
        namesvg = 'cache/' + hashlib.sha1(encoded).hexdigest() + '.svg'
        with open(namesvg, "wb", 0) as out:
            out.write(encoded)
        txt = txt.replace(item, '[image="' + namesvg + '", width="0.6", height="1.7", tooltip=<' + s + '>]')
    txt = txt.replace('node [style="filled,rounded", fillcolor="#ffffaa"]', 'node [shape=none, label=""]')
    return SVG(str_to_svg(txt.encode('utf-8')))

def lift_display(k, arg=None):
    if k is None:
        return "OK"
    if type(k) == twa_run:
        k = k.as_twa(True)
    if arg is None:
        return fix_graph(k.to_str('dot', '.Ak'))
    else:
        return fix_graph(k.to_str('dot', '.Akv<' + str(arg)))
