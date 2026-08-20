import json
from st2common.runners.base_action import Action

QC_COLUMN_MAP = {
        "M Aligned reads": {
            "suffix": " M",
            "data_field": "reads_mapped"
            },
        "% Mapped": {
            "suffix": "%",
            "data_field": "reads_mapped_percent"
            },
        "Duplicates [%]": {
            "suffix": "%",
            "data_field": "PERCENT_DUPLICATION"
            },
        "Bases on exon target [%]": {
            "suffix": "%",
            "data_field": "PCT_SELECTED_BASES"
            },
        "Usable bases [%]": {
            "suffix": "%",
            "data_field": "PCT_USABLE_BASES_ON_TARGET"
            },
        "Exon target bases over 100X [%]": {
            "suffix": "%",
            "data_field": "PCT_TARGET_BASES_100X"
            },
        "Exon target bases over 500X [%]": {
            "suffix": "%",
            "data_field": "PCT_TARGET_BASES_500X"
            },
        "Mean exon target coverage": {
            "suffix": "",
            "data_field": "MEAN_TARGET_COVERAGE"
            },
        "Median insert size": {
            "suffix": "",
            "data_field": "summed_median"
            },
        "contamination": {
            "suffix": "",
            "data_field": "contamination"
            },
        "AT-dropout [%]": {
            "suffix": "%",
            "data_field": "AT_DROPOUT"
            },
        "GC-dropout [%]": {
            "suffix": "%",
            "data_field": "GC_DROPOUT"
            },
        "Target bases with zero coverage [%]": {
            "suffix": "%",
            "data_field": "ZERO_CVG_TARGETS_PCT"
            },
        "FOLD-80": {
            "suffix": "",
            "data_field": "FOLD_80_BASE_PENALTY"
            },
        }

class GetQCRow(Action):
    """
    Action that outputs qc row for sample based on a multiqc_data.json file
    """
    def run(self, multiqc_data_file: str, sample_id: str, existing_header: bool = True):

        try:
            with open(multiqc_data_file) as f:
                multiqc_data = json.load(f)

            general_stats = multiqc_data["report_general_stats_data"]

            sample_key = f"{sample_id}_T"
            qc_row = ""

            if not existing_header:
                qc_row += "sample_id\t" + "\t".join(QC_COLUMN_MAP.keys()) + "\n"

            qc_row += sample_id + "\t"

            qc_values = []

            for column_name, data_spec in QC_COLUMN_MAP.items():
                data_field = data_spec["data_field"]
                column_value = None

                for data_dict in general_stats:
                    sample_qc_data = data_dict.get(sample_key)
                    if sample_qc_data is not None and sample_qc_data.get(data_field) is not None:
                        column_value=sample_qc_data[data_field]
                        break
                if column_value is None:
                    raise ValueError(f"No entry for {data_field} in {multiqc_data_file}")
                qc_values.append(str(column_value) + data_spec["suffix"])
            
            qc_row += "\t".join(qc_values)

            return True, qc_row

        except Exception as exc:
            return False, str(exc) 
