from dataclasses import dataclass, field
from typing import List, Optional

from json2any.project.JobDescriptor import JobDescriptor

JSON2ANY_SCHEMA_VERSION = 1

@dataclass
class Json2AnyDescriptor:

    name: str = field(metadata=dict(description="Name of the Generator run - for debugging purposes"))

    template_location: Optional[str] = field(default=None, metadata=dict(
        description='Location of templates - format depends on Template Provider used'))

    template_provider: Optional[str] = field(default='FileSystem',
                                             metadata=dict(description='Template Provider to use'))

    jobs: List[JobDescriptor] = field(default_factory=list,
                                      metadata=dict(description='Job descriptors'))
