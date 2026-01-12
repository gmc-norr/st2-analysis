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
- `plumber.config_repo`: The URL to the GMC-Norr config-repo that contains the pipeline settings corresponding to the TestProfiles from iGene

Furthermore, the following parameters needs to be defined in the datastore service:
- `notification_email`: The email address where notifications will be sent

## Actions

ref                                               | description
--------------------------------------------------|------------------------------------------
gmc_norr_analysis.generate_tumor_evolution_report | Generate a tumor evolution report from an Excel file
gmc_norr_analysis.write_file                      | Write a text string to a file
gmc_norr_analysis.make_case_id                    | Make a case id of random words and a hash of sample ids
gmc_norr_analysis.make_raredisease_samplesheet    | Make a samplesheet for the nf-core/raredisease pipeline
gmc_norr_analysis.get_plumber_arguments           | From a TestProfile get which pipeline, versions and configs to run plumber with


## Workflows

ref                                               | description
--------------------------------------------------|------------------------------------------
gmc_norr_analysis.tumor_evolution                 | Generate a tumor evolution report
gmc_norr_analysis.start_analysis                  | Start the plumber_sample_analyis workflow for all samples belonging to a sequencing run
gmc_norr_analysis.plumber_sample_analyis          | Run an analysis with plumber for a sample

## Rules

ref                                               | description
--------------------------------------------------|---------------------------------
gmc_norr_analysis.generate_tumor_evolution_report | Generate tumor evolution report
gmc_norr_analysis.send_notification_email         | Send a notification email
gmc_norr_analyis.plumber_webhook_end_email        | Trigger the notification_email trigger when receiving a plumber webhook of messagetype "end"
gmc_norr_analysis.start_analysis                  | Start the start_analysis workflow from a cleve.analysis_state_update trigger with state "ready"

## Sensors

ref                                               | description
--------------------------------------------------|---------------------------------
gmc_norr_analysis.TumorEvolutionSensor            | Sensor that detects new requests to generate tumor evolution reports

##Policies

ref                                               | description
--------------------------------------------------|------------------------------------
gmc_norr_analyis.tumor_evolution_report           | Limits the concurrent executions for the tumor evolution report to 1 

# Known issues

None at the moment.
