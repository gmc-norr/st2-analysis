import os
import yaml
import requests
from st2common.runners.base_action import Action

supported_applications = ["NfCoreRareDisease"]


def get_supported_analysis(test_analyses):
    for analysis in test_analyses:
        if analysis["ApplicationProfileName"] in supported_applications:
            return analysis["ApplicationProfileName"], analysis["ApplicationProfileVersion"]
    return None, None


class GetPlumberArgumentsAction(Action):
    def run(self, config_path, test_profile):
        test_profile_path = os.path.join(config_path, "test-profile-config/test_profiles/",
                                         f"{test_profile}.yaml")
        r = requests.get(test_profile_path)
        if not r.status_code == 200:
            return (False,
                    f"Request for TestProfile file {test_profile_path} failed, " +
                    f"status={r.status_code}")
        test_config = yaml.safe_load(r.text)
        test_analyses = test_config.get("TestApplicationProfiles", {}
                                        ).get("DownstreamAnalysis")
        if test_analyses is None:
            return (False, "Error: DownstreamAnalysis not found")
        else:
            app_profile, app_profile_v = get_supported_analysis(test_analyses)

        if app_profile is None:
            return (False, "Error: Unsupported DownstreamAnalysis")

        app_profile_path = os.path.join(config_path, "test-profile-config/application_profiles/",
                                        f"{app_profile}.yaml")
        r = requests.get(app_profile_path)
        if not r.status_code == 200:
            return (False,
                    f"Request for ApplicationProfile file {app_profile_path} failed, " +
                    f"status={r.status_code}")
        app_config = yaml.safe_load(r.text)

        if app_config["ApplicationProfileVersion"] != app_profile_v:
            return (False, "Error: ApplicationProfileVersions don't match.")

        pipeline_dict = {"PipelineSystem": app_config["ApplicationType"],
                         "Pipeline": app_config["ApplicationName"]
                         }
        pipeline_dict.update(app_config["Settings"])

        return (True, pipeline_dict)
