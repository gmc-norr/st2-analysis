from pathlib import Path
from sensors.tumor_evolution_sensor import TumorEvolutionSensor
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
        self.sensor = self.get_sensor_instance(config={
            "notification_email": ["me@mail.com"],
            "tumor_evolution": {
                "output_directory": str(self.output_dir),
                "watch_file": str(self.watch_file),
                "watch_file_instructions": "# test instructions\n",
                "version": "0.5.4"
            }
        })

    def test_excel_paths(self):
        paths = [
            {
                "input": "G:\\Genetik\\path\\to\\a\\file.xlsx",
                "output": "/mnt/G-Genetik/path/to/a/file.xlsx",
            },
            {
                "input": "\"G:\\Genetik\\path\\to\\another\\file.xlsx\"",
                "output": "/mnt/G-Genetik/path/to/another/file.xlsx",
            },
            {
                "input": "K:\\Genetik\\path\\to\\a\\file.xlsx",
                "output": "/mnt/K-Genetik/path/to/a/file.xlsx",
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
                )
            )

    def test_missing_watch_file(self):
        self.assertFalse(self.watch_file.exists())
        self.sensor.poll()
        self.assertTrue(self.watch_file.exists())
        self.assertEqual(len(self.get_dispatched_triggers()), 0)
        with open(self.watch_file) as f:
            self.assertEqual(
                f.read(),
                self.sensor.config["tumor_evolution"]
                                  ["watch_file_instructions"]
            )

    def test_missing_watch_file_path(self):
        self.watch_file = Path("/no/such/path/watch.txt")
        self._sensor_setup()
        self.assertFalse(
            Path(self.watch_file).exists()
        )
        original_poll_interval = self.sensor.get_poll_interval()
        self.sensor.poll()
        self.assertFalse(
            Path(self.sensor.config["tumor_evolution"]["watch_file"]).exists()
        )
        self.assertTriggerDispatched(
            trigger="gmc_norr_analysis.notification_email",
            payload={
                "to": ["me@mail.com"],
                "subject": "[TumorEvolutionSensor] Failed to "
                           "create watch file",
                "message": "Failed to create watch file: [Errno 2] "
                           "No such file or directory: "
                           "'/no/such/path/watch.txt'"
            }
        )
        self.assertFalse(self.watch_file.exists())
        self.assertEqual(
            self.sensor.get_poll_interval(),
            original_poll_interval * 2
        )

    def test_missing_mount(self):
        self._sensor_setup()
        original_func = self.sensor._watch_file_ok
        self.sensor._watch_file_ok = Mock(
            side_effect=OSError(112, "Host is down", str(self.watch_file))
        )
        original_poll_interval = self.sensor.get_poll_interval()
        self.sensor.poll()
        self.assertEqual(
            self.sensor.get_poll_interval(),
            original_poll_interval * 2
        )
        self.assertTriggerDispatched("gmc_norr_analysis.notification_email")
        trigger = self.get_dispatched_triggers()[0]
        self.assertEqual(
            trigger["payload"]["message"],
            "Failed to check watch file: [Errno 112] "
            f"Host is down: '{self.watch_file}'"
        )

        self.sensor._watch_file_ok = original_func

        # This should create the watch file and reset the polling interval,
        # but no more triggers should be dispatched.
        self.sensor.poll()
        self.assertTrue(self.watch_file.exists())
        self.assertEqual(len(self.get_dispatched_triggers()), 1)
        self.assertEqual(
            self.sensor.get_poll_interval(),
            original_poll_interval
        )

    def test_max_polling_interval(self):
        self.watch_file = Path("/no/such/path/watch.txt")
        self._sensor_setup()

        original_poll_interval = self.sensor.get_poll_interval()

        self.sensor.poll()
        self.assertEqual(len(self.get_dispatched_triggers()), 1)
        self.assertEqual(
            self.sensor.get_poll_interval(),
            original_poll_interval * 2
        )

        self.sensor.poll()
        self.assertEqual(len(self.get_dispatched_triggers()), 2)
        self.assertEqual(
            self.sensor.get_poll_interval(),
            original_poll_interval * 4
        )

        self.sensor.poll()
        self.assertEqual(len(self.get_dispatched_triggers()), 3)
        self.assertEqual(
            self.sensor.get_poll_interval(),
            original_poll_interval * 8
        )

        self.sensor.poll()
        self.assertEqual(len(self.get_dispatched_triggers()), 4)
        self.assertEqual(
            self.sensor.get_poll_interval(),
            original_poll_interval * 16
        )

        self.sensor.poll()
        self.assertEqual(len(self.get_dispatched_triggers()), 5)
        self.assertEqual(
            self.sensor.get_poll_interval(),
            self.sensor.max_poll_interval
        )
