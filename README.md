# StackStorm pack for GMC Norr

## Installation

```bash
st2 pack install https://github.com/gmc-norr/st2-gmc-norr.git
st2 pack config gmc_norr
```

The config parameters that need to be defined are:

- `tumor_evolution.output_directory`: The directory where the evolution reports will be saved.
- `tumor_evolution.watch_file`: The path to the file that will be watched for new requests to generate reports.

## Actions

ref                                      | description
-----------------------------------------|------------------------------------------
gmc_norr.check_tumor_evolution_request   | Check if there is a request for generating a tumor evolution report
gmc_norr.generate_tumor_evolution_report | Generate a tumor evolution report from an Excel file
gmc_norr.parse_arguments                 | Parse command line arguments from a string
gmc_norr.rm                              | Remove files
gmc_norr.truncate_file                   | Truncate a file
gmc_norr.tumor_evolution                 | Workflow for generating a tumor evolution report
gmc_norr.write_file                      | Write a text string to a file

## Rules

ref                                      | description
-----------------------------------------|---------------------------------
gmc_norr.generate_tumor_evolution_report | Generate tumor evolution report
