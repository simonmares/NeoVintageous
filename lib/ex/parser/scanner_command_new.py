from .tokens import TokenEof
from .tokens_base import TOKEN_COMMAND_NEW
from .tokens_base import TokenOfCommand
from NeoVintageous.lib import ex
from NeoVintageous.lib import nvim


plus_plus_translations = {
    'ff': 'fileformat',
    'bin': 'binary',
    'enc': 'fileencoding',
    'nobin': 'nobinary',
}


@ex.command('new', 'new')
class TokenNew(TokenOfCommand):
    def __init__(self, params, *args, **kwargs):
        super().__init__(params, TOKEN_COMMAND_NEW, 'new', *args, **kwargs)
        self.target_command = 'ex_new'


def scan_command_new(state):
    params = {
        '++': None,
        'cmd': None,
    }
    state.skip(' ')
    state.ignore()

    c = state.consume()

    if c == '+':
        state.expect('+')
        state.ignore()
        # TODO: expect_match should work with emit()
        # https://neovim.io/doc/user/editing.html#[++opt]
        m = state.expect_match(
            r'(?:f(?:ile)?f(?:ormat)?|(?:file)?enc(?:oding)?|(?:no)?bin(?:ary)?|bad|edit)(?=\s|$)',
            lambda: nvim.Error(nvim.E_INVALID_ARGUMENT))
        name = m.group(0)
        params['++'] = plus_plus_translations.get(name, name)
        state.ignore()
        raise NotImplementedError(':new not fully implemented')

    m = state.match(r'.+$')
    if m:
        params['cmd'] = m.group(0).strip()
        raise NotImplementedError(':new not fully implemented')

    return None, [TokenNew(params), TokenEof()]
