#-----------------------------------------------------------------------------------------------------
# fio.py
#-----------------------------------------------------------------------------------------------------

#------------------------------------
# iTOR
#------------------------------------
from .ds import iTOR
def SAVE_iTOR(path, data):
    itor = iTOR.create(path)
    itor.open('w')
    itor.write(*data)
    itor.close()
    return path
def LOAD_iTOR(path):
    itor = iTOR.create(path)
    itor.open('r')
    return list(itor.iterR())


#------------------------------------
# text
#------------------------------------
def SAVE_TEXT(path, data):
    with open(path, 'wt') as f:
        f.write(data)
    return path
def LOAD_TEXT(path):
    with open(path, 'rt') as f:
        data = f.read()
    return data
#------------------------------------


#------------------------------------
# json
#------------------------------------
import json
def SAVE_JSON(path, data):
    """ saves a dict to disk in json format """
    with open(path, 'w') as f:
        f.write(json.dumps(data, sort_keys=False, indent=4))
    return path
def LOAD_JSON(path):
    """ returns a dict from a json file """
    data = None
    with open(path, 'r') as f:
        data = json.loads(f.read())
    return data


#------------------------------------
# numpy
#------------------------------------
from numpy import load as LOAD_NP
from numpy import save as SAVE_NP



#------------------------------------
# images - plt.imread
#------------------------------------
from matplotlib.pyplot import imread as LOAD_IM
from matplotlib.pyplot import imsave as SAVE_IM



#------------------------------------
# fig - plt.fig
#------------------------------------
def SAVE_PLT(path, data):
    data.savefig(path)
    return path
def LOAD_PLT(path):
    return path



#------------------------------------
# types - use with fio.FORAGE( ... type_dict ... )
#------------------------------------
TYPE_DICT = {
    'text': (SAVE_TEXT, LOAD_TEXT),
    'json': (SAVE_JSON, LOAD_JSON),
    'np':   (SAVE_NP, LOAD_NP),
    'im':   (SAVE_IM, LOAD_IM),
    'plt':  (SAVE_PLT, LOAD_PLT),
    'itor': (SAVE_iTOR, LOAD_iTOR),
    }
#------------------------------------
