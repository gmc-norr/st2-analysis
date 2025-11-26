import yaml

from st2common.runners.base_action import Action


class GetPlumberArgumentsAction(Action):
    def run(self, config_file, test_profile):
        with open(config_file, "r") as ymlfile:
                config = yaml.safe_load(ymlfile)
        test_analysis = config.get("Methods", {}
                                   ).get(test_profile, {}
                                         ).get("Analysis", {})
        return (True, test_analysis)