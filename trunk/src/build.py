from configobj import ConfigObj
import sys
import os

def makeServerIni():
    config = ConfigObj()
    config.filename = os.path.join(sys.path[0], 'servers.ini') 
    config['servers'] = {}
    config['servers']['0'] = {}
    config['servers']['0']['name'] = 'Demo Server'
    config['servers']['0']['ip_address'] = 'localhost'
    config['servers']['0']['port'] = '11211'
    config.write()
    
if __name__ == '__main__':
    makeServerIni()