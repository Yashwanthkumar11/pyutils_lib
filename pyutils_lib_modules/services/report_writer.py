import  csv, os, logging

from pyutils_lib_modules.services.config_manager import ConfigManager
from pyutils_lib_modules.services.StatTimer import StatTimer

# Since Abstract Report is loaded dynamically, this setting must be defined here (or in Main)
ConfigManager().define_setting("REPORTS_FOLDER",False, "./reports", "output_folder_path","")

class ReportWriter():
    ''' 
    The ReportWriter is responsible for managing the generation of release documentation for the KEV Fixlet Manager. 
    '''
    __instance = None

    def __new__(cls):
        if ReportWriter.__instance is None:
            ReportWriter.__instance = object.__new__(cls)
        return ReportWriter.__instance

    def __init__(self) -> None:
        if not hasattr(self, 'reports'):
            self.reports = set()

    def register(self, this_report_class):
        self.reports.add(this_report_class)


    def generate_reports(self):
        logs    = ConfigManager().get_logger("report_writer.generate_reports")
        this_timer = StatTimer()
        
        logs.info("Generating Reports")

        for this_report_class in self.reports:
            this_report = this_report_class()
            logs.info(f"Processing Report: {this_report.report_name}")
            this_report.generate()
            this_report.write()
        
        logs.info(f"Reports Generated In {this_timer.Duration()}")



        
