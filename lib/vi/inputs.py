from collections import namedtuple

from NeoVintageous.lib.vi.utils import input_types
from NeoVintageous.lib.vi import utils


parser_def = namedtuple('parsed_def', 'command interactive_command input_param on_done type')


def get(state, name):
    parser_func = globals().get(name, None)
    if parser_func is None:
        raise ValueError('parser name unknown')
    return parser_func(state)


def one_char(in_):
    """Any input (character) satisfies this parser."""
    in_ = utils.translate_char(in_)
    return len(in_) == 1


def vi_f(state):
    return parser_def(command=one_char,
                      interactive_command=None,
                      input_param=None,
                      on_done=None,
                      type=input_types.INMEDIATE)


def vi_big_f(state):
    return parser_def(command=one_char,
                      interactive_command=None,
                      input_param=None,
                      on_done=None,
                      type=input_types.INMEDIATE)


def vi_big_t(state):
    return parser_def(command=one_char,
                      interactive_command=None,
                      input_param=None,
                      on_done=None,
                      type=input_types.INMEDIATE)


def vi_t(state):
    return parser_def(command=one_char,
                      interactive_command=None,
                      input_param=None,
                      on_done=None,
                      type=input_types.INMEDIATE)


# TODO: rename to "vi_a_text_object".
def vi_inclusive_text_object(state):
    return parser_def(command=one_char,
                      interactive_command=None,
                      input_param=None,
                      on_done=None,
                      type=input_types.INMEDIATE)


def vi_exclusive_text_object(state):
    return parser_def(command=one_char,
                      interactive_command=None,
                      input_param=None,
                      on_done=None,
                      type=input_types.INMEDIATE)


def vi_m(state):
    return parser_def(command=one_char,
                      interactive_command=None,
                      input_param=None,
                      on_done=None,
                      type=input_types.INMEDIATE)


def vi_q(state):
    return parser_def(command=one_char,
                      interactive_command=None,
                      input_param=None,
                      on_done=None,
                      type=input_types.INMEDIATE)


def vi_at(state):
    return parser_def(command=one_char,
                      interactive_command=None,
                      input_param=None,
                      on_done=None,
                      type=input_types.INMEDIATE)


def vi_a_text_object(state):
    return parser_def(command=one_char,
                      interactive_command=None,
                      input_param=None,
                      on_done=None,
                      type=input_types.INMEDIATE)


def vi_i_text_object(state):
    return parser_def(command=one_char,
                      interactive_command=None,
                      input_param=None,
                      on_done=None,
                      type=input_types.INMEDIATE)


def vi_quote(state):
    return parser_def(command=one_char,
                      interactive_command=None,
                      input_param=None,
                      on_done=None,
                      type=input_types.INMEDIATE)


def vi_r(state):
    return parser_def(command=one_char,
                      interactive_command=None,
                      input_param=None,
                      on_done='_vi_r_on_parser_done',
                      type=input_types.INMEDIATE)


def vi_backtick(state):
    return parser_def(command=one_char,
                      interactive_command=None,
                      input_param=None,
                      on_done=None,
                      type=input_types.INMEDIATE)


def vi_left_square_bracket(state):
    return parser_def(command=lambda x: x in '(){}',
                      interactive_command=None,
                      input_param=None,
                      on_done=None,
                      type=input_types.INMEDIATE)


def vi_slash(state):
    """Parse should always be used non-interactively.

    / usually collects its input from an input panel.
    """
    # Any input is valid; we're never satisfied.
    if state.non_interactive:
        return parser_def(command=lambda x: False,
                          interactive_command='_vi_slash',
                          type=input_types.INMEDIATE,
                          on_done='_vi_slash_on_parser_done',
                          input_param='key')
    else:
        return parser_def(command='_vi_slash',
                          interactive_command='_vi_slash',
                          type=input_types.VIA_PANEL,
                          on_done=None,
                          input_param='default')


def vi_question_mark(state):
    """Parser should always be used non-interactively.

    ? usually collects its input from an input panel.
    """
    # Any input is valid; we're never satisfied.
    if state.non_interactive:
        return parser_def(command=lambda x: False,
                          interactive_command='_vi_question_mark',
                          type=input_types.INMEDIATE,
                          on_done='_vi_question_mark_on_parser_done',
                          input_param='key')
    else:
        return parser_def(command='_vi_question_mark',
                          interactive_command='_vi_question_mark',
                          type=input_types.VIA_PANEL,
                          on_done=None,
                          input_param='default')
