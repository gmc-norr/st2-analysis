from wonderwords import RandomWord
from st2common.runners.base_action import Action


class MakeCaseID(Action):
    def run(self):
        word_generator = RandomWord()
        case_id_adj = word_generator.word(include_categories=["adjective"]).strip(
            ).replace("'", "").replace("-", "_").replace(" ", "_")
        case_id_noun = word_generator.word(include_categories=["noun"]).strip(
            ).replace("'", "").replace("-", "_").replace(" ", "_")
        return (True,  f"{case_id_adj}_{case_id_noun}")
