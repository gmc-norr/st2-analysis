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
- `notification_email`: An array of email addresses where notifications will be sent

## Actions

ref                                               | description
--------------------------------------------------|------------------------------------------
gmc_norr_analysis.generate_tumor_evolution_report | Generate a tumor evolution report from an Excel file
gmc_norr_analysis.tumor_evolution                 | Workflow for generating a tumor evolution report
gmc_norr_analysis.write_file                      | Write a text string to a file

## Rules

ref                                               | description
--------------------------------------------------|---------------------------------
gmc_norr_analysis.generate_tumor_evolution_report | Generate tumor evolution report
gmc_norr_analysis.send_notification_email         | Send a notification email

## Sensors

ref                                               | description
--------------------------------------------------|---------------------------------
gmc_norr_analysis.TumorEvolutionSensor            | Sensor that detects new requests to generate tumor evolution reports

# Known issues

None at the moment.
