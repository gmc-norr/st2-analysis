from st2common.runners.base_action import Action


def get_rd_input_files(sample_id, analysis_id, fastq_files):
    input_files = []
    for file in fastq_files["R1"] + fastq_files["R2"]:
        input_files.append({'analysis_id': analysis_id, 'name':  file.split('/')[-1],
                            'level': 'sample', 'type': 'fastq', 'parent_id': sample_id})
    return input_files


class GetPipelineInputFilesAction(Action):
    def run(self, pipeline, fastq_files, analysis_ids, sample_id):
        if len(fastq_files[sample_id]["R1"]) != len(fastq_files[sample_id]["R2"]):
            return (False, "The number of R1 and R2 fastq files don't match")
        if len(fastq_files[sample_id]["R1"]) < 1:
            return (False, "No fastq files received")
        if pipeline == "nf-core/raredisease":
            input_files = get_rd_input_files(sample_id, analysis_ids[sample_id],
                                             fastq_files[sample_id])
        else:
            return (False, f"Pipeline not supported: {pipeline}")
        return (True, input_files)
