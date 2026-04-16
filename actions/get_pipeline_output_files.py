from st2common.runners.base_action import Action


def get_rd_output_files(sample_id, case_id):
    output_files = [
        {'path': 'raredisease_results/multiqc/multiqc_report.html',
         'level': 'case', 'type': 'html', 'parent_id': sample_id},
        {'path': f'raredisease_results/peddy/{case_id}.peddy.ped',
         'level': 'case', 'type': 'text', 'parent_id': sample_id},
        {'path': f'raredisease_results/peddy/{case_id}.sex_check.csv',
         'level': 'case', 'type': 'text', 'parent_id': sample_id},
        {'path': f'raredisease_results/peddy/{case_id}.ped_check.csv',
         'level': 'case', 'type': 'text', 'parent_id': sample_id},
        {'path': f'raredisease_results/alignment/{sample_id}_sorted_md.bam',
         'level': 'sample', 'type': 'bam', 'parent_id': sample_id},
        {'path': f'raredisease_results/qc_bam/{sample_id}_mosdepth.per-base.d4',
         'level': 'sample', 'type': 'd4', 'parent_id': sample_id},
        {'path': 'raredisease_results/annotate_snv/genome/' +
         f'{sample_id}_rhocallviz_autozyg_chromograph/{sample_id}_rhocallviz_chr*.png',
         'level': 'sample', 'type': 'png', 'parent_id': sample_id},
        {'path': f'raredisease_results/qc_bam/{sample_id}_chromographcov/'
         + f'{sample_id}_tidditcov_chr*.png',
         'level': 'sample', 'type': 'png', 'parent_id': sample_id},
        {'path': f'raredisease_results/smncopynumbercaller/out/{case_id}_smncopynumbercaller.tsv',
         'level': 'case', 'type': 'text', 'parent_id': sample_id},
        {'path': f'raredisease_results/rank_and_filter/{case_id}_snv_ranked_clinical.vcf.gz',
         'level': 'case', 'type': 'vcf_snv', 'parent_id': sample_id},
        {'path': f'raredisease_results/rank_and_filter/{case_id}_snv_ranked_research.vcf.gz',
         'level': 'case', 'type': 'vcf_snv', 'parent_id': sample_id}
         ]
    return output_files


class GetPipelineOutputFiles(Action):
    def run(self, pipeline, sample_id, case_id):
        if pipeline == "nf-core-raredisease":
            output_files = get_rd_output_files(sample_id, case_id)
        else:
            return (False, "unsupported pipeline")
        return (True,  output_files)
