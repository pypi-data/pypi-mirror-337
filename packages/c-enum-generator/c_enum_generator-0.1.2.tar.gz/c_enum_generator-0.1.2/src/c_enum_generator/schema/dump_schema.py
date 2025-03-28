from pathlib import Path

from json2any.project.schema_utils import dump_schema

from c_enum_generator.schema.CEnumsSchema import CENUM_SCHEMA_VERSION, CEnumsSchema


def main():
    schema_d = {
        '$id': f'https://gitlab.com/maciej.matuszak/c-enum-generator/cenum.schema_v{CENUM_SCHEMA_VERSION}',
        'title': 'C enum generator data schema',
        'description': 'Describes the C enum generator schema'
    }

    schema_file = Path(__file__).parent.parent / 'resources' / f'cenum.schema_v{CENUM_SCHEMA_VERSION}.json'

    dump_schema(CEnumsSchema, schema_file, schema_d)


if __name__ == '__main__':
    main()
