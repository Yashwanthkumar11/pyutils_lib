import os, shutil, datetime, yaml, logging, argparse
from pyutils_lib_modules.model.config_setting import ConfigSetting
from pyutils_lib_modules.services.crypto_service import CryptoServices

class ConfigManager():
    '''
 Description   
    -Managing configuration is a common task in software development which involves handling parameters,options,
    connection details,file paths,API keys,feature flags and other customizable parameters.
    -This utility helps manage the configuration settings within Python applications.

Below are steps on how to use ConfigManager.

    STEP 1: Define the settings using ConfigManager().define_setting(key,is_secret,value,datatype,Description). 
    (a) Defining a setting which is NOT a secret.
    ConfigManager().define_setting("setting_name",False,"setting_value",str,"Description of the setting") 
    (b) Defining a setting which is a secret.
    ConfigManager().define_setting("secret_setting_name",True,None,str,"Description of the secret setting") 

    STEP 2: Load the configuration. This step should be executed after all the settings are defined.
    ConfigManager().load_configuration()

    STEP 3: Use/Get the Config settings whereever needed using "ConfigManager().get_setting(key)".
    print(ConfigManager().get_setting("setting_name"))

Note: This is implemented as a singleton. So, the application using this has only a single instance of ConfigManager.
'''
    __instance = None
    def __new__(cls,logger_name="pyLog", config_file_name="main"):
        if ConfigManager.__instance is None:
            ConfigManager.__instance = object.__new__(cls)
        return ConfigManager.__instance

    def __init__(self,logger_name="pyLog", config_file_name="main") -> None:
        if not hasattr(self, 'is_configured'):
            self.is_configured = False
            self.logger_name                = logger_name
            self.main_config_file_name      = f"{config_file_name}.conf"
            self.secrets_config_file_name   = f"{config_file_name}.conf.secrets"

            self.schema                 = {}
            self.constants              = {}

            self.cryptoservice          = CryptoServices()

            self.arg_parser             = argparse.ArgumentParser(prog='ConfigManager',)

            self.define_setting(key="logs_folder", default_value="logs", datatype="output_folder_path") 




#Accessor Methods
    def define_setting(self, key:str, is_secret:bool=False, default_value=None, datatype=None, description:str=None):
        this_key = key.upper()
        if this_key not in self.schema.keys():
            this_setting                = ConfigSetting()
            this_setting.key            = this_key
            this_setting.is_secret      = is_secret
            this_setting.value          = default_value
            this_setting.datatype       = datatype
            this_setting.description    = description

            self.schema[this_key]            = this_setting

            self.arg_parser.add_argument(f'--{this_key.replace("_","-")}', action='store', nargs='?')
        else:
            raise Exception("Setting Already Defined")

    def get_setting(self, key):
        this_key = key.upper()
        if not self.schema[this_key].is_secret:
            return self.schema[this_key].value
        else:
            encrypted_value = self.schema[this_key].value
            decrypted_value = self.cryptoservice.decrypt(encrypted_value)
            return decrypted_value

    def define_constant(self, key:str, is_secret:bool=False, default_value=None, datatype=None, description:str=None):
        this_key = key.upper()
        if this_key not in self.schema.keys():
            this_setting                = ConfigSetting()
            this_setting.key            = this_key
            this_setting.is_secret      = is_secret
            this_setting.value          = default_value
            this_setting.datatype       = datatype
            this_setting.description    = description

            self.constants[this_key]            = this_setting
        else:
            raise Exception(f"Constant already defined: {this_key}")

    def get_constant(self, key):
        this_key = key.upper()
        if not self.constants[this_key].is_secret:
            return self.constants[this_key].value
        else:
            encrypted_value = self.constants[this_key].value
            decrypted_value = self.cryptoservice.decrypt(encrypted_value)
            return decrypted_value        

    def get_logger(self, logger_name=""):
        if logger_name:
            logger_name = f"{self.logger_name}.{logger_name}"

        return logging.getLogger(logger_name)

    def load_configuration(self): 
        self.load_config_files()

        self.load_setting_overrides()

        self.load_missing_settings()

        self.validate_folder_paths()
        self.configure_logging()

        self.save_config_files()

        self.is_configured = True

# Utility Functions
    def load_config_files(self): 
        these_setting_values = self.load_config_file(self.main_config_file_name)
        these_setting_values.update(self.load_config_file(self.secrets_config_file_name))

        for this_key, this_value in these_setting_values.items():
            if this_key in self.schema.keys():
                this_setting = self.schema[this_key]
                this_setting.value = this_value
    
    def load_config_file(self, filename):
        these_settings = {}
        
        if os.path.exists(filename):
            with open(filename, mode="rt", encoding="utf-8") as this_file:
                these_settings = yaml.safe_load(this_file)
        
        return these_settings

    def save_config_files(self):
        main_config_settings = {}
        secret_config_settings = {}

        for this_setting in self.schema.values():
            if this_setting.source != "environment" and this_setting.source != "args":            
                if this_setting.is_secret:
                    secret_config_settings[this_setting.key] = this_setting.value
                else:
                    main_config_settings[this_setting.key] = this_setting.value

        self.save_config_file(self.main_config_file_name, main_config_settings)
        if len(secret_config_settings.keys()):
            self.save_config_file(self.secrets_config_file_name, secret_config_settings)        

    def save_config_file(self, filename, data):
        with open(filename, mode="wt", encoding="utf-8") as this_file:
            yaml.dump(data, this_file)

    def load_setting_overrides(self):
        args, unknown = self.arg_parser.parse_known_args()
        these_arguments = vars(args) 

        for this_setting in self.schema.values():
            if this_setting.key in os.environ:
                this_setting.value = os.environ.get(this_setting.key)
                this_setting.source = "environment"
            
            if this_setting.key in these_arguments.keys() and these_arguments[this_setting.key] is not None:
                this_setting.value = these_arguments[this_setting.key]
                this_setting.source = "args"

    def load_missing_settings(self):
        for this_setting in self.schema.values():
            if this_setting.value is None:
                if this_setting.default_value is not None:
                    this_setting.value = this_setting.default_value
                else:
                    self.get_setting_from_user(this_setting)
                
    def get_setting_from_user(self, this_setting):
        print("\n", this_setting.description)
        this_value = input(f"Enter the value for {this_setting.key}: ")

        if this_setting.is_secret:
            this_value = CryptoServices().encrypt(this_value)

        this_setting.value = this_value

    def initialize_output_folder_path(self, folder_path:str):
        if os.path.isdir(folder_path):
            shutil.rmtree(folder_path)

        os.makedirs(folder_path)        

    def validate_folder_paths(self):
        for this_setting_name in self.schema.keys():
            this_setting = self.schema[this_setting_name]

            if this_setting.datatype == "output_folder_path":
                if os.path.isdir(this_setting.value):
                    shutil.rmtree(this_setting.value)

                os.makedirs(this_setting.value)

            if this_setting.datatype == "input_folder_path":
                if not os.path.isdir(this_setting.value):
                    raise Exception(f"Input Folder: {this_setting_name} is required in main.conf")
  
    def rotating_filename(self):
        this_log_folder     = self.get_setting("logs_folder")
        this_logger_name    = self.logger_name
        return f'{this_log_folder}\{this_logger_name}_'+ datetime.datetime.now().strftime("%Y%m%d_%H%M%S")+".log"

    def configure_logging(self):
        logs = logging.getLogger()
        logs.setLevel(logging.DEBUG)

        fh = logging.FileHandler(self.rotating_filename())
        fh.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

        logs.addHandler(fh)
        logs.addHandler(logging.StreamHandler())

        return logs

