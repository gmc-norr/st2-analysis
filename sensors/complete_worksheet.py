import os
import shutil
from pathlib import Path
from st2common import log as logging
from st2reactor.sensor.base import PollingSensor

LOG = logging.getLogger(__name__)


class CompleteWorksheetSensor(PollingSensor):
    def __init__(self, sensor_service, config=None, poll_interval=60):
        super(CompleteWorksheetSensor, self).__init__(
            sensor_service, config, poll_interval
        )
        self._watched_directory = self.config.get("log_directory")

    def setup(self):
        pass

    def poll(self):
        """
        Poll the file system for new run directories
        """
        automation_dirs = self.check_ongoing_worksheets()
        if automation_dirs is not None:
            for dir in automation_dirs:
                started_samples, completed_samples, failed_samples = self.samples_from_logfiles(dir)
                if len(started_samples) == 0:
                    continue
                if len(completed_samples) + len(failed_samples) == len(started_samples):

                    pipeline = dir.split("/")[-1]
                    LOG.info(f"dispatching trigger gmc_norr_analysis.complete_worksheet\n"
                             f"completed_samples: {completed_samples}\n"
                             f"failed_samples: {failed_samples}\n"
                             f"pipeline: {pipeline}"
                             )
                    self.sensor_service.dispatch(
                        "gmc_norr_analysis.complete_worksheet",
                        {"completed_samples": completed_samples,
                         "failed_samples": failed_samples,
                         "pipeline": pipeline}
                         )
                    shutil.move(dir, self._watched_directory + "/complete ")

    def samples_from_logfiles(self, dir):
        """
        Check for new run directories within the watched directories.

        :param registered_rundirs: Existing run directories
        :type registered_rundirs: dict
        """
        failed_samples = []
        completed_samples = []
        try:
            with open(dir + "/start") as file:
                sample_lines = file.readlines()
            started_samples = [sample_line.split(" ")[0] for sample_line in sample_lines]
        except FileNotFoundError:
            started_samples = []
        try:
            with open(dir + "/end") as file:
                sample_lines = file.readlines()
            for sample_line in sample_lines:
                sample, succeeded = sample_line.split(" ")
                if succeeded.strip() == "true":
                    completed_samples.append(sample)
                else:
                    failed_samples.append(sample)
        except FileNotFoundError:
            started_samples = []
        return started_samples, completed_samples, failed_samples

    def check_ongoing_worksheets(self):
        dirs = set()

        LOG.debug(f"checking watch directory: {self._watched_directory}")
        if not os.path.exists(self._watched_directory):
            LOG.error(f"directory {self._watched_directory} does not exist")
            return
        root, rundirnames, _ = next(os.walk(self._watched_directory))
        for run_dir_name in rundirnames:
            if run_dir_name == "complete":
                continue
            dir_path = Path(root) / str(run_dir_name)
            root2, pipeline_dir_names, _ = next(os.walk(dir_path))
            for pipeline_dir_name in pipeline_dir_names:
                log_dir = Path(root2) / str(pipeline_dir_name)
                dirs.add(str(log_dir))
        return dirs

    def cleanup(self):
        pass

    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass
