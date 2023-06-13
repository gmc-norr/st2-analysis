from st2common.runners.base_action import Action


class ParseArguments(Action):
    def run(self, arg_string, n_expected=None):
        args = arg_string.split()
        if n_expected is not None:
            assert len(args) == n_expected, \
                f"Expected {n_expected} arguments, got {len(args)}"
        return args
