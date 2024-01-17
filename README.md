# StackStorm pack for GMC Norr

## Installation

```bash
st2 pack install https://github.com/gmc-norr/st2-gmc-norr.git
st2 pack config gmc_norr
```

The config parameters that need to be defined are:

- `tumor_evolution.output_directory`: The directory where the evolution reports will be saved.
- `tumor_evolution.watch_file`: The path to the file that will be watched for new requests to generate reports.
- `tumor_evolution.version`: The version of the tumor-evolution script to be used.

## Actions

ref                                      | description
-----------------------------------------|------------------------------------------
gmc_norr.generate_tumor_evolution_report | Generate a tumor evolution report from an Excel file
gmc_norr.tumor_evolution                 | Workflow for generating a tumor evolution report
gmc_norr.write_file                      | Write a text string to a file

## Triggers

ref                                      | description
-----------------------------------------|------------------------------------------
gmc_norr.copy_complete                   | Triggers when a new copycomplete file is found

## Rules

ref                                      | description
-----------------------------------------|---------------------------------
gmc_norr.generate_tumor_evolution_report | Generate tumor evolution report

## Sensors

ref                                      | description
-----------------------------------------|---------------------------------
gmc_norr.TumorEvolutionSensor            | Sensor that detects new requests to generate tumor evolution reports
gmc_norr.RunDirectorySensor              | Polling sensor that emits triggers for subdirectories within `config.run_directories` when their state change, e.g. a CopyComplete.txt file is found.

# Known issues

- If a quoted string is entered in the tumor evolution watch file, it will not find the file.
