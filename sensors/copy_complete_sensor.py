import json
from pathlib import Path
from paramiko.client import SSHClient, AutoAddPolicy
from st2reactor.sensor.base import PollingSensor
from typing import Dict, List, Optional, Union


class RunDirectoryState:
    NEW = "new"
    PROCESSING = "processing"
    PROCESSED = "processed"


class CopyCompleteSensor(PollingSensor):
    _dispatched_run_directories: List[Dict[str, str]]

    def __init__(self, sensor_service, config=None, poll_interval=60):
        super(CopyCompleteSensor, self).__init__(sensor_service, config, poll_interval)
        self._logger = self.sensor_service.get_logger(__name__)
        self._dispatched_run_directories = []

        dispatched_run_directories = self.sensor_service.get_value("dispatched_run_directories")
        if dispatched_run_directories is not None:
            self._dispatched_run_directories = json.loads(dispatched_run_directories)

    def setup(self):
        pass

    def poll(self):
        user = self.sensor_service.get_value("service_user", local=False)
        pwd = self.sensor_service.get_value("service_password", local=False, decrypt=True)

        watch_directories = self.config.get("copy_complete", {}).get("watch_directories", [])
        for wd in watch_directories:
            self._logger.debug(f"checking watch directory: {wd}")

            host = wd.get("host", "localhost")

            client = SSHClient()
            client.set_missing_host_key_policy(AutoAddPolicy)

            self._logger.debug(f"connecting to {host} as {user}")

            client.connect(
                hostname=host,
                username=user,
                password=pwd,
            )

            _, stdout, stderr = client.exec_command(
                f"find {wd['path']} -maxdepth 2 -mindepth 2 -type f -name CopyComplete.txt"
            )

            for line in stdout:
                copycomplete_path = Path(line.strip())
                run_directory = copycomplete_path.parent
                self._logger.debug(f"found copycomplete: {host}:{copycomplete_path}")
                if self._is_dispatched(run_directory, host):
                    self._logger.debug(f"already dispatched, skipping: {host}:{run_directory}")
                    continue
                self._add_run_directory(run_directory, host)
                self._sensor_service.dispatch(
                    trigger="gmc_norr.copy_complete",
                    payload={"run_directory": str(run_directory), "host": host},
                )

            for line in stderr:
                self._logger.warning(f"stderr: {line}")

            client.close()

            self._update_datastore()

    def cleanup(self):
        pass

    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass

    def _add_run_directory(self, run_directory: Path, host: str):
        self._dispatched_run_directories.append({"path": str(run_directory), "host": host})

    def _is_dispatched(self, run_directory: Union[Path, str], host: str):
        matches = filter(
            lambda x: x["path"] == str(run_directory) and x["host"] == host,
            self._dispatched_run_directories,
        )
        return len(list(matches)) > 0

    def _update_datastore(self):
        self.sensor_service.set_value(
            "dispatched_run_directories",
            json.dumps(self._dispatched_run_directories)
        )
