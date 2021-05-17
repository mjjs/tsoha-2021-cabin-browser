from os import getenv, path, getcwd

class EnvironmentalVariableNotFoundError(Exception):
    def __init__(self, env_var):
        super().__init__(f"Environmental variable {env_var} not found")

def ensure_env_var(env_var: str) -> str:
    var = getenv(env_var)
    if var:
        return var

    raise EnvironmentalVariableNotFoundError(env_var)

def env_var_or_default(env_var, default):
    var = getenv(env_var)
    if var:
        return var

    return default


DATABASE_HOST = ensure_env_var("DATABASE_HOST")
DATABASE_USERNAME = ensure_env_var("DATABASE_USERNAME")
DATABASE_PASSWORD = ensure_env_var("DATABASE_PASSWORD")
DATABASE_PORT = ensure_env_var("DATABASE_PORT")
DATABASE_NAME = ensure_env_var("DATABASE_NAME")
FLASK_SECRET_KEY = ensure_env_var("FLASK_SECRET_KEY")
UPLOAD_FOLDER = path.join(getcwd(), env_var_or_default("UPLOAD_FOLDER", "static"))
