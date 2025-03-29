"""Handle /presence."""
import prompt_toolkit as pt

from ..config import baseConf
from ..conversation import Conversation
from ..OwegaSession import OwegaSession as ps
from ..utils import info_print
from ..colors import clrtxt
from ..constants import OWEGA_DEFAULT_PRESENCE_PENALTY as ODPP


# change presence penalty
def handle_presence(
    temp_file: str,
    messages: Conversation,
    given: str = "",
    temp_is_temp: bool = False,
    silent: bool = False
) -> Conversation:
    f"""Handle /presence.

    Command description:
        Sets the presence penalty (0.0 - 2.0, defaults {ODPP}).

    Usage:
        /presence [presence]
    """
    # removes linter warning about unused arguments
    if temp_file:
        pass
    if temp_is_temp:
        pass
    given = given.strip()
    try:
        new_presence_penalty = float(given)
    except ValueError:
        if not silent:
            info_print(
                'Current presence penalty: '
                + f'{baseConf.get("presence_penalty", ODPP)}')
            info_print(
                f'New presence penalty value (0.0 - 2.0, defaults {ODPP})')
        try:
            if ps['float'] is not None:
                new_presence_penalty = ps['float'].prompt(pt.ANSI(
                    '\n' + clrtxt("magenta", " presence penalty ") + ': '
                )).strip()
            else:
                new_presence_penalty = input(
                    '\n' + clrtxt("magenta", " presence penalty ") + ': '
                ).strip()
        except (ValueError, KeyboardInterrupt, EOFError):
            if not silent:
                info_print("Invalid presence penalty.")
            return messages
    baseConf["presence_penalty"] = float(new_presence_penalty)
    nv = baseConf.get('presence_penalty', ODPP)
    if nv > 2.0:
        if not silent:
            info_print('Penalty too high, capping to 2.0')
        baseConf["presence_penalty"] = 2.0
    if nv < 0.0:
        if not silent:
            info_print('Penalty too low, capping to 0.0')
        baseConf["presence_penalty"] = 0.0
    if not silent:
        info_print(
            'Set presence penalty to '
            + f'{baseConf.get("presence_penalty", {ODPP})}')
    return messages


item_presence = {
    "fun": handle_presence,
    "help": f"sets the presence penalty (0.0 - 2.0, defaults {ODPP})",
    "commands": ["presence"],
}
