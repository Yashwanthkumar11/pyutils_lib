import sys, os
import hashlib
import pickle
import base64
import socket, platform

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends.openssl import backend as openssl_backend


if sys.platform.startswith('win32'):
    import winreg

class CryptoServices:
    __instance = None

    def __new__(cls):
        if CryptoServices.__instance is None:
            CryptoServices.__instance = object.__new__(cls)

        return CryptoServices.__instance

    def __init__(self) -> None:
        if not hasattr(self, 'OSName'):
            self.OSName     = platform.system()
            thisBackend     = openssl_backend

            thisIV          = str(self.getMachineHostname())
            thisSalt        = str(self.getInstallTime())
            thisKey         = str(self.getMachineUUID())

            thisHash        = hashlib.sha3_256()
            thisHash.update(thisKey.encode())
            thisHash.update(thisSalt.encode())
            thisKeyHash     = thisHash.digest()

            thisHash        = hashlib.shake_128()
            thisHash.update(thisIV.encode())
            thisHash.update(thisSalt.encode())

            thisIVHash      = thisHash.digest(16)

            self._Cipher    = Cipher(   algorithms.AES(thisKeyHash),
                                        modes.CBC(thisIVHash),
                                        backend=thisBackend)

    def getMachineUUID(self):

        if sys.platform.startswith('win32'):
            thisKey         = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                            "SOFTWARE\\Microsoft\\Cryptography",0,
                            winreg.KEY_READ | winreg.KEY_WOW64_64KEY)
            thisUuid        = winreg.QueryValueEx(thisKey, "MachineGuid")[0]
            return thisUuid
        else:
            pass

    def getMachineHostname(self):
        return socket.gethostname()

    def getInstallTime(self):

        if sys.platform.startswith('win32'):
            thisKey         = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                            "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion",0,
                            winreg.KEY_READ | winreg.KEY_WOW64_64KEY)
            thisInstallTime = winreg.QueryValueEx(thisKey, "InstallDate")[0]
            return thisInstallTime
        else:
            pass


    def encrypt(self,thisData):
        thisEncryptor           = self._Cipher.encryptor()
        thisBinaryData          = thisData.encode()

        thisPadder              = padding.PKCS7(256).padder()
        thisPaddedBinaryData    = thisPadder.update(thisBinaryData)
        thisPaddedBinaryData   += thisPadder.finalize()

        thisEncryptedBinaryData = thisEncryptor.update(thisPaddedBinaryData) + thisEncryptor.finalize()

        thisEncryptedString     = base64.encodebytes(thisEncryptedBinaryData).decode()
        return thisEncryptedString


    def decrypt(self,thisEncryptedString):
        try:
            thisDecryptor = self._Cipher.decryptor()
            thisBinaryEncryptedString = base64.decodebytes(thisEncryptedString.encode())

            thisDecryptedPaddedData = thisDecryptor.update(thisBinaryEncryptedString) + thisDecryptor.finalize()

            thisUnPadder = padding.PKCS7(256).unpadder()
            thisUnPaddedDecryptedData = thisUnPadder.update(thisDecryptedPaddedData)
            thisUnPaddedDecryptedData += thisUnPadder.finalize()

            thisDecryptedString = thisUnPaddedDecryptedData.decode()
            return thisDecryptedString
        except:
            raise ValueError("Credentials are corrupted , please enter them again")

    def encryptBinary(self, thisBinaryData):
        thisEncryptor = self._Cipher.encryptor()

        thisPadder = padding.PKCS7(256).padder()
        thisPaddedBinaryData = thisPadder.update(thisBinaryData)
        thisPaddedBinaryData += thisPadder.finalize()

        thisEncryptedBinaryData = thisEncryptor.update(thisPaddedBinaryData) + thisEncryptor.finalize()

        return thisEncryptedBinaryData


    def decryptBinary(self,thisBinaryEncryptedData):
        thisDecryptor             = self._Cipher.decryptor()
        thisDecryptedPaddedData   = thisDecryptor.update(thisBinaryEncryptedData) + thisDecryptor.finalize()

        thisUnPadder              = padding.PKCS7(256).unpadder()
        thisUnPaddedDecryptedData = thisUnPadder.update(thisDecryptedPaddedData)
        thisUnPaddedDecryptedData += thisUnPadder.finalize()
        return thisUnPaddedDecryptedData

'''
def EncryptAndSerialize(BinaryFileName, BinaryObjects):
    CryptoServices().init()
    WorkingDir = ConfigManager().GetSetting("RecordCacheDir", os.getcwd(), DataTypes.STRING)
    encrypt = ConfigManager().GetSetting("encrypt", True, DataTypes.BOOLEAN)

    BinaryFileLocation = os.path.join(WorkingDir, BinaryFileName)
    # Open the Binary file and Save the pickle object
    with open(BinaryFileLocation, 'wb') as binary_data:
        if encrypt:
            binary_data.write(CryptoServices().encryptBinary(pickle.dumps(BinaryObjects)))
        else:
            binary_data.write(pickle.dumps(BinaryObjects))


def DecryptAndDeserialize(BinaryFileName):
    CryptoServices().init()
    WorkingDir = ConfigManager().GetSetting("RecordCacheDir", os.getcwd(), DataTypes.STRING)
    encrypt = ConfigManager().GetSetting("encrypt", True, DataTypes.BOOLEAN)
    BinaryFileLocation = os.path.join(WorkingDir, BinaryFileName)
    # Open the Binary file and Save the pickle object
    with open(BinaryFileLocation, "rb") as BinaryFile:
        thisByteData = BinaryFile.read()
    if encrypt:
        return pickle.loads(CryptoServices().decryptBinary(thisByteData))
    else:
        return pickle.loads(thisByteData)
'''