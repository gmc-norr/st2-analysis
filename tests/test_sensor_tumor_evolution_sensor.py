from pathlib import Path
from tumor_evolution_sensor import TumorEvolutionSensor
from st2tests.base import BaseSensorTestCase
import tempfile
from unittest.mock import Mock


class TumorEvolutionSensorTest(BaseSensorTestCase):
    sensor_cls = TumorEvolutionSensor

    def setUp(self):
        super(TumorEvolutionSensorTest, self).setUp()

        self.watch_dir = tempfile.TemporaryDirectory()
        self.watch_file = Path(self.watch_dir.name) / "watch.txt"
        self.output_dir = tempfile.TemporaryDirectory()

        self._sensor_setup()

    def _sensor_setup(self):
        self.sensor = self.get_sensor_instance(
            config={
                "notification_email": ["me@mail.com"],
                "tumor_evolution": {
                    "output_directory": str(self.output_dir),
                    "watch_file": str(self.watch_file),
                    "watch_file_instructions": "# test instructions\n",
                    "version": "0.5.4",
                },
                "mounts": [
                    {
                        "win": "G:\\Genetik",
                        "unix": "/mnt/G-Genetik",
                    },
                    {
                        "win": "K:\\Genetik",
                        "unix": "/mnt/testmount",
                    },
                    {
                        "win": "V:\\Genetik",
                        "unix": "/mnt/V-Genetik",
                    },
                ],
            }
        )

    def test_excel_paths(self):
        paths = [
            {
                "input": "G:\\Genetik\\path\\to\\a\\file.xlsx",
                "output": "/mnt/G-Genetik/path/to/a/file.xlsx",
            },
            {
                "input": "G:\\Genetik\\path\\To\\A\\CaseSensitiveFile.xlsx",
                "output": "/mnt/G-Genetik/path/To/A/CaseSensitiveFile.xlsx",
            },
            {
                "input": '"G:\\Genetik\\path\\to\\another\\file.xlsx"',
                "output": "/mnt/G-Genetik/path/to/another/file.xlsx",
            },
            {
                "input": "K:\\Genetik\\path\\to\\a\\file.xlsx",
                "output": "/mnt/testmount/path/to/a/file.xlsx",
            },
            {
                "input": "V:\\Genetik\\path\\to\\a\\file.xlsx",
                "output": "/mnt/V-Genetik/path/to/a/file.xlsx",
            },
            {
                "input": "/storage/path/to/excel/file",
                "output": "/storage/path/to/excel/file",
            },
        ]

        for i, p in enumerate(paths, start=1):
            with open(self.watch_file, "a") as wf:
                wf.write(p["input"])
            self.sensor.poll()
            self.assertEqual(len(self.get_dispatched_triggers()), i)
            self.assertTriggerDispatched(
                trigger="gmc_norr_analysis.tumor_evolution_request",
                payload=dict(
                    excel_file=p["output"],
                    sheet="1",
                ),
            )

    def test_missing_watch_file(self):
        self.assertFalse(self.watch_file.exists())
        self.sensor.poll()
        self.assertTrue(self.watch_file.exists())
        self.assertEqual(len(self.get_dispatched_triggers()), 0)
        with open(self.watch_file) as f:
            self.assertEqual(
                f.read(
                ), self.sensor.config["tumor_evolution"]["watch_file_instructions"]
            )

    def test_missing_watch_file_path(self):
        self.watch_file = Path("/no/such/path/watch.txt")
        self._sensor_setup()
        self.assertFalse(Path(self.watch_file).exists())
        original_poll_interval = self.sensor.get_poll_interval()
        self.sensor.poll()
        self.assertFalse(
            Path(self.sensor.config["tumor_evolution"]["watch_file"]).exists())
        self.assertTriggerDispatched(
            trigger="gmc_norr_analysis.email_notification",
            payload={
                "to": ["me@mail.com"],
                "subject": "[TumorEvolutionSensor] Failed to create watch file",
                "message": "Failed to create watch file: [Errno 2] "
                "No such file or directory: "
                "'/no/such/path/watch.txt'",
            },
        )
        self.assertFalse(self.watch_file.exists())
        self.assertEqual(self.sensor.get_poll_interval(),
                         original_poll_interval * 2)

    def test_missing_mount(self):
        self._sensor_setup()
        original_func = self.sensor._watch_file_ok
        self.sensor._watch_file_ok = Mock(
            side_effect=OSError(112, "Host is down", str(self.watch_file))
        )
        original_poll_interval = self.sensor.get_poll_interval()
        self.sensor.poll()
        self.assertEqual(self.sensor.get_poll_interval(),
                         original_poll_interval * 2)
        self.assertTriggerDispatched("gmc_norr_analysis.email_notification")
        trigger = self.get_dispatched_triggers()[0]
        self.assertEqual(
            trigger["payload"]["message"],
            f"Failed to check watch file: [Errno 112] Host is down: '{self.watch_file}'",
        )

        self.sensor._watch_file_ok = original_func

        # This should create the watch file and reset the polling interval,
        # but no more triggers should be dispatched.
        self.sensor.poll()
        self.assertTrue(self.watch_file.exists())
        self.assertEqual(len(self.get_dispatched_triggers()), 1)
        self.assertEqual(self.sensor.get_poll_interval(),
                         original_poll_interval)

    def test_max_polling_interval(self):
        self.watch_file = Path("/no/such/path/watch.txt")
        self._sensor_setup()

        original_poll_interval = self.sensor.get_poll_interval()

        for i in range(5):
            self.sensor.poll()
            self.assertEqual(len(self.get_dispatched_triggers()), i + 1)
            self.assertEqual(
                self.sensor.get_poll_interval(),
                min(self.sensor.max_poll_interval,
                    original_poll_interval * 2 * 2**i),
            )

    def test_poll_interval_reset(self):
        self._sensor_setup()
        original_poll_interval = self.sensor.get_poll_interval()
        self.assertEqual(original_poll_interval, 60)

        # File has an entry to start with...
        with open(self.watch_file, "w") as f:
            f.write("/path/to/excel_file.xlsx")

        # ... but something is wrong...
        self.sensor._watch_file_ok = Mock(
            side_effect=OSError(
                126, "Required key not available", str(self.watch_file))
        )

        self.sensor.poll()
        # ... so an email trigger should be dispatched...
        self.assertTriggerDispatched(
            trigger="gmc_norr_analysis.email_notification",
        )
        # ... and the polling interval increased
        self.assertEqual(self.sensor.get_poll_interval(),
                         original_poll_interval * 2)

        # Things are now ok...
        self.sensor._watch_file_ok = Mock(return_value=True)

        self.sensor.poll()
        # ... a report generation trigger should be dispatched...
        self.assertTriggerDispatched(
            trigger="gmc_norr_analysis.tumor_evolution_request",
            payload={
                "excel_file": "/path/to/excel_file.xlsx",
                "sheet": "1",
            },
        )
        # ... and the polling interval should be reset
        self.assertEqual(self.sensor.get_poll_interval(),
                         original_poll_interval)

    def test_invalid_encoding(self):
        with open(self.watch_file, "bw") as f:
            f.write("nedlåst".encode("latin-1"))

        self.sensor.poll()
        self.assertEqual(len(self.get_dispatched_triggers()), 1)
        self.assertTriggerDispatched("gmc_norr_analysis.email_notification")
        trigger = self.get_dispatched_triggers()[0]
        self.assertEqual(
            trigger["payload"]["subject"],
            "[TumorEvolutionSensor] Error reading watch file",
        )
