from pathlib import Path
from st2reactor.sensor.base import PollingSensor


class TumorEvolutionSensor(PollingSensor):
    def __init__(self, sensor_service, config, poll_interval=60):
        super(TumorEvolutionSensor, self).__init__(sensor_service, config, poll_interval)
        self.logger = self.sensor_service.get_logger(__name__)
        # self.watch_file = Path(self.config["tumor_evolution"]["watch_file"])
        self.watch_file = Path("/home/nima18/tmp/test.txt")
        self.watch_file_instructions = self.config["tumor_evolution"]["watch_file_instructions"]

    def setup(self):
        pass

    def poll(self):
        self.logger.debug(f"looking for requests in {self.watch_file}")

        if not self.watch_file.exists():
            self.logger.warning("watch file not found, creating it")
            self._reset_watch_file()
            return

        n_dispatched = 0

        with open(self.watch_file) as f:
            for line in f:
                if line.startswith("#") or len(line.strip()) == 0:
                    continue
                payload = self._parse_arguments(line)
                self.logger.debug(f"dispatching payload: {payload}")
                self.sensor_service.dispatch(
                    trigger="gmc_norr.tumor_evolution_request",
                    payload=payload,
                )
                n_dispatched += 1

        if n_dispatched == 0:
            self.logger.debug("watch file empty")
            return

        self._reset_watch_file()

    def cleanup(self):
        pass

    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass

    def _parse_arguments(self, arg_string):
        args = arg_string.split()

        if len(args) > 2:
            raise ValueError("too many arguments")

        excel_file = args[0]
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
