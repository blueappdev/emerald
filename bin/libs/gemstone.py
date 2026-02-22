#!/usr/bin/python3
#
# gemstone.py
#

import os.path, sys
from ctypes import *

GciSession = c_void_p
OopType = c_uint64
ByteType = c_ubyte

GCI_ERR_STR_SIZE = 1024
GCI_ERR_reasonSize = GCI_ERR_STR_SIZE
GCI_MAX_ERR_ARGS = 10

GCI_PERFORM_FLAG_ENABLE_DEBUG = 1
GCI_PERFORM_FLAG_DISABLE_ASYNC_EVENTS = 2
GCI_PERFORM_FLAG_SINGLE_STEP = 4
GCI_PERFORM_noClientUseraction = 0x10
GCI_PERFORM_FLAG_INTERPRETED = 0x20

OOP_ILLEGAL = 1
OOP_NIL = 20
OOP_MinusOne = 18446744073709551610
OOP_MinusTwo = 18446744073709551602
OOP_Zero = 2
OOP_One = 10
OOP_Two = 18
OOP_Three = 26

OOP_CLASS_STRING = 74753
OOP_CLASS_Utf8 = 154113

GCI_LOGIN_QUIET = 0x10

class Interface:
    def __init__(self):
        path = os.path.expandvars('$GEMSTONE/lib/libgcits-3.6.2-64.so')
        self.library = CDLL(path)

        self.gciI32ToOop = self.library.GciI32ToOop
        self.gciI32ToOop.restype = OopType
        self.gciI32ToOop.argtypes = [c_int32]

        self.gciTsAbort = self.library.GciTsAbort
        self.gciTsAbort.restype = c_bool
        self.gciTsAbort.argtypes = [GciSession, POINTER(GciErrSType)]

        self.gciTsBegin = self.library.GciTsBegin
        self.gciTsBegin.restype = c_bool
        self.gciTsBegin.argtypes = [GciSession, POINTER(GciErrSType)]

        self.gciTsCharToOop = self.library.GciTsCharToOop
        self.gciTsCharToOop.restype = OopType
        self.gciTsCharToOop.argtypes = [c_uint]

        self.gciTsCommit = self.library.GciTsCommit
        self.gciTsCommit.restype = c_bool
        self.gciTsCommit.argtypes = [GciSession, POINTER(GciErrSType)]

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

        self.gciTsNewString = self.library.GciTsNewString
        self.gciTsNewString.restype = OopType
        self.gciTsNewString.argtypes = [GciSession, c_char_p, POINTER(GciErrSType)]

        self.gciTsNewSymbol = self.library.GciTsNewSymbol
        self.gciTsNewSymbol.restype = OopType
        self.gciTsNewSymbol.argtypes = [GciSession, c_char_p, POINTER(GciErrSType)]

        self.gciTsOopIsSpecial = self.library.GciTsOopIsSpecial
        self.gciTsOopIsSpecial.restype = c_bool
        self.gciTsOopIsSpecial.argtypes = [OopType]

        self.gciTsOopToChar = self.library.GciTsOopToChar
        self.gciTsOopToChar.restype = c_int
        self.gciTsOopToChar.argtypes = [OopType]

        self.gciTsPerform = self.library.GciTsPerform
        self.gciTsPerform.restype = OopType
        self.gciTsPerform.argtypes = [
                GciSession,            # GciSession sess
                OopType,               # OopType receiver
                OopType,               # OopType aSymbol
                c_char_p,              # const *char selectorStr
                POINTER(OopType),      # OopType *args
                c_int,                 # int numArgs
                c_int,                 # int flags (per GCI_PERFORM_FLAG* in gcicmn.ht)
                c_ushort,              # ushort environmentId (normally zero)
                POINTER(GciErrSType)   # GciErrSType *err
            ]

        self.gciTsPerformFetchBytes = self.library.GciTsPerformFetchBytes
        self.gciTsPerformFetchBytes.restype = c_ssize_t
        self.gciTsPerformFetchBytes.argtypes = [
                GciSession,            # GciSession sess
                OopType,               # OopType receiver
                c_char_p,              # const *char selectorStr
                POINTER(OopType),      # OopType *args
                c_int,                 # int numArgs
                c_char_p,              # Byte_Type *result
                c_ssize_t,             # ssize_t maxResultSize
                POINTER(GciErrSType)   # GciErrSType *err
            ]

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

    def execute(self, aString) -> OopType:
        self.print(f"execute({aString})")
        error = GciErrSType()
        result = self._interface.gciTsExecute(
                self._session_id,
                aString.encode('utf-8'),
                OOP_CLASS_Utf8,
                OOP_ILLEGAL,
                OOP_NIL,
                0, 0, byref(error))
        if result == OOP_ILLEGAL:
            raise GciException(error)
        return result

    def execute_(self, aString) -> OopType:
        self.print(f"execute_({aString})")
        error = GciErrSType()
        encodedString = aString.encode('utf-8')
        result = self._interface.gciTsExecute_(
                self._session_id,     # GciSession sess
                encodedString,        # const *char sourceStr 
                len(encodedString),   # ssize_t sourceSize
                OOP_CLASS_Utf8,       # OopType sourceOop (OOP_CLASS_STRING or OOP_CLASS_Utf8)
                OOP_ILLEGAL,          # OopType contextObject
                OOP_NIL,              # OopType symbolList
                0,                    # int flags 
                0,                    # ushort environmentId 
                byref(error))         # GciErrSType *err
        self.print("execute_ result", result)
        if result == OOP_ILLEGAL:
            self.print("execute_ FAILED")
            raise GciException(error)
        else:
            self.print("execute_ SUCCESS")
        return result

    def executeFetchBytes(self, aString) -> str:
        self.print(f"executeFetchBytes({aString})")
        encodedString = aString.encode('utf-8')
        bufferSize = 1000000
        buffer = create_string_buffer(bufferSize)
        error = GciErrSType()
        numberOfBytes = self._interface.gciTsExecuteFetchBytes(
                self._session_id,       # GciSession sess
                encodedString,          # const *char sourceStr
                len(encodedString),     # ssize_t sourceSize`
                OOP_CLASS_Utf8,         # OOP_CLASS_STRING, OOP_CLASS_Utf8
                OOP_ILLEGAL,            # OopType contextObject
                OOP_NIL,                # OopType symbolList
                buffer,                 # Byte_Type *result
                bufferSize,             # ssize_t maxResultSize
                byref(error))           # GciErrSType *err
        self.print("executeFetchBytes numberOfBytes", numberOfBytes)
        if numberOfBytes == -1:
            raise GciException(error)
        if numberOfBytes >= bufferSize:
            raise 'results exceeds buffer size'
        self.print("executeFetchBytes SUCCESS", numberOfBytes)
        result = buffer.value.decode('utf-8', errors='strict')
        self.print("len", len(result), result.__class__)
        return result

    def perform(self, receiver : OopType, aSymbol : OopType, selectorStr, arguments) -> OopType:
        error = GciErrSType()
        result = self._interface.gciTsPerform(
                self._session_id,       # GciSession sess
                receiver,               # OopType receiver
                aSymbol,                # OopType aSymbol
                selectorStr.encode('utf-8'),   # const char* selectorStr
                (OopType * len(arguments))(*arguments), # OopType *args
                len(arguments),         # int numArgs
                0,                      # int flags (per GCI_PERFORM_FLAG* in gcicmn.ht)
                0,                      # ushort environmentId (normally zero)
                byref(error))           # GciErrSType *err)
        if result == OOP_ILLEGAL:
            raise GciException(error)
        return result

    def performFetchBytes(self, receiver : OopType, selectorStr : str, arguments) -> str:
        self.print(f"performFetchBytes({selectorStr})")
        bufferSize = 1000000
        buffer = create_string_buffer(bufferSize)
        error = GciErrSType()
        numberOfBytes = self._interface.gciTsPerformFetchBytes(
                self._session_id,       # GciSession sess
                receiver,               # OopType receiver
                selectorStr.encode('utf-8'),   # const char* selectorStr
                (OopType * len(arguments))(*arguments), # OopType *args
                len(arguments),         # int numArgs
                buffer,                 # Byte_Type *result
                bufferSize,             # ssize_t maxResultSize
                byref(error))           # GciErrSType *err
        if numberOfBytes == -1:
            raise GciException(error)
        if numberOfBytes >= bufferSize:
            raise 'results exceeds buffer size'
        result = buffer.value.decode('utf-8', errors='strict')
        return result

    def I32ToOop(self, arg) -> OopType:
        result = self._interface.gciI32ToOop(arg)
        return result

    def isSessionValid(self) -> bool:
        return self._interface.gciTsSessionIsRemote(self._session_id) == 1

    def login(self,
              gem_host='localhost',
              stone='gs64stone',
              gs_user='DataCurator',
              gs_password='',
              netldi='gs64ldi',
              host_user='',
              host_password='') -> GciSession:
        stone_nrs = '!tcp@localhost#server!' + stone
        #gem_nrs = '!tcp@' + gem_host
        gem_nrs = '!tcp@' + gem_host + '#netldi:' + netldi + '#task!gemnetobject'
        #flags = 0
        flags = GCI_LOGIN_QUIET
        executedSessionInit = c_bool()
        error = GciErrSType()

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
            stone_nrs.encode('ascii'),        # const char *StoneNameNrs
            host_user.encode('ascii'),        # const char *HostUserId
            host_password.encode('ascii'),    # const char *HostPassword
            False,                            # BoolType hostPwIsEncrypted
            gem_nrs.encode('ascii'),          # const char *GemServiceNrs
            gs_user.encode('ascii'),          # const char *gemstoneUsername
            gs_password.encode('ascii'),      # const char *gemstonePassword
            flags,                            # unsigned int loginFlags (per GCI_LOGIN* in gci.ht)
            0,                                # int haltOnErrNum
            byref(executedSessionInit),       # BoolType *executedSessionInit
            byref(error))                     # GciErrSType *err
        self.print('session_id=', self._session_id)
        if self._session_id is None:
            raise GciException(error)

    def logout(self) -> None:
        error = GciErrSType()
        if not self._interface.gciTsLogout(self._session_id, byref(error)):
            raise GciException(error)

    def newString(self, str) -> OopType:
        error = GciErrSType()
        result = self._interface.gciTsNewString(
                self._session_id, 
                str.encode('utf-8'), 
                byref(error))
        if result == OOP_ILLEGAL:
            raise GciException(error)
        return result

    def newSymbol(self, str) -> OopType:
        error = GciErrSType()
        result = self._interface.gciTsNewSymbol(
                self._session_id, 
                str.encode('utf-8'), 
                byref(error))
        if result == OOP_ILLEGAL:
            raise GciException(error)
        return result


    def oopIsSpecial(self, oop) -> c_bool:
        result = self._interface.gciTsOopIsSpecial(oop)
        return result

    def oopToChar(self, oop) -> c_int:
        result = self._interface.gciTsOopToChar(oop)
        # should check for -1
        return result

    def resolveSymbol(self, symbolName : str) -> OopType:
        error = GciErrSType()
        result = self._interface.gciTsResolveSymbol(
                self._session_id, 
                symbolName.encode('ascii'), 
                OOP_NIL, 
                byref(error))
        if result == OOP_ILLEGAL:
            raise GciException(error)
        return result

    def resolveSymbolObj(self, symbolName : OopType) -> OopType:
        error = GciErrSType()
        result = self._interface.gciTsResolveSymbolObj(
                self._session_id, 
                symbolName, 
                OOP_NIL, 
                byref(error))
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


