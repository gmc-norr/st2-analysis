import datetime
import os
from pathlib import Path
import shutil
from st2tests.base import BaseActionTestCase
import tempfile

from validate_samplesheet import ValidateSampleSheet


class SampleSheetValidatorTest(BaseActionTestCase):
    action_cls = ValidateSampleSheet

    def setUp(self):
        global n
        super().setUp()

        self.samplesheet = Path(__file__).parent / "fixtures" / "SampleSheet.csv"
        self.run_directory = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.run_directory.cleanup()

    def test_most_recent_samplesheet(self):
        latest_samplesheet = Path(self.run_directory.name) / "SampleSheet_v3.csv"
        old_samplesheet = Path(self.run_directory.name) / "SampleSheet_v2.csv"
        older_samplesheet = Path(self.run_directory.name) / "SampleSheet_v1.csv"

        shutil.copy(self.samplesheet, latest_samplesheet)
        shutil.copy(self.samplesheet, old_samplesheet)
        shutil.copy(self.samplesheet, older_samplesheet)

        epoch_time = datetime.datetime.now().timestamp()
        os.utime(old_samplesheet, (epoch_time, epoch_time - 2000))
        os.utime(older_samplesheet, (epoch_time, epoch_time - 4000))

        action = self.get_action_instance()
        results = action.run(
            run_directory=self.run_directory.name,
            data_section="Data",
            required_data_columns=[]
        )

        assert results[1]["samplesheet"].name == "SampleSheet_v3.csv"

    def test_valid_samplesheet(self):
        latest_samplesheet = Path(self.run_directory.name) / "SampleSheet.csv"
        shutil.copy(self.samplesheet, latest_samplesheet)

        action = self.get_action_instance()
        results = action.run(
            run_directory=self.run_directory.name,
            data_section="Data",
            required_data_columns=[
                "SampleID",
                "index",
                "index2",
            ],
        )

        assert results[0]
        assert results[1]["samplesheet"].name == "SampleSheet.csv"

    def test_missing_columns(self):
        samplesheet = Path(self.run_directory.name) / "SampleSheet.csv"
        shutil.copy(self.samplesheet, samplesheet)

        action = self.get_action_instance()
        results = action.run(
            run_directory=self.run_directory.name,
            data_section="Data",
            required_data_columns=[
                "SampleID",
                "index",
                "index2",
                "sex",
            ],
        )

        assert not results[0]
        assert results[1]["message"] == "missing required column: sex"

    def test_missing_data_section(self):
        samplesheet = Path(self.run_directory.name) / "SampleSheet.csv"
        shutil.copy(self.samplesheet, samplesheet)

        action = self.get_action_instance()
        results = action.run(
            run_directory=self.run_directory.name,
            data_section="BCLConvert_Data",
            required_data_columns=[
                "SampleID",
                "index",
                "index2",
            ]
        )

        assert not results[0]
        assert results[1]["message"] == "no data section found"

    def test_nonexistent_directory(self):
        action = self.get_action_instance()
        results = action.run(
            run_directory="nonexistent",
            data_section="Data",
            required_data_columns=[
                "SampleID",
                "index",
                "index2",
            ]
        )

        assert not results[0]
        assert results[1]["message"] == "run directory not found"

    def test_invalid_directory(self):
        samplesheet = Path(self.run_directory.name) / "SampleSheet.csv"
        samplesheet.touch()

        action = self.get_action_instance()
        results = action.run(
            run_directory=samplesheet,
            data_section="Data",
            required_data_columns=[
                "SampleID",
                "index",
                "index2",
            ]
        )

        assert not results[0]
        assert results[1]["message"] == "run directory is not a directory"

    def test_missing_samplesheet(self):
        action = self.get_action_instance()
        results = action.run(
            run_directory=self.run_directory.name,
            data_section="Data",
            required_data_columns=[
                "SampleID",
                "index",
                "index2",
            ]
        )

        assert not results[0]
        assert results[1]["message"] == "no samplesheet found"
