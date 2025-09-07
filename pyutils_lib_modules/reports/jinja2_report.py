import os
from datetime import datetime
from dataclasses import dataclass
from pyutils_lib_modules.services.config_manager import ConfigManager
from pyutils_lib_modules.reports.abstract_report import AbstractReport
from jinja2 import Environment, FileSystemLoader

@dataclass
class Jinja2Report(AbstractReport):
    template_folder                 = None
    template_name                   = None
    extension                       = "txt"

    def __post_init__(self):
        cd = datetime.now().strftime("%Y%m%d")
        self.file_name = f"{cd}_{self.report_name}.{self.extension}"

    def write(self):
        self.reports_folder  = ConfigManager().get_setting("REPORTS_FOLDER_PATH")
        template = ConfigManager().get_constant("templates").get_template(self.template_name)

        this_path = os.path.join(self.reports_folder, self.file_name)
        
        with open(this_path,'wt', encoding='utf-8') as this_report_file:
            this_report = template.render(report = self)        
            this_report_file.write(this_report)        
    
