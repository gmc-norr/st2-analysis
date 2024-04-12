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
                "watch_file_instructions": "test instructions",
                "version": "0.5.4"
            }
        })

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
        self.sensor.poll()
        self.assertFalse(
            Path(self.sensor.config["tumor_evolution"]["watch_file"]).exists()
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

        # This should create the watch file and reset the polling interval
        self.sensor.poll()
        self.assertEqual(len(self.get_dispatched_triggers()), 1)
        self.assertEqual(
            self.sensor.get_poll_interval(),
            original_poll_interval
        )
