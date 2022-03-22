#-----------------------------------------------------------------------------------------------------
# ds.py
#-----------------------------------------------------------------------------------------------------
import os, json
GLOBAL_CTRL_CHAR = {

    'SOH'   : 1,    # start of header
    'STX'   : 2,    # start of text
    'ETX'   : 3,    # end of text
    'EOT'   : 4,    # end of transmission
    'ETB'   : 23,   # end of transmission block
    'EOM'   : 25,   # end of medium

    'DLE'   : 16,
    'DC1'   : 17,
    'DC2'   : 18,
    'DC3'   : 19,
    'DC4'   : 20,

    'FS'   : 28,
    'GS'   : 29,
    'RS'   : 30,    # Record Seperator      
    'US'   : 31,    # Unit Seperator        

    'ENQ'   : 5,
    'ACK'   : 6,
    'NAK'   : 21,
    'BEL'   : 7,
    'CAN'   : 24,
    'SYN'   : 22,
    'SUB'   : 26,
    'ESC'   : 27,
    'SI'   : 14,
    'SO'   : 15,
}
#-----------------------------------------------------------------------------------------------------



#------------------------------------
# indexed table of records - iTOR data structure
#------------------------------------
class iTOR:
    """ (i)ndexed (T)able (O)f (R)ecords 
    
        its just a,         list of(    records of(     units   )))
        which basically,    list of(    list of(        strings )))
        an iTOR is represented using 2 files - data file and index file
    """
    #<< class variables
    GLOBAL_US =     GLOBAL_CTRL_CHAR['US']
    GLOBAL_RS =     GLOBAL_CTRL_CHAR['RS']
    def create(path, index_ext='.index'):
        """
        creates a new STORAGE with root dir at 'root' where 'storage' is the name of storage configuration file
        * prefered method of creating new storage from scratch
        """
        return iTOR(path, os.path.join(os.path.dirname(path), os.path.basename(path) + index_ext) )


    #<< dunder methods      ----------------------------------------------------------
    def __init__(self, data_file_path, index_file_path) -> None:
        #assert(index.lower.endswith('.npy'))
        self.path= data_file_path
        self.index = index_file_path
        self.US = bytes([int(self.GLOBAL_US)]) # unit seperator
        self.RS = bytes([int(self.GLOBAL_RS)]) # record seperator
        self.mode = '' #<-- is closed
    def __iter__(self):
        return self.iterR()
    def __len__(self):
        return self.len()


    #<< open method
    def _iopen(self):
        with open(self.index, 'rt', encoding='utf-8', newline='\n') as f:
            res = [ ([ int(y) for y in x[0:-1].split(' ')]  if len(x)>1 else [])  for x in f.readlines() ]
        return res
    def _openi(self):
        if self.mode!='w':
            try:
                i = self._iopen()
                self.i = i if i else []
            except FileNotFoundError:
                self.i = []
        else:
            self.i = []
        self.i.append([(self.i[-1][-1]+1) if self.i else 0])
    def open(self, mode='w'): 
        """ opens the list for appending, mode should be either w/a """
        if not self.mode:
            self.mode=mode
            self.f = open(self.path, mode=self.mode+'b')
            self._openi()
        else:
            print('! Already open in [{}] mode !'.format(self.mode))


    #<< close method        ----------------------------------------------------------
    def _iclose(self):
        with open(self.index, 'wt', encoding='utf-8', newline='\n') as f:
            for i in self.i:
                f.write( ' '.join([ str(d) for d in i ]) + '\n' )
            del self.i
        return self.index
    def _closei(self):
        #assert(not self.i.pop()) #<----- means that some row might be open.... close it?
        lR = self.i.pop()
        if len(lR)>1:
            print('! Last Record was not closed - ignoring data: [{}] !'.format(lR))
        self._iclose()
    def close(self):
        """ closes the list, should be called to free resources """
        if self.mode:
            self.f.close()
            self._closei()
            self.mode=''
        else:
            print('! Already closed !')


    #<< write method        ----------------------------------------------------------
    def _uwrite(self, *units):
        for unit in units:
            self.f.write(str(unit).encode('utf-8'))
            self.f.write(self.US)
            self.i[-1].append( self.f.tell() )
    def _uclose(self):
        self.f.write(self.RS)
        self.i.append([self.f.tell()])
    def write(self, *rows): # rows are records
        """ args = multiple rows, writes multiple rows at once
                assumes that each item in args is a row itself - row should be iterable """
        for row in rows:
            self.writeR(*row)
    def writeR(self, *units):
        """ args = multiple units in a row, writes one full row at once
                assumes that each item in arg is a item(unit) in this row """
        self._uwrite(*units)
        self._uclose()
    def writeU(self, *units, close=False):
        """ args = multiple cells in a row, 
                assumes that each item in arg is a item(cell) in this row """
        self._uwrite(*units)
        self._uclose() if close else None
        

    #<< read method     ----------------------------------------------------------
    def readU(self, row, unit):
        a, b = self.i[row][unit], self.i[row][unit+1]
        self.f.seek(a)
        return self.f.read(b - a - 1).decode('utf-8')
    def readR(self, row):
        a, b = self.i[row][0], self.i[row][-1]
        self.f.seek(a)
        return [ d.decode('utf-8') for d in self.f.read(b - a - 1).split(self.US) ]
    def read(self, *rows):
        return [ self.readR(row) for row in rows ]
    def readA(self):
        return self.read(*range(len(self)))
    

    #<< generator method ----------------------------------------------------------
    def iterU(self):
        if not self.mode:
            self.open('r')
        else:
            if self.mode!='r':
                raise Exception('! Already open in [{}] mode - close it first!'.format(self.mode))
        ptr = 0
        self.f.seek(ptr)
        temp= self.i.pop()
        for ii in self.i:
            assert(ptr==ii[0]) #<---- indicates errors in file
            for index in ii[1:]:
                i =  index - ptr - 1
                buffer = self.f.read(i)
                _ = self.f.read(1)
                ptr += (i +1)
                yield buffer.decode('utf-8')
            _ = self.f.read(1)
            ptr += 1
            yield None #<--- None to mark end of row
        del ptr #<-- clean up
        self.i.append(temp)
        self.close()
    def iterR(self):
        if not self.mode:
            self.open('r')
        else:
            if self.mode!='r':
                raise Exception('! Already open in [{}] mode - close it first!'.format(self.mode))
        ptr = 0
        self.f.seek(ptr)
        temp= self.i.pop()
        for ii in self.i:
            assert(ptr==ii[0]) #<---- indicates errors in file
            row = []
            for index in ii[1:]:
                i =  index - ptr - 1
                buffer = self.f.read(i)
                _ = self.f.read(1)
                ptr += (i +1)
                row.append(buffer.decode('utf-8'))
            _ = self.f.read(1)
            ptr += 1
            yield row #<--- None to mark end of row
        del ptr #<-- clean up
        self.i.append(temp)
        self.close()


    #<< info method     ----------------------------------------------------------
    def len(self):
        return len(self.i)-1 if self.mode else 0
    def count(self, i):
        return len(self.i[i])-1 if self.mode else -1
    def info(self, p=print):
        m,l = self.mode, self.len()
        p('Mode[{}]/Len:[{}]'.format(m,l))
        if m:
            p('Count:')
            for i in range(l):
                p('\t_{}_\t:\t[{}]'.format(i, self.count(i)))



#------------------------------------
# multi context manager for iTOR
#------------------------------------
class MCM:
    """ multi context-manager """
    def from_lot(*lot):
        ds, mode = [], []
        for d,m in lot:
            ds.append(d)
            mode.append(m)
        return MCM(ds, mode)
    def from_list(dsL, mode):
        return MCM(dsL, [mode for _ in range(len(dsL))] )
    def from_lists(dsL, modeL):
        return MCM(dsL, modeL)

    def __init__(self, ds, mode) -> None:
        self.ds, self.mode = ds, mode
    def __enter__(self):
        for ds, mode in zip(self.ds, self.mode):
            ds.open(mode)
        return self.ds
    def __exit__(self, exc_type, exc_val, exc_tb):
        for ds in self.ds:
            ds.close()
        return True



#------------------------------------
# Storage 
#------------------------------------
class STORAGE:
    DEFAULT_ROOT_STORE = '.' #<--- this store refers to the root dir as a store, the relative path is blank
    """
        Represents a collection of stores

        [Members]
        self.cwd        abs path of current working directory (of python)
        self.storage    abs path of storage config (json) file
        self.root       abs path of root dir which is the dir containing storage file
                        Note: 'root_relative_paths' are relative to this root
        self.stores     a dictionary of 'store_alias' v/s 'root_relative_paths' <-- contents of storage file

    """
    def create(root, storage, auto_load=True, auto_save=True):
        """
        creates a new STORAGE with root dir at 'root' where 'storage' is the name of storage configuration file
        * prefered method of creating new storage from scratch
        """
        return STORAGE( os.path.join(root, storage), auto_create=True, auto_load=auto_load, auto_save=auto_save )

    def __init__(self, storage, auto_create=True, auto_load=True, auto_save=True):
        """
        Create a storage configuration using a json file 'storage'
        storage can be relative or absolute, only absolute paths are stored
        storage ia the abs path for storage file
        use STORAGE.create(root, storage) if 'storage' is just the name of storage file located inside root
        """

        self.cwd = os.getcwd() #<-- always returns a abs path
        self.storage = os.path.abspath(storage) # stores abs paths in instances
        self.root = os.path.dirname(self.storage) # abs dir name <-- root
        self.autosave = auto_save

        self.create_config() if auto_create else None #<-- create if not existing, it has no effect if storage exists
        self.load_config() if auto_load else None # without calling load_config(), self.stores will not be created
        
    def load_config(self):
        if os.path.exists(self.storage):
            with open(self.storage, 'r') as f:
                self.stores = json.loads(f.read())
            return True
        else:
            return False

    def save_config(self):
        if os.path.exists(self.storage):
            with open(self.storage, 'w') as f:
                f.write(json.dumps(self.stores, sort_keys=False, indent=4))
            return True
        else:
            return False

    def create_config(self):
        os.makedirs(self.root, exist_ok=True) 
        if not os.path.exists(self.storage):
            with open(self.storage, 'w') as f:
                f.write(json.dumps({STORAGE.DEFAULT_ROOT_STORE:''}, sort_keys=False, indent=4))

    def register(self, **stores):
        """ register multiple stores using a dict of "alias":"root_relative_path """
        for alias, root_rel_path in stores.items():
            self.stores[alias] = root_rel_path
            full_path =  os.path.join(self.root, root_rel_path)
            os.makedirs( full_path, exist_ok=True )
        return self.save_config() if self.autosave else None #<=== save json after adding


    #------------------------------------
    # path query 
    #------------------------------------
    def path_rel(self, alias, file):
        return os.path.join(self.stores[alias], file) 

    def path_abs(self, alias, file):
        return os.path.join(os.path.join(self.root, self.stores[alias]), file)

    def path_py(self, alias, file):
        return os.path.relpath(os.path.join(os.path.join(self.root, self.stores[alias]), file), self.cwd)

    def paths(self, alias, file): # path_ds replaced by call
        """ returns 3-tuple (r,a,p) paths where
            r = root realtive path
            a = absolute path
            p = python relative path
        """
        root_rel_path = self.stores[alias] #<--- ds path relative to root
        file_root_rel_path = os.path.join(root_rel_path, file) #<--- file path relative to root

        root_abs_path = os.path.join(self.root, root_rel_path) #<--- ds path abs
        file_root_abs_path = os.path.join(root_abs_path, file) #<--- abs file path

        py_rel_path = os.path.relpath(file_root_abs_path, self.cwd)

        return file_root_rel_path, file_root_abs_path, py_rel_path # relp, absp, pyp

    def __call__(self, alias, file):  #<--- returns python relative path
        return self.path_py(alias, file)     


    #------------------------------------
    # file IO 
    #------------------------------------
    def save(self, alias, file, data, saveF):
        """ save a file in this storage using saveF function like (lambda path, data: None) """
        r,a,p = self.paths(alias, file)
        saveF(p, data)
        return r, a, p

    def save_py(self, alias, file, data, saveF):
        """ save a file in this storage using saveF function like (lambda path, data: None) """
        p = self.path_py(alias, file)
        saveF(p, data)
        return p

    def save_abs(self, alias, file, data, saveF):
        """ save a file in this storage using saveF function like (lambda path, data: None) """
        a = self.path_abs(alias, file)
        saveF(a, data)
        return a

    def load(self, alias, file, loadF):
        """ load a file from this storage using loadF function like (lambda path: data) """
        r,a,p = self.paths(alias, file)
        return loadF(p), r, a, p

    def load_py(self, alias, file, loadF):
        """ load a file from this storage using loadF function like (lambda path: data) """
        p = self.path_py(alias, file)
        return loadF(p), p

    def load_abs(self, alias, file, loadF):
        """ load a file from this storage using loadF function like (lambda path: data) """
        a = self.path_abs(alias, file)
        return loadF(a), a



#------------------------------------
# Forage
#------------------------------------

class FORAGE(STORAGE):

    def create(root, storage, type_dict, auto_load=True, auto_save=True):
        """
        creates a new STORAGE with root dir at 'root' where 'storage' is the name of storage configuration file
        * prefered method of creating new storage from scratch
        """
        return FORAGE( os.path.join(root, storage), type_dict, auto_create=True, auto_load=auto_load, auto_save=auto_save )
        
    def __init__(self, storage, type_dict, auto_create=True, auto_load=True, auto_save=True):
        """ data_type_dict is a dictionary of   'dtype' : (saveF, loadF)    """
        super().__init__(storage, auto_create, auto_load, auto_save)
        self.type_dict = type_dict

    def save(self, alias, file, data, dtpye):
        r,a,p = self.paths(alias, file)
        self.type_dict[dtpye][0](p, data)
        return r, a, p

    def save_py(self, alias, file, data, dtpye):
        p = self.path_py(alias, file)
        self.type_dict[dtpye][0](p, data)
        return p

    def save_abs(self, alias, file, data, dtpye):
        a = self.path_abs(alias, file)
        self.type_dict[dtpye][0](a, data)
        return a

    def load(self, alias, file, dtpye):
        r,a,p = self.paths(alias, file)
        return self.type_dict[dtpye][1](p), r, a, p

    def load_py(self, alias, file, dtpye):
        p = self.path_py(alias, file)
        return self.type_dict[dtpye][1](p), p

    def load_abs(self, alias, file, dtpye):
        a = self.path_abs(alias, file)
        return self.type_dict[dtpye][1](a), a



#-----------------------------------------------------------------------------------------------------
# Foot-Note:
""" NOTE:
    * Author:           Nelson.S
"""
#-----------------------------------------------------------------------------------------------------
