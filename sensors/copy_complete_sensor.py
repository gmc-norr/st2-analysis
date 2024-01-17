from pathlib import Path
from st2reactor.sensor.base import PollingSensor


class CopyCompleteSensor(PollingSensor):
    def __init__(self, sensor_service, config=None, poll_interval=60):
        super(CopyCompleteSensor, self).__init__(sensor_service, config, poll_interval)
        self._logger = self.sensor_service.get_logger(__name__)

        self._directories = []
        self._processed_run_directories = set()

    def setup(self):
        pass

    def poll(self):
        for d in self._directories:
            for child in d.iterdir():
                if child.is_file() or child in self._processed_run_directories:
                    continue

                copycomplete = child / "CopyComplete.txt"
                if copycomplete.exists():
                    self._processed_run_directories.add(child)
                    self.sensor_service.dispatch(
                        trigger="gmc_norr.copy_complete",
                        payload={
                            "run_directory": str(child),
                        }
                    )

    def cleanup(self):
        pass

    def add_trigger(self, trigger):
        self._logger.error(f"adding trigger: {trigger}")

        ref = trigger.get("ref")
        if ref is None:
            self._logger.error("trigger did not contain a ref")
            raise Exception("trigger did not contain a ref")

        trigger_type = trigger.get("type")
        if trigger_type != "gmc_norr.copy_complete":
            self._logger.error(f"trigger not supported: {trigger_type}")
            raise Exception(f"unsupported trigger type: {trigger_type}")

        config_section = trigger.get("parameters", {}).get("config_section")
        watch_dir = Path(self._config.get(config_section, {}).get("watch_directory"))
        if watch_dir is None:
            self._logger.error("trigger did not contain a watch_directory")
            raise Exception("trigger did not contain a watch_directory")
        if not watch_dir.exists():
            self._logger.error(f"watch directory does not exist: {watch_dir}")
            raise Exception("watch directory does not exist")

        self._logger.info(f"watch directory added: {watch_dir.name}")

        self._directories.append(watch_dir)

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass

    def watched_directories(self):
        return self._directories
