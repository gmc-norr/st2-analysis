from wonderwords import RandomWord
from st2common.runners.base_action import Action


class MakeCaseID(Action):
    def run(self):
        word_generator = RandomWord()
        case_id_adj = word_generator.word(include_categories=["adjective"]).strip()
        case_id_noun = word_generator.word(include_categories=["noun"]).strip()
        case_id = f"{case_id_adj}_{case_id_noun}".replace(
            "'", "").replace("-", "_").replace(" ", "_")
        return (True,  case_id + "_" + str(hash(case_id))[-4:])
