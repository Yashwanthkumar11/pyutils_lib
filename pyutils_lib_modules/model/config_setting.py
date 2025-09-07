from dataclasses import dataclass
from typing import List,Any

@dataclass()
class ConfigSetting:
    key             :str            = None
    is_secret       :bool           = False
    description     :str            = None
    default_value   :Any            = None
    value           :Any            = None
    datatype        :str            = None
    source          :str            = "config"
    
    
    

            
        