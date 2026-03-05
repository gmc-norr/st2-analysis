import hashlib

from st2common.runners.base_action import Action
from wonderwords import RandomWord


class MakeCaseID(Action):
    def run(self, samples):
        word_generator = RandomWord()

        case_id_adj = word_generator.word(include_categories=["adjective"]).strip()
        case_id_noun = word_generator.word(include_categories=["noun"]).strip()
        case_id = f"{case_id_adj}_{case_id_noun}".replace(
            "'", "").replace("-", "_").replace(" ", "_")

        sample_bytes = bytes(" ".join(samples), "utf-8")
        hash_id = hashlib.md5(sample_bytes).hexdigest()[:8]

        return (True,  case_id + "_" + hash_id)
