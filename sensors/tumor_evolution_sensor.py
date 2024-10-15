from pathlib import Path
import re
from st2reactor.sensor.base import PollingSensor


class TumorEvolutionSensor(PollingSensor):
    def __init__(self, sensor_service, config, poll_interval=60):
        super(TumorEvolutionSensor, self).__init__(sensor_service, config, poll_interval)
        self._original_poll_interval = self.get_poll_interval()
        self.max_poll_interval = 1200
        self.logger = self.sensor_service.get_logger(__name__)
        self.watch_file = Path(self.config["tumor_evolution"]["watch_file"])
        self.watch_file_instructions = self.config["tumor_evolution"]["watch_file_instructions"]

    def setup(self):
        pass

    def _watch_file_ok(self):
        try:
            return self.watch_file.exists()
        except OSError:
            raise

    def _increase_poll_interval(self):
        self.set_poll_interval(min(
            self.get_poll_interval() * 2,
            self.max_poll_interval
        ))

    def poll(self):
        self.logger.debug(f"looking for requests in {self.watch_file}")

        try:
            found_watch_file = self._watch_file_ok()
        except OSError as e:
            self.logger.error(f"failed to check watch file: {e}")
            self.sensor_service.dispatch(
                trigger="gmc_norr_analysis.notification_email",
                payload={
                    "to": self.config["notification_email"],
                    "subject": "[TumorEvolutionSensor] Failed to "
                        "check watch file",
                    "message": "Failed to check watch file: %s" % e
                }
            )
            self._increase_poll_interval()
            return

        if not found_watch_file:
            self.logger.warning("watch file not found, creating it")
            try:
                self._reset_watch_file()
                self.set_poll_interval(self._original_poll_interval)
            except FileNotFoundError as e:
                self.logger.error(f"failed to create watch file: {e}")
                self.sensor_service.dispatch(
                    trigger="gmc_norr_analysis.notification_email",
                    payload={
                        "to": self.config["notification_email"],
                        "subject": "[TumorEvolutionSensor] Failed to "
                            "create watch file",
                        "message": "Failed to create watch file: %s" % e
                    }
                )
                self._increase_poll_interval()
            return

        n_dispatched = 0

        with open(self.watch_file) as f:
            for line in f:
                if line.startswith("#") or len(line.strip()) == 0:
                    continue
                payload = self._parse_arguments(line)
                self.sensor_service.dispatch(
                    trigger="gmc_norr_analysis.tumor_evolution_request",
                    payload=payload,
                )
                n_dispatched += 1

        if n_dispatched == 0:
            self.logger.debug("watch file empty")
            return

        self.logger.info(f"dispatched {n_dispatched} "
                         f"request{'' if n_dispatched == 1 else 's'}")

        self._reset_watch_file()

    def cleanup(self):
        pass

    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass

    def win2unix(self, path: str):
        """
        Convert a windows path to a unix path.

        This assumes that any windows drive letter has been mounted
        at /mnt/<drive-letter>-Genetik. For example, G: should be
        mounted at /mnt/G-Genetik, K: at /mnt/K-Genetik, and so on.
        """
        unix_path = path.replace("\\", "/")
        winre = re.compile("^([GKV]):")
        if winre.match(unix_path):
            unix_path = winre.sub("/mnt/\\1-Genetik", unix_path)
        return unix_path

    def _parse_arguments(self, arg_string):
        args = arg_string.split()

        if len(args) > 2:
            self.logger.warning("too many arguments, ignoring all but first two")

        excel_file = self.win2unix(args[0])
        sheet = "1"

        if len(args) > 1:
            sheet = args[1]

        return {
            "excel_file": excel_file,
            "sheet": sheet,
        }

    def _reset_watch_file(self):
        with open(self.watch_file, "w") as f:
            f.write(self.watch_file_instructions)
