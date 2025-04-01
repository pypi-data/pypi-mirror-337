from enum import Enum


class TableColumns(Enum):
    TagNo = 'Tag No'
    TagId = 'Tag Id'
    Project = 'Project'
    Branch = 'Branch'
    SHA = 'SHA'
    Stage = 'Stage'
    StageName = 'Stage Name'
    Status = 'Status'
    PipelineUrl = 'Pipeline Url'
    CreateTime = 'Create Time'
