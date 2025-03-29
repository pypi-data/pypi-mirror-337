"""Handle /frequency."""
import prompt_toolkit as pt

from ..config import baseConf
from ..conversation import Conversation
from ..OwegaSession import OwegaSession as ps
from ..utils import info_print
from ..colors import clrtxt
from ..constants import OWEGA_DEFAULT_FREQUENCY_PENALTY as ODFP


# change frequency penalty
def handle_frequency(
    temp_file: str,
    messages: Conversation,
    given: str = "",
    temp_is_temp: bool = False,
    silent: bool = False
) -> Conversation:
    f"""Handle /frequency.

    Command description:
        Sets the frequency penalty (0.0 - 2.0, defaults {ODFP}).

    Usage:
        /frequency [frequency]
    """
    # removes linter warning about unused arguments
    if temp_file:
        pass
    if temp_is_temp:
        pass
    given = given.strip()
    try:
        new_frequency_penalty = float(given)
    except ValueError:
        if not silent:
            info_print(
                'Current frequency penalty: '
                + f'{baseConf.get("frequency_penalty", ODFP)}')
            info_print(
                f'New frequency penalty value (0.0 - 2.0, defaults {ODFP})')
        try:
            if ps['float'] is not None:
                new_frequency_penalty = ps['float'].prompt(pt.ANSI(
                    '\n' + clrtxt("magenta", " frequency penalty ") + ': '
                )).strip()
            else:
                new_frequency_penalty = input(
                    '\n' + clrtxt("magenta", " frequency penalty ") + ': '
                ).strip()
        except (ValueError, KeyboardInterrupt, EOFError):
            if not silent:
                info_print("Invalid frequency penalty.")
            return messages
    baseConf["frequency_penalty"] = float(new_frequency_penalty)
    nv = baseConf.get('frequency_penalty', ODFP)
    if nv > 2.0:
        if not silent:
            info_print('Penalty too high, capping to 2.0')
        baseConf["frequency_penalty"] = 2.0
    if nv < 0.0:
        if not silent:
            info_print('Penalty too low, capping to 0.0')
        baseConf["frequency_penalty"] = 0.0
    if not silent:
        info_print(
            'Set frequency penalty to '
            + f'{baseConf.get("frequency_penalty", ODFP)}')
    return messages


item_frequency = {
    "fun": handle_frequency,
    "help": f"sets the frequency penalty (0.0 - 2.0, defaults {ODFP})",
    "commands": ["frequency"],
}
