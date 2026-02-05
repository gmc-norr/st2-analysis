from st2common.runners.base_action import Action


class MakePlumberAnalysisID(Action):
    def run(self, workdir, pipeline, pipeline_version):
        try:
            analysis_id = '_'.join([workdir.split('/')[-3], workdir.split('/')[-1],
                                    pipeline, pipeline_version])
        except IndexError:
            return (False, "workdir didn't have the expected format")
        analysis_id = analysis_id.replace("/", "-").replace(".", "_")
        return (True,  analysis_id)
