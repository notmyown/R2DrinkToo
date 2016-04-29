import platform

TRACE = 0
DEBUG = 1
INFO = 2
WARN = 3
ERROR = 4
OFF = 10

defaultLevel = OFF

def toString(obj):
    if platform.system() != "Windows":
        return str(obj)
    else:
        return str(obj)
        #return unicode(obj) //TODO Wechsel zu unicode in p2
    
def log(level, obj):
    if level >= defaultLevel:
        print(toString(obj))

def debug(obj):
    log(DEBUG, obj)

def info(obj):
    log(INFO, obj)

def warn(obj):
    log(WARN, obj)

def error(obj):
    log(ERROR, obj)

def trace(obj):
    log(TRACE, obj)