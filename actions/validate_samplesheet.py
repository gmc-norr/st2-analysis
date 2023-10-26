import csv
from pathlib import Path

from st2common.runners.base_action import Action


class ValidateSampleSheet(Action):
    def run(self, run_directory, required_data_columns, data_section="Data"):
        self.data_section = data_section
        self.samplesheet = None
        run_directory = Path(run_directory).resolve()

        if not run_directory.exists():
            self.logger.error(f"run directory not found: {run_directory}")
            return self._result(False, message="run directory not found")
        if not run_directory.is_dir():
            self.logger.error(f"not a directory: {run_directory}")
            return self._result(False, message="run directory is not a directory")

        samplesheets = list(run_directory.glob("SampleSheet*.csv"))

        if len(samplesheets) == 0:
            self.logger.error(f"no samplesheet found in {run_directory}")
            return self._result(False, message="no samplesheet found")

        self.samplesheet = self._get_most_recent_samplesheet(samplesheets)

        samplesheet_data = self._get_data_section()

        if samplesheet_data is None:
            self.logger.error(f"no data section found in {self.samplesheet}")
            return self._result(False, message="no data section found")

        if samplesheet_data.fieldnames is None or len(samplesheet_data.fieldnames) == 0:
            self.logger.error(f"data section is empty in {self.samplesheet}")
            return self._result(False, message="data section is empty")

        for col in required_data_columns:
            if col not in samplesheet_data.fieldnames:
                self.logger.error(f"missing required column: {col}")
                return self._result(False, message=f"missing required column: {col}")

        return self._result(
            True, message="valid samplesheet found"
        )

    def _get_most_recent_samplesheet(self, samplesheets):
        return max(samplesheets, key=lambda x: x.stat().st_mtime)

    def _get_data_section(self):
        data_csv = []
        found_data = False
        with open(self.samplesheet, "r") as f:
            for line in f:
                if not found_data and line.startswith(f"[{self.data_section}]"):
                    found_data = True
                    continue
                if found_data and line[0] == "[":
                    break
                if found_data:
                    data_csv.append(line.strip())

        if not found_data:
            return None

        return csv.DictReader(data_csv)

    def _result(self, success, message=None):
        return (
            success,
            {
                "success": success,
                "message": message,
                "samplesheet": str(self.samplesheet) if self.samplesheet is not None else None,
            },
        )
