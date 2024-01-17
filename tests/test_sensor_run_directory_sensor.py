from pathlib import Path
from st2tests.base import BaseSensorTestCase
import tempfile

from run_directory_sensor import RunDirectorySensor


class RunDirectorySensorTestCase(BaseSensorTestCase):
    sensor_cls = RunDirectorySensor

    def setUp(self):
        super(RunDirectorySensorTestCase, self).setUp()

        self.watch_directory = tempfile.TemporaryDirectory()

    def test_new_copycomplete(self):
        sensor = self.get_sensor_instance(config={
            "run_directories": [
                {"path": self.watch_directory.name}
            ]
        })
        sensor.poll()

        run_directory = Path(self.watch_directory.name) / "run1"
        run_directory.mkdir()

        sensor.poll()
        assert len(self.get_dispatched_triggers()) == 0

        copycomplete = run_directory / "CopyComplete.txt"
        copycomplete.touch()

        assert copycomplete.exists()

        sensor.poll()

        self.assertTriggerDispatched(
            trigger="gmc_norr.copy_complete",
            payload={
                "run_directory": str(run_directory),
                "host": "localhost"
            }
        )
        self.assertEqual(len(self.get_dispatched_triggers()), 1)

        # The trigger should not be emitted for the same directory again
        sensor.poll()
        self.assertEqual(len(self.get_dispatched_triggers()), 1)
