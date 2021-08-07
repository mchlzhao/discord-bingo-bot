SUCCESS_EMOJI = '👍'
FAILURE_EMOJI = '👎'
ERROR_EMOJI = '❌'
HIT_EMOJI = '🟢'
UNHIT_EMOJI = '🔴'
SPACER_EMOJI = '▪️'
HIDDEN_EMOJI = '❔'

NUM_COMBOS = 4
COMBO_SIZE = 3


def index_to_char(i):
    return chr(ord('A') + i)


def char_to_index(c):
    return ord(c.upper()) - ord('A')


def char_to_emoji(c):
    return f':regional_indicator_{c.lower()}:'


def index_to_emoji(i):
    return char_to_emoji(index_to_char(i))


def hit_emoji(is_hit):
    return HIT_EMOJI if is_hit else UNHIT_EMOJI
