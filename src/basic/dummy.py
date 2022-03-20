#-----------------------------------------------------------------------------------------------------
# dummy.py
#-----------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Dummy objects
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
OBJECT = lambda members: type('object', (object,), members)() #<---- create a dummy object on the fly (members is a dictionary)
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
class O:
    """ dummy object that mimics a dict """
    def __init__(self, **config_dict):
        for key, val in config_dict.items():
            if not (hasattr(self, key)):
                setattr(self, key, val) # dict[key] = getattr(self, key)
            else:
                print('Warning: cannot attribute with name [{}]! Skipping.'.format(key))
    def __bool__(self):
        return True if self.__dict__ else False
    def __len__(self):
        return len(self.__dict__)
    def __call__(self, key=None):
        if key:
            return key, self.__dict__[key]
        else:
            return self.__dict__.items()
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=



#-----------------------------------------------------------------------------------------------------
# Foot-Note:
""" NOTE:
    * Author:           Nelson.S
"""
#-----------------------------------------------------------------------------------------------------
