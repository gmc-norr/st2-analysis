from st2common.runners.base_action import Action


class GetRDOutputFile(Action):
    def run(self, sample_id, case_id):
        output_files = "[{'path': 'raredisease_results/multiqc/multiqc_report.html', " \
            "'level': 'sample', 'type': 'html', 'parent_id': '" + sample_id + "'}, " \
            "{'path': 'raredisease_results/peddy/" + case_id + ".peddy.ped', " \
            "'level': 'sample', 'type': 'text', 'parent_id': '" + sample_id + "'}, " \
            "{'path': 'raredisease_results/peddy/" + case_id + ".sex_check.csv', " \
            "'level': 'sample', 'type': 'text', 'parent_id': '" + sample_id + "'}, " \
            "{'path': 'raredisease_results/peddy/" + case_id + ".ped_check.csv', " \
            "'level': 'sample', 'type': 'text', 'parent_id': '" + sample_id + "'}, " \
            "{'path': 'raredisease_results/alignment/" + sample_id + "_sorted_md.bam', " \
            "'level': 'sample', 'type': 'bam', 'parent_id': '" + sample_id + "'}, " \
            "{'path': 'raredisease_results/qc_bam/" + sample_id + "_mosdepth.per-base.d4', " \
            "'level': 'sample', 'type': 'd4', 'parent_id': '" + sample_id + "'}, " \
            "{'path': 'raredisease_results/annotate_snv/genome/" + sample_id + \
            "_rhocallviz_autozyg_chromograph/" + sample_id + "_rhocallviz_chr*.png'," \
            "'level': 'sample', 'type': 'png', 'parent_id': '" + sample_id + "'}, " \
            "{'path': 'raredisease_results/qc_bam/" + sample_id + "_chromographcov/" \
            "" + sample_id + "_tidditcov_chr*.png', " \
            "'level': 'sample', 'type': 'png', 'parent_id': '" + sample_id + "'}, " \
            "{'path': 'raredisease_results/smncopynumbercaller/out/" \
            "" + case_id + "_smncopynumbercaller.tsv', " \
            "'level': 'sample', 'type': 'text', 'parent_id': '" + sample_id + "'}, " \
            "{'path': 'raredisease_results/rank_and_filter/" + case_id + "" \
            "_snv_ranked_clinical.vcf.gz', " \
            "'level': 'sample', 'type': 'vcf_snv', 'parent_id': '" + sample_id + "'}, " \
            "{'path': 'raredisease_results/rank_and_filter/" \
            "" + case_id + "_snv_ranked_research.vcf.gz', " \
            "'level': 'sample', 'type': 'vcf_snv', 'parent_id': '" + sample_id + "'},]"
        return (True,  output_files)
