from pathlib import Path

from st2common.runners.base_action import Action


class CheckTumorEvolutionRequest(Action):
    def __init__(self, config):
        super().__init__(config)
        self._excel_file = None
        self._sheet = None

    def run(self, watch_file):
        watch_file = Path(watch_file)

        if not watch_file.exists():
            return (False, self._result(message="watch file not found"))

        with open(watch_file) as f:
            # Only consider the last line, and ignore comments and empty lines
            last_line = None
            for line in f:
                if not line.startswith("#") and len(line.strip()) > 0:
                    last_line = line
                pass

        if not last_line or len(last_line.strip()) == 0:
            return (False, self._result(message="watch file empty"))

        return self._parse_arguments(last_line)

    def _parse_arguments(self, arg_string):
        args = arg_string.split()

        if len(args) > 2:
            return (False, self._result(error="too many arguments"))

        self._excel_file = args[0]
        self._sheet = "1"

        if len(args) > 1:
            self._sheet = args[1]

        return (True, self._result())

    def _result(self, message=None, error=None):
        return {
            "message": message,
            "error": error,
            "excel_file": self._excel_file,
            "sheet": self._sheet,
        }
