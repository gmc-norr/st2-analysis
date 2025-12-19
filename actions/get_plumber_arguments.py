import os

import yaml
from st2common.runners.base_action import Action

supported_applications = ["NfCoreRareDisease", "NfCoreRareDiseaseResearch"]

def get_supported_analysis(test_analyses):
    for analysis in test_analyses:
        if analysis["ApplicationProfileName"] in supported_applications:
            return analysis["ApplicationProfileName"], analysis["ApplicationProfileVersion"]
    return None, None


class GetPlumberArgumentsAction(Action):
    def run(self, config_path, test_profile):
        test_profile_file = os.path.join(config_path, "test_profiles/", 
                                         f"{test_profile}.yaml")
        if not os.path.isfile(test_profile_file):
            return (False, f"Error: TestProfile file {test_profile_file} not found")
        with open(test_profile_file, "r") as ymlfile:
            test_config = yaml.safe_load(ymlfile)

        test_analyses = test_config.get("TestApplicationProfiles", {}
                                        ).get("DownstreamAnalysis")
        if test_analyses is None:
             return (False, "Error: DownstreamAnalysis not found")
        else:
             app_profile, app_profile_v = get_supported_analysis(test_analyses)
        
        if app_profile is None:
            return (False, "Error: Unsupported DownstreamAnalysis")

        app_profile_file = os.path.join(config_path, "application_profiles",
                                        f"{app_profile}.yaml")
        if not os.path.isfile(app_profile_file):
            return (False, "Error: ApplicationProfile file not found")

        with open(app_profile_file, "r") as ymlfile:
            app_config = yaml.safe_load(ymlfile)
        if app_config["ApplicationProfileVersion"] != app_profile_v:
            return (False, "Error: ApplicationProfileVersions don't match.")

        pipeline_dict = {"PipelineSystem": app_config["ApplicationType"],
                    "Pipeline": app_config["ApplicationName"],
        }
        pipeline_dict.update(app_config["Settings"])

        return (True, pipeline_dict)
