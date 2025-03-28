from argparse import Namespace
from pathlib import Path

from json2any.project.Json2AnyDescriptor import Json2AnyDescriptor, JSON2ANY_SCHEMA_VERSION
from json2any.project.schema_utils import dump_schema


def cmd_dump_schema_setup(subparsers):
    parser = subparsers.add_parser('dump-rds', aliases=['rds'], help='Generate RDS JSON schema to file')
    parser.add_argument('--schema_file', help='file to write schema to ', type=Path)

    parser.set_defaults(func=cmd_dump_schema_execute)


def cmd_dump_schema_execute(args: Namespace):
    schema_d = {
        '$id': f'https://gitlab.com/maciej.matuszak/json2any/rds_v{JSON2ANY_SCHEMA_VERSION}',
        'title': 'json2any Runs description schema',
        'description': 'Describes how the templates and data are put together to generate output'
    }

    schema_file = args.schema_file

    if schema_file is None:
        schema_file = Path(__file__).parent.parent / 'resources' / f'rds.schema_v{JSON2ANY_SCHEMA_VERSION}.json'

    dump_schema(Json2AnyDescriptor, schema_file, schema_d)
