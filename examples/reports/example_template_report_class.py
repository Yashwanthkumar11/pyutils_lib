from dataclasses import dataclass, field
from datetime import datetime

from pyutils_lib.reports.jinja2_report import Jinja2Report
from datetime import date

from pyutils_lib.services.report_writer import ReportWriter

@dataclass
class ReleaseNotes(Jinja2Report):
    report_name :str = "Example_Jinja2Report"

    def __post_init__(self):
        self.template_name = "release_notes/template.jinja2"

        super().__post_init__()


    def generate(self):
        # Every Property of This Report Class is Accessible in the Jinja2 Template Named Above. 
        pass

ReportWriter().register(ReleaseNotes)    