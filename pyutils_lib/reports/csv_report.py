from datetime import datetime
import os, csv

from dataclasses import dataclass, field
from pyutils_lib.reports.abstract_report import AbstractReport
from pyutils_lib.services.config_manager import ConfigManager

@dataclass
class CSVReport(AbstractReport):
    rows:list                   = field(default_factory=list)

    def __post_init__(self):
        cd = datetime.now().strftime("%Y%m%d")
        self.file_name = f"{cd}_{self.report_name}.csv"
        

    def write(self):
        self.reports_folder  = ConfigManager().get_setting("REPORTS_FOLDER_PATH")
        this_path = os.path.join(self.reports_folder, self.file_name)

        with open(this_path, 'w', newline = '') as csvfile:
            this_writer = csv.writer(csvfile, quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
            this_writer.writerows(self.rows)
        