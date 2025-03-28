from argparse import Namespace
from typing import Any, Dict

from json2any_plugin.AbstractHelperProvider import AbstractHelperProvider


class CGenHelper:
    def validate_enum_desc(self):
        pass

    def entry_name(self, entry: Dict[str, Any], name: str):
        """
        cenum.entry_name(entry, name)
        :param entry:
        :param name:
        :return:
        """
        key = entry.get('entry_prefix', entry.get('name'))
        key = f'{key}_{name}'

        if entry.get('capitalise', False):
            return key.upper()

        return key

    def enum_name_e(self, name: str):
        return f'{name}_e'

    def enum_name_t(self, name: str):
        return f'{name}_t'

    def format_doco(self, doco: str):
        if not doco:
            return ''
        out = '/**\n'
        for line in doco.splitlines():
            out += f' * {line}\n'
        out += ' */\n'
        return out


class CGenHelperProvider(AbstractHelperProvider):
    def get_helper_object(self) -> Any:
        return CGenHelper()

    def get_helper_ns(self) -> str:
        return 'cenum'

    @property
    def name(self) -> str:
        return 'CGenHelperProvider'

    @property
    def arg_prefix(self) -> str:
        return ''

    @property
    def has_arguments(self) -> bool:
        return False

    def update_arg_parser(self, parser: '_ArgumentGroup') -> None:
        # Unused
        pass

    def process_args(self, args: Namespace) -> bool:
        return True

    def init(self, **kwargs) -> None:
        # Unused
        pass
