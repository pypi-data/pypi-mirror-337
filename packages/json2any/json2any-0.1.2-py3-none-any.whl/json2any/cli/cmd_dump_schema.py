import json
from argparse import Namespace
from pathlib import Path

from marshmallow_dataclass import class_schema
from marshmallow_jsonschema import JSONSchema

from json2any.project.Json2AnyDescriptor import Json2AnyDescriptor, JSON2ANY_SCHEMA_VERSION


def cmd_dump_schema_setup(subparsers):
    parser = subparsers.add_parser('dump-rds', aliases=['rds'], help='Generate RDS JSON schema to file')
    parser.add_argument('--schema_file', help='file to write schema to ', type=Path)

    parser.set_defaults(func=cmd_dump_schema_execute)


def cmd_dump_schema_execute(args: Namespace):
    schema = class_schema(Json2AnyDescriptor)()

    json_schema = JSONSchema()

    schema_d = json_schema.dump(schema)
    schema_d['$id'] = f'https://gitlab.com/maciej.matuszak/json2any/rds_v{JSON2ANY_SCHEMA_VERSION}'
    schema_d['title'] = 'json2any Runs description schema'
    schema_d['description'] = 'Describes how the templates and data are put together to generate output'

    schema_file = args.schema_file

    if schema_file is None:
        schema_file = Path(__file__).parent.parent / 'resources' / f'rds.schema_v{JSON2ANY_SCHEMA_VERSION}.json'

    with schema_file.open('w') as file:
        json.dump(schema_d, file, indent=4)
