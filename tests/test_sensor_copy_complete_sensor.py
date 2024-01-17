from pathlib import Path
from st2tests.base import BaseSensorTestCase
import tempfile

from copy_complete_sensor import CopyCompleteSensor


class CopyCompleteSensorTestCase(BaseSensorTestCase):
    sensor_cls = CopyCompleteSensor

    def setUp(self):
        super(CopyCompleteSensorTestCase, self).setUp()

        self.watch_directory = tempfile.TemporaryDirectory()

    def test_new_copycomplete(self):
        sensor = self.get_sensor_instance(config={})
        sensor.poll()

        sensor.add_trigger({
            "ref": "gmc_norr.copy_complete",
            "parameters": {
                "watch_directory": self.watch_directory.name,
            }
        })

        self.assertEqual(len(sensor.watched_directories()), 1)
        self.assertEqual(
            sensor.watched_directories()[0],
            Path(self.watch_directory.name)
        )

        run_directory = Path(self.watch_directory.name) / "run1"
        run_directory.mkdir()

        sensor.poll()

        copycomplete = run_directory / "CopyComplete.txt"
        copycomplete.touch()

        assert copycomplete.exists()

        sensor.poll()

        self.assertTriggerDispatched(
            trigger="gmc_norr.copy_complete",
            payload={
                "run_directory": str(run_directory),
            }
        )
        self.assertEqual(len(self.sensor_service.dispatched_triggers), 1)

        # The trigger should not be emitted for the same directory again
        sensor.poll()
        self.assertEqual(len(self.sensor_service.dispatched_triggers), 1)
