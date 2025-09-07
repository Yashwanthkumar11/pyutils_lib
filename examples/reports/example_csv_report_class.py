from dataclasses import dataclass, field
from datetime import datetime

from pyutils_lib_modules.reports.csv_report import CSVReport
from pyutils_lib_modules.services.report_writer import ReportWriter

@dataclass()
class ExampleCSVReport(CSVReport):
    report_name :str = "Example_CSV_Report"

    def __post_init__(self):
        super().__post_init__()

    # Generate Method collects data
    def generate(self):
        # Reset Rows List, used by parent class to create the CSV, and add a Header Row
        self.rows = []
        self.rows.append(["Issue_name", "Issue Description"])

        for i in range(1, 100):
            this_Issue_name = f"Issue_name-{i}"
            this_description = "Some Boring Description"
            this_row = [this_Issue_name, this_description]
            
            self.rows.append(this_row)

ReportWriter().register(ExampleCSVReport)