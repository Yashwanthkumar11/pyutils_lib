# main.py format to be used in other projects

from examples.reports.example_csv_report_class import ExampleCSVReport
from pyutils_lib.services.config_manager import ConfigManager
from pyutils_lib.services.stat_timer import StatTimer

ConfigManager().define_setting("setting_name",False,'xyz',"string","This is a normal non-secret setting") 
ConfigManager().define_setting("secret_setting_name",True,None,"string","This is a secret setting") 


ConfigManager().load_configuration()
logs = ConfigManager().get_logger()

this_timer = StatTimer()
logs.info("Starting Example")

ExampleCSVReport()

logs.info(f"Example Processed In: {this_timer.Duration()}")

