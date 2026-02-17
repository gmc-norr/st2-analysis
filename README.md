# StackStorm pack for GMC Norr downstream analysis

## Installation

```bash
st2 pack install https://github.com/gmc-norr/st2-analysis.git
st2 pack config gmc_norr_analysis
```

The config parameters that need to be defined are:

- `tumor_evolution.output_directory`: The directory where the evolution reports will be saved.
- `tumor_evolution.watch_file`: The path to the file that will be watched for new requests to generate reports.
- `tumor_evolution.version`: The version of the tumor-evolution script to be used.
- `mount_points`: An array of mappings between windows paths and their mount points on the system.
    - Each entry in the array should be an object with two keys: `win` and `unix`. The value for `win` should be a windows path, and `unix` should be the path where the windows path is mounted.
- `plumber.user`: The user to run plumber with
- `plumber.host`: THe host to run plumber on.

Furthermore, the following parameters needs to be defined in the datastore service:
- `notification_email`: The email address where notifications will be sent
- `api_url`: The url to Stackstorm's API (needed for plumber's webhooks)
- `plumber_api_key`: A Stackstorm API key for plumber's webhooks (stored encrypted)

## Actions

ref                                               | description
--------------------------------------------------|------------------------------------------
gmc_norr_analysis.generate_tumor_evolution_report | Generate a tumor evolution report from an Excel file
gmc_norr_analysis.write_file                      | Write a text string to a file


## Workflows

ref                                               | description
--------------------------------------------------|------------------------------------------
gmc_norr_analysis.tumor_evolution                 | Generate a tumor evolution report
gmc_norr_analysis.start_plumber_workflows         | For all runs belonging to an analysis, start the get_samples_for_plumber workflow
gmc_norr_analysis.get_samples_for_plumber         | For all samples belongin to a run, start the plumber_nalysis workflow
gmc_norr_analysis.plumber_analysis                | Run a downstream analysis with plumber on a sample

## Rules

ref                                               | description
--------------------------------------------------|---------------------------------
gmc_norr_analysis.generate_tumor_evolution_report | Generate tumor evolution report
gmc_norr_analysis.send_notification_email         | Send a notification email
gmc_norr_analysis.start_plumber_analysis          |  Runs start_plumber_workflows for an analysis with state "ready" and software BCLConvert

## Sensors

ref                                               | description
--------------------------------------------------|---------------------------------
gmc_norr_analysis.TumorEvolutionSensor            | Sensor that detects new requests to generate tumor evolution reports

# Known issues

None at the moment.
