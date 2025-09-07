from examples.reports.example_csv_report_class import ExampleCSVReport
from pyutils_lib_modules.services.config_manager import ConfigManager
from pyutils_lib_modules.services.StatTimer import StatTimer

ConfigManager().define_setting("application_name",     False,None,"string","Application Name is a Required Field") 
ConfigManager().define_setting("application_secret",   True,None,"string","Application Secret is a Required Field") 


ConfigManager().load_configuration()
logs = ConfigManager().get_logger()

this_timer = StatTimer()
logs.info("Starting Example")

ExampleCSVReport()

logs.info(f"Example Processed In: {this_timer.Duration()}")

