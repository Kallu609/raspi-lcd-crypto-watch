import json
import urllib2

def isFloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

def read_config():
    with open('config.json', 'r') as f:
        return json.loads(f.read())

def chunks(l, n):
    """Yield succesive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i + n]

def internet_on():
    try:
        urllib2.urlopen('http://216.58.192.142', timeout=3)
        return True

    except urllib2.URLError as err:
        return False

