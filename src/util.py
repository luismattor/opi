
def toint(s, default = 0):
    try:
        o = int(s)
    except:
        #print 'Error when parsing %s' % s
        o = default
    return o

def tofloat(s):
    try:
        o = float(s)
    except:
        #print 'Error when parsing %s' % s
        o = None
    return o

def fix_hour_padding(s):
    if s.index(':') == 1:
        s = '0' + s
    return s

def fix_ms(s):
    if '.' in s:
        index = s.index('.')
        s = s[:index]
    return s
