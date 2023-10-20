# StackStorm pack for GMC Norr

## Installation

```bash
st2 pack install https://github.com/gmc-norr/st2-gmc-norr.git
st2 pack config gmc_norr
```

There are some config parameters that have to be set for each workflow.

### Tumor evolution

- `tumor_evolution.output_directory`: The directory where the evolution reports will be saved.
- `tumor_evolution.watch_file`: The path to the file that will be watched for new requests to generate reports.
- `tumor_evolution.version`: The version of the tumor-evolution script to be used.

### Archer

- `archer.watch_directory`: The directory to watch for new sequencing runs
- `archer.processed_directory`: The directory where to move the data once it has been processed
- `archer.archer_directory`: The watch directory for Archer Analysis
- `archer.required_samplesheet_columns`: List of required columns in the Data section of the samplesheet
- `archer.samplesheet_data_section`: The name of the relevant data section of the samplesheet

## Actions

ref                                      | description
-----------------------------------------|------------------------------------------
gmc_norr.generate_tumor_evolution_report | Generate a tumor evolution report from an Excel file
gmc_norr.tumor_evolution                 | Workflow for generating a tumor evolution report
gmc_norr.write_file                      | Write a text string to a file
gmc_norr.validate_samplesheet            | Validate samplesheet

## Triggers

ref                                      | description
-----------------------------------------|------------------------------------------
gmc_norr.copy_complete                   | Triggers when a new copycomplete file is found

## Sensors

ref                                      | description
-----------------------------------------|------------------------------------------
gmc_norr.CopyCompleteSensor              | Sensor that emits triggers for
                                         | subdirectories within a
                                         | specific directory where a new
                                         | CopyComplete.txt file is
                                         | written.

## Rules

ref                                      | description
-----------------------------------------|---------------------------------
gmc_norr.generate_tumor_evolution_report | Generate tumor evolution report

## Sensors

ref                                      | description
-----------------------------------------|---------------------------------
gmc_norr.TumorEvolutionSensor            | Sensor that detects new requests to generate tumor evolution reports

# Known issues

- If a quoted string is entered in the tumor evolution watch file, it will not find the file.
