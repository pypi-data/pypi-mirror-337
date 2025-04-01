from dataclasses import dataclass


@dataclass
class job_dto:
    job_id: str
    branch: str
    project_id: str
    project_name: str
    pipeline_id: str
    job_name: str
    tag_id: str
    name: str
    stage: str
    status: str
    web_url: str
    create_time: str
    hexsha: str
