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
- `plumber.host`: The host to run plumber on.
- `plumber.twist_solid_dir`: The directory where we run the GMS Solid runs from

Furthermore, the following parameters needs to be defined in the datastore service:
- `notification_email`: The email address where notifications will be sent.
- `plumber_api_key`: An API key for plumber webhooks. Should be encrypted.
- `api_url`: The URL to Stackstorm's API. Used in the `plumber_analysis` workflow, to set up plumber's webhooks.

## Actions

ref                                               | description
--------------------------------------------------|------------------------------------------
gmc_norr_analysis.generate_tumor_evolution_report | Generate a tumor evolution report from an Excel file
gmc_norr_analysis.write_file                      | Write a text string to a file
gmc_norr_analysis.make_case_id                    | Make a case id of random words and a hash of sample ids
gmc_norr_analysis.make_raredisease_samplesheet    | Make a samplesheet for the nf-core/raredisease pipeline
gmc_norr_analysis.get_pipeline_output_files       | Get output files for updating an analysis in Cleve
gmc_norr_analysis.get_pipeline_input_files        | Format fastq files for adding an analysis in Cleve
gmc_norr_analysis.get_plumber_arguments           | Translate a iGene TestProfile into a pipeline with versions and config files
gmc_norr_analysis.get_qc_row                      | Get QC data from MultiQC JSON for a sample
## Workflows

ref                                               | description
--------------------------------------------------|------------------------------------------
gmc_norr_analysis.tumor_evolution                 | Generate a tumor evolution report
gmc_norr_analysis.start_plumber_workflows         | For all runs belonging to an analysis, start the get_samples_for_plumber workflow
gmc_norr_analysis.get_samples_for_plumber         | For all samples belonging to a run, start the plumber_analysis workflow
gmc_norr_analysis.plumber_analysis                | Run a downstream analysis with plumber on a sample
gmc_norr_analysis.second_plumber_analysis         | Run an annotation analysis with plumber on a sample
gmc_norr_analysis.prepare_twist_solid             | Symlink fastq files and make GMS Solid input files for a sample
gmc_norr_analysis.write_qc_data                   | Take MultiQC JSON data for a sample and write to a tsv file common for the run

## Workflows

ref                                                 | description
----------------------------------------------------|------------------------------------------
gmc_norr_analysis.tumor_evolution                   | Workflow for generating a tumor evolution report
gmc_norr_analysis.update_complete_plumbler_analysis | Move output files and update the analysis in Cleve

## Rules

ref                                                  | description
-----------------------------------------------------|---------------------------------
gmc_norr_analysis.generate_tumor_evolution_report    | Generate tumor evolution report
gmc_norr_analysis.send_notification_email            | Send a notification email
gmc_norr_analysis.start_plumber_analysis             | Runs start_plumber_workflows for an analysis with state "ready", software BCLConvert and the path includes "Analysis/1"
gmc_norr_analysis.email_plumber_end                  | Trigger send_notification_email when plumber webhook reports a failure
gmc_norr_analysis.update_complete_plumber_analysis   | Trigger workflow of same name if plumber ended successfully, and pipeline isn't GMS Solid
gmc_norr_analysis.update_incomplete_plumber_analysis | Update analysis to incomplete in Cleve if plumber ends unsuccessfully
gmc_norr_analysis.second_plumber_analysis            | Trigger second_plumber_analysis when plumber succesfully finishes a GMS Solid run for a sample


## Sensors

ref                                               | description
--------------------------------------------------|---------------------------------
gmc_norr_analysis.TumorEvolutionSensor            | Sensor that detects new requests to generate tumor evolution reports

## Policies

ref                                                            | description
---------------------------------------------------------------|---------------------------------
gmc_norr_analysis.tumor_evolution.concurrency                  | Limit concurrent executions to 1 at a time and delay the rest
gmc_norr_analysis.update_complete_plumber_analysis.concurrency | Limit concurrent executions to 2 at a time and delay the rest
gmc_norr_analysis.second_plumber_analysis.concurrency          | Limit concurrent executions to 1 at a time and delay the rest
gmc_norr_analysis.write_qc_data.concurrency                    | Limit concurrent executions to 1 at a time and delay the rest

# Known issues

None at the moment.
