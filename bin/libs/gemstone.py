#!/usr/bin/python3
#
# gemconnect.py
#

import os.path
from ctypes import *
#from platform import * 

GciSession = c_void_p
OopType = c_uint64
ByteType = c_char

GCI_ERR_STR_SIZE = 1024
GCI_ERR_reasonSize = GCI_ERR_STR_SIZE
GCI_MAX_ERR_ARGS = 10

OOP_ILLEGAL = 1
OOP_NIL = 20
OOP_One = 10
OOP_Two = 18
OOP_Three = 26

GCI_LOGIN_QUIET = 0x10

class Interface:
    def __init__(self):
        path = os.path.expandvars('$GEMSTONE/lib/libgcits-3.6.2-64.so')
        self.library = CDLL(path)

        self.gciTsVersion = self.library.GciTsVersion
        self.gciTsVersion.restype = c_int
        self.gciTsVersion.argtypes = [c_char_p, c_size_t]

        self.gciI32ToOop = self.library.GciI32ToOop
        self.gciI32ToOop.restype = c_int32
        self.gciI32ToOop.argtypes = [OopType]

        self.gciTsAbort = self.library.GciTsAbort
        self.gciTsAbort.restype = c_bool
        self.gciTsAbort.argtypes = [GciSession, POINTER(GciErrSType)]

        self.gciTsBegin = self.library.GciTsBegin
        self.gciTsBegin.restype = c_bool
        self.gciTsBegin.argtypes = [GciSession, POINTER(GciErrSType)]

        self.gciTsCommit = self.library.GciTsCommit
        self.gciTsCommit.restype = c_bool
        self.gciTsCommit.argtypes = [GciSession, POINTER(GciErrSType)]

        self.gciTsCharToOop = self.library.GciTsCharToOop
        self.gciTsCharToOop.restype = OopType
        self.gciTsCharToOop.argtypes = [c_uint]

        self.gciTsDoubleToSmallDouble = self.library.GciTsDoubleToSmallDouble
        self.gciTsDoubleToSmallDouble.restype = OopType
        self.gciTsDoubleToSmallDouble.argtypes = [c_double]

        self.gciTsExecute = self.library.GciTsExecute
        self.gciTsExecute.restype = OopType
        self.gciTsExecute.argtypes = [
                GciSession,            # GciSession sess
                c_char_p,              # const *char sourceStr 
                OopType,               # OopType sourceOop
                OopType,               # OopType contextObject
                OopType,               # OopType symbolList
                c_int,                 # int flags 
                c_ushort,              # ushort environmentId 
                POINTER(GciErrSType)   # GciErrSType *err
            ]

        self.gciTsExecute_ = self.library.GciTsExecute_
        self.gciTsExecute_.restype = OopType
        self.gciTsExecute_.argtypes = [
                GciSession,            # GciSession sess
                c_char_p,              # const *char sourceStr 
                c_ssize_t,             # ssize_t sourceSize
                OopType,               # OopType sourceOop
                OopType,               # OopType contextObject
                OopType,               # OopType symbolList
                c_int,                 # int flags 
                c_ushort,              # ushort environmentId 
                POINTER(GciErrSType)   # GciErrSType *err
            ]

        self.gciTsExecuteFetchBytes = self.library.GciTsExecuteFetchBytes
        self.gciTsExecuteFetchBytes.restype = c_ssize_t
        self.gciTsExecuteFetchBytes.argtypes = [
                GciSession,            # GciSession sess
                c_char_p,              # const *char sourceStr
                c_ssize_t,             # ssize_t sourceSize
                OopType,               # OopType sourceOop
                OopType,               # OopType contextObject
                OopType,               # OopType symbolList
                c_char_p,              # Byte_Type *result
                c_ssize_t,             # ssize_t maxResultSize
                POINTER(GciErrSType)   # GciErrSType *err
            ]

        self.gciTsLogin = self.library.GciTsLogin
        self.gciTsLogin.restype = GciSession
        self.gciTsLogin.argtypes = [
                c_char_p,              # const char *StoneNameNrs
                c_char_p,              # const char *HostUserId
                c_char_p,              # const char *HostPassword
                c_bool,                # BoolType hostPwIsEncrypted
                c_char_p,              # const char *GemServiceNrs
                c_char_p,              # const char *gemstoneUsername
                c_char_p,              # const char *gemstonePassword
                c_uint,                # unsigned int loginFlags (per GCI_LOGIN* in gci.ht)
                c_int,                 # int haltOnErrNum
                POINTER(c_bool),       # BoolType *executedSessionInit
                POINTER(GciErrSType)   # GciErrSType *err
            ]

        self.gciTsLogout = self.library.GciTsLogout
        self.gciTsLogout.restype = c_bool
        self.gciTsLogout.argtypes = [GciSession, POINTER(GciErrSType)]

        self.gciTsOopIsSpecial = self.library.GciTsOopIsSpecial
        self.gciTsOopIsSpecial.restype = c_bool
        self.gciTsOopIsSpecial.argtypes = [OopType]

        self.gciTsOopToChar = self.library.GciTsOopToChar
        self.gciTsOopToChar.restype = c_int
        self.gciTsOopToChar.argtypes = [OopType]

        self.gciTsResolveSymbol = self.library.GciTsResolveSymbol
        self.gciTsResolveSymbol.restype = OopType
        self.gciTsResolveSymbol.argtypes = [GciSession, c_char_p, OopType, POINTER(GciErrSType)]

        self.gciTsResolveSymbolObj = self.library.GciTsResolveSymbolObj
        self.gciTsResolveSymbolObj.restype = OopType
        self.gciTsResolveSymbolObj.argtypes = [GciSession, OopType, OopType, POINTER(GciErrSType)]

        self.gciTsSessionIsRemote = self.library.GciTsSessionIsRemote
        self.gciTsSessionIsRemote.restype = c_int
        self.gciTsSessionIsRemote.argtypes = [GciSession]

        self.gciTsVersion = self.library.GciTsVersion
        self.gciTsVersion.restype = c_int
        self.gciTsVersion.argtypes = [c_char_p, c_size_t]

class Session:
    def __init__(self, verbose=False):
        self._interface=Interface()
        self._session_id = None
        self.verbose = verbose

    def print(self, *arguments):
        if self.verbose:
            print(*arguments, file=sys.stderr)

    def abort(self) -> None:
        error = GciErrSType()
        if not self._interface.gciTsAbort(self._session_id, byref(error)):
            raise GciException(error)
        return None

    def begin(self) -> None:
        error = GciErrSType()
        if not self._interface.gciTsBegin(self._session_id, byref(error)):
            raise GciException(error)
        return None

    def commit(self) -> None:
        error = GciErrSType()
        if not self._interface.gciTsCommit(self._session_id, byref(error)):
            raise GciException(error)
        return None

    def doubleToSmallDouble(self, aFloat) -> c_double:
        result = self._interface.gciTsDoubleToSmallDouble(aFloat)
        if result == OOP_ILLEGAL:
            raise InvalidArgumentError()
        return result

    def execute(self, session, aString) -> OopType:
        print(f"execute({aString})")
        error = GciErrSType()
        result = self.gciTsExecute(
                session,
                aString.encode('ascii'),
                74753, # 74753 is the oop of String
                OOP_ILLEGAL,
                OOP_NIL,
                0, 0, byref(error))
        print("result", result)
        if result == OOP_ILLEGAL:
            print("execute FAILED")
            raise GciException(error)
        else:
            print("execute SUCCESS")
        return result

    def execute_(self, session, aString) -> OopType:
        print(f"execute_({aString})")
        error = GciErrSType()
        encodedString = aString.encode('ascii')
        result = self.gciTsExecute_(
                session,
                encodedString,
                len(encodedString),
                154113,   # 74753=String, 154113=Utf8
                OOP_ILLEGAL,
                OOP_NIL,
                0,
                0,
                byref(error))
        print("execute_ result", result)
        if result == OOP_ILLEGAL:
            print("execute_ FAILED")
            raise GciException(error)
        else:
            print("execute_ SUCCESS")
        return result

    def executeFetchBytes(self, session, aString): # -> String:
        self.print(f"executeFetchBytes({aString})")
        encodedString = aString.encode('utf-8')
        bufferSize = 1000000
        buffer = create_string_buffer(bufferSize)
        error = GciErrSType()
        numberOfBytes = self._interface.gciTsExecuteFetchBytes(
                self._session_id,       # GciSession sess
                encodedString,          # const *char sourceStr
                len(encodedString),     # ssize_t sourceSize`
                74753,                  # 74753 is the oop of String, OopType sourceOop
                OOP_ILLEGAL,            # OopType contextObject
                OOP_NIL,                # OopType symbolList
                buffer,                 # Byte_Type *result
                bufferSize,             # ssize_t maxResultSize
                byref(error))           # GciErrSType *err
        self.print("executeFetchBytes numberOfBytes", numberOfBytes)
        if numberOfBytes == -1:
            print("executeFetchBytes FAILED")
            raise GciException(error)
        if numberOfBytes >= bufferSize:
            raise 'results exceeds buffer size'
        self.print("executeFetchBytes SUCCESS", numberOfBytes)
        result = buffer.value.decode('utf-8', errors='strict')
        self.print("len", len(result), result.__class__)
        return result

    def I32ToOop(self, arg) -> c_int32:
        result = self._interface.gciI32ToOop(arg)
        return result

    def isSessionValid(self) -> bool:
        return self._interface.gciTsSessionIsRemote(self._session_id) == 1

    def login(self,
              gem_host='localhost',
              stone='gs64stone',
              gs_user='DataCurator',
              gs_password='swordfish',
              netldi='netldi',
              host_user='',
              host_password='') -> GciSession:
        stone_nrs = '!tcp@localhost#server!' + stone
        #gem_nrs = '!tcp@' + gem_host
        gem_nrs = '!tcp@' + gem_host + '#netldi:' + netldi + '#task!gemnetobject'
        if host_user is None:
            host_user = ''
        else:
            host_user = host_user.encode('ascii')
        if host_password is None:
            host_password = ''
        else:
            host_password = host_password.encode('ascii')
        error = GciErrSType()
        executedSessionInit = c_bool()

        #flags = 0
        flags = GCI_LOGIN_QUIET

        self.print('gciTsLogin')
        self.print('stone_nrs', stone_nrs)
        self.print('host_user', host_user)
        self.print('host_password', host_password)
        self.print('hosPwIsEncrypted')
        self.print('GemServiceNrs', gem_nrs)
        self.print('gemstoneUsername', gs_user)
        self.print('gemstonePassword', gs_password)
        self.print('loginFlag', flags)
        self.print('haltOnErrNum')
        self.print('pGciErrSType')
        self._session_id = self._interface.gciTsLogin(
            stone_nrs.encode('ascii'),
            host_user,
            host_password,
            False,
            gem_nrs.encode('ascii'),
            gs_user.encode('ascii'),
            gs_password.encode('ascii'),
            flags,
            0,
            byref(executedSessionInit),
            byref(error))
        self.print('session_id=', self._session_id)
        if self._session_id is None:
            raise GciException(error)

    def logout(self) -> None:
        error = GciErrSType()
        if not self._interface.gciTsLogout(self._session_id, byref(error)):
            raise GciException(error)

    def oopIsSpecial(self, oop) -> c_bool:
        result = self._interface.gciTsOopIsSpecial(oop)
        return result

    def oopToChar(self, oop) -> c_int:
        result = self._interface.gciTsOopToChar(oop)
        # should check for -1
        return result

    def resolveSymbol(self, symbolName) -> OopType:
        error = GciErrSType()
        result = self._interface.gciTsResolveSymbol(
                self._session_id, 
                symbolName.encode('ascii'), 
                OOP_NIL, 
                byref(error))
        if result == OOP_ILLEGAL:
            raise GciException(error)
        return result

    def resolveSymbolObj(self, session, symbolName) -> OopType:
        error = GciErrSType()
        result = self.gciTsResolveSymbolObj(session, symbolName, OOP_NIL, byref(error))
        if result == OOP_ILLEGAL:
            raise GciException(error)
        return result

    def version(self) -> str:
        buffer = create_string_buffer(256)
        code = self._interface.gciTsVersion(buffer, sizeof(buffer))
        assert code == 3
        return buffer.value.decode('ascii')

    def charToOop(self, ch) -> OopType:
        oop = self._interface.gciTsCharToOop(ch)
        # should check for 1 (OOP_ILLEGAL)
        return oop

# see $GEMSTONE/include/gci.ht
class GciErrSType(Structure):
    _fields_ = [
        ('category',        OopType),   # error dictionary
        ('context',         OopType),   # a GsProcess
        ('exceptionObj',    OopType),   # an AbstractException or nil
        ('args',            OopType * GCI_MAX_ERR_ARGS),    # arguments
        ('number',          c_int),     # GemStone error number
        ('argCount',        c_int),     # num of arg in the args[]
        ('fatal',           c_ubyte),   # nonzero if err is fatal
        ('message',         c_char * (GCI_ERR_STR_SIZE + 1)),      # null-terminated Utf8
        ('reason',          c_char * (GCI_ERR_reasonSize + 1))     # null-terminated Utf8
    ]

    def __repr__(self):
        return 'aGciErrSType'

    def __str__(self):
        return ('GciErrSType(category=' + hex(self.category) +   
               ', context=' + hex(self.context) +               
               ', exceptionObj=' + hex(self.exceptionObj) +     
               ', args=' + str(list(map(hex, self.args))[0:self.argCount]) +     
               ', number=' + str(self.number) +                 
               ', argCount=' + str(self.argCount) +             
               ', fatal=' + str(self.fatal) +                   
               ', message=' + str(self.message) +               
               ', reason=' + str(self.reason) + ')')

# Base class for other exceptions
class Error(Exception):
    pass

# Invalid argument for GCI function
class InvalidArgumentError(Error):
    pass

class GciException(Error):

    def __init__(self, ex: GciErrSType):
        super().__init__(str(ex.message))
        self.ex = ex

    def number(self):
        return self.ex.number


