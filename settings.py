from pathlib import Path, PosixPath
from pydantic import ConfigDict, model_validator
from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):

    token: str

    project_path: PosixPath = Path.cwd()
    file_dir: str
    users_filename: str
    db_name: str
    base_url: str

    grant_type: str
    scope: str
    admin_email: str
    password: str
    client_id: str
    client_secret: str

    @property
    def db_path(self):
        return self.project_path / self.db_name

    @property
    def user_list_path(self):
        return self.project_path / self.users_filename

    def get_year_path(self, year: int):
        return  self.project_path / self.file_dir / str(year)


settings = AppSettings()