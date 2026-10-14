from pathlib import Path
from st2common.runners.base_action import Action


def get_rd_output_files(sample_id, case_id):
    output_files = [ 
        'raredisease_results/multiqc/multiqc_report.html',
        f'raredisease_results/peddy/{case_id}.peddy.ped',
        f'raredisease_results/peddy/{case_id}.sex_check.csv',
        f'raredisease_results/peddy/{case_id}.ped_check.csv',
        f'raredisease_results/alignment/{sample_id}_sorted_md.bam',
        f'raredisease_results/qc_bam/{sample_id}_mosdepth.per-base.d4',
        f'raredisease_results/annotate_snv/genome/{sample_id}_rhocallviz_autozyg_chromograph/{sample_id}_rhocallviz_chr*.png',
        f'raredisease_results/qc_bam/{sample_id}_chromographcov/{sample_id}_tidditcov_chr*.png',
        f'raredisease_results/smncopynumbercaller/out/{case_id}_smncopynumbercaller.tsv',
        f'raredisease_results/rank_and_filter/{case_id}_snv_ranked_clinical.vcf.gz',
        f'raredisease_results/rank_and_filter/{case_id}_snv_ranked_research.vcf.gz',
    ]

    return output_files

def get_twist_solid_output_files(sample_id, case_id):
    output_files = [ 
        f'bam_dna/{sample_id}_T.bam',
        f'results/dna/{sample_id}_T/vcf/{sample_id}_T.annotated.exon_only.filter.hard_filter.codon_snv.vcf',
        f"results/dna/{sample_id}_T/cnv/{sample_id}_T.pathology_purecn.cnv.html",
        f"results/dna/{sample_id}_T/biomarker/{sample_id}_T.TMB.txt",
        f"results/dna/{sample_id}_T/biomarker/{sample_id}_T.pathology_purecn.scarhrd_cnvkit_score.txt",
        f"results/dna/{sample_id}_T/biomarker/{sample_id}_T.msisensor_pro.filtered.score.tsv",
        f"results/dna/{sample_id}_T/qc/{sample_id}_T.coverage_and_mutations.tsv",
        f"results/dna/{sample_id}_T/{sample_id}_T.general_report.html"
    ]

    return output_files


def touch_file(file_path):
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.touch()

class MockStartPlumber(Action):
    def run(self, pipeline, workdir, sample_id, case_id):
        if pipeline == "nf-core/raredisease":
            output_files = get_rd_output_files(sample_id, case_id)
        elif pipeline == "genomic-medicine-sweden/Twist_Solid":
            output_files = get_twist_solid_output_files(sample_id, case_id, complete)
        elif pipeline == "gmc-norr/scout-annotation":
            output_files = get_scout_annotation_output_files(sample_id, case_id)
        else:
            return (False, "unsupported pipeline")
        
        for output_file in output_files:
            file_path = Path(workdir + '/' + output_file)
            touch_file(file_path)

        return (True, f"touched files {output_files}, in {workdir}")

