from NeoVintageous.lib import nvim
from NeoVintageous.lib.vi.keys import seq_to_command
from NeoVintageous.lib.vi.keys import to_bare_command_name
from NeoVintageous.lib.vi.keys import KeySequenceTokenizer
from NeoVintageous.lib.vi.utils import modes
from NeoVintageous.lib.vi.cmd_base import cmd_types
from NeoVintageous.lib.vi import variables


_logger = nvim.get_logger(__name__)


_mappings = {
    modes.INSERT: {},
    modes.NORMAL: {},
    modes.VISUAL: {},
    modes.VISUAL_LINE: {},
    modes.OPERATOR_PENDING: {},
    modes.VISUAL_BLOCK: {},
    modes.SELECT: {},
}


class mapping_status:
    INCOMPLETE = 1
    COMPLETE = 2


class Mapping(object):
    def __init__(self, head, mapping, tail, status):
        self.mapping = mapping
        self.head = head
        self.tail = tail
        self.status = status

    @property
    def sequence(self):
        try:
            return self.head + self.tail
        except TypeError:
            raise ValueError('no mapping found')


class Mappings(object):
    def __init__(self, state):
        self.state = state

    def _get_mapped_seqs(self, mode):
        return sorted(_mappings[mode].keys())

    def _find_partial_match(self, mode, seq):
        return list(x for x in self._get_mapped_seqs(mode) if x.startswith(seq))

    def _find_full_match(self, mode, seq):
        partials = self._find_partial_match(mode, seq)
        try:
            _logger.debug('check partials %s for %s', partials, seq)
            name = list(x for x in partials if x == seq)[0]
            # FIXME: Possibly related to #613. We're not returning the view's current mode

            return (name, _mappings[mode][name])
        except IndexError:
            return (None, None)

    def expand(self, seq):
        pass

    def expand_first(self, seq):
        head = ''

        keys, mapped_to = self._find_full_match(self.state.mode, seq)
        if keys:
            _logger.debug('found full command \'%s\' -> \'%s\'', keys, mapped_to)
            return Mapping(seq, mapped_to['name'], seq[len(keys):], mapping_status.COMPLETE)

        for key in KeySequenceTokenizer(seq).iter_tokenize():
            head += key
            keys, mapped_to = self._find_full_match(self.state.mode, head)
            if keys:
                _logger.debug('found full command \'%s\' -> \'%s\'', keys, mapped_to)
                return Mapping(head, mapped_to['name'], seq[len(head):], mapping_status.COMPLETE)
            else:
                break

        if self._find_partial_match(self.state.mode, seq):
            _logger.debug('found partial command \'%s\'', seq)
            return Mapping(seq, '', '', mapping_status.INCOMPLETE)

        return None

    # XXX: Provisional. Get rid of this as soon as possible.
    def can_be_long_user_mapping(self, key):
        full_match = self._find_full_match(self.state.mode, key)
        partial_matches = self._find_partial_match(self.state.mode, key)
        if partial_matches:
            _logger.debug('found user mapping \'%s\' -> %s', key, partial_matches)

            return (True, full_match[0])

        _logger.debug('user mapping not found \'%s\'', key)

        return (False, True)

    # XXX: Provisional. Get rid of this as soon as possible.
    def incomplete_user_mapping(self):
        (maybe_mapping, complete) = self.can_be_long_user_mapping(self.state.partial_sequence)
        if maybe_mapping and not complete:
            _logger.debug('\'%s\'', self.state.partial_sequence)

            return True

    def resolve(self, sequence=None, mode=None, check_user_mappings=True):
        """
        Look at the current global state and return the command mapped to the available sequence.

        It may be a 'missing' command.

        @sequence
            If a @sequence is passed, it is used instead of the global state's.
            This is necessary for some commands that aren't name spaces but act
            as them (for example, ys from the surround plugin).
        @mode
            If different than `None`, it will be used instead of the global
            state's. This is necessary when we are in operator pending mode
            and we receive a new action. By combining the existing action's
            name with name of the action just received we could find a new
            action.

            For example, this is the case of g~~.
        """
        # we usually need to look at the partial sequence, but some commands do weird things,
        # like ys, which isn't a namespace but behaves as such sometimes.
        seq = sequence or self.state.partial_sequence
        seq = to_bare_command_name(seq)

        # TODO: Use same structure as in mappings (nested dicst).
        command = None
        if check_user_mappings:
            _logger.debug('check user mappings')
            # TODO: We should be able to force a mode here too as, below.
            command = self.expand_first(seq)

        if command:
            _logger.debug('\'%s\' equals command \'%s\'', seq, command)
            return command
            # return {'name': command.mapping, 'type': cmd_types.USER}
        else:
            _logger.debug('look up command for seq >>>%s<<<', seq)
            command = seq_to_command(self.state, seq, mode=mode)
            _logger.debug('got command \'%s\'', command)
            return command

    def add(self, mode, new, target):
        new = variables.expand_keys(new)
        _mappings[mode][new] = {'name': target, 'type': cmd_types.USER}

    def remove(self, mode, new):
        try:
            del _mappings[mode][new]
        except KeyError:
            raise KeyError('mapping not found')

    def clear(self):
        _mappings[modes.NORMAL] = {}
        _mappings[modes.VISUAL] = {}
        _mappings[modes.VISUAL_LINE] = {}
        _mappings[modes.VISUAL_BLOCK] = {}
        _mappings[modes.OPERATOR_PENDING] = {}
