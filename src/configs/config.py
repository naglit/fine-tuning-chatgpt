from src.pyutil.util import file_query_repository as repo
from src.pyutil.util import datetime_util as du

def get_config_file_path():
    dirpath = repo.get_current_dir()
    path = repo.path_join(dirpath, "src", "configs", "config.json")
    print(f"Read the config file: {path}")
    return path