
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
