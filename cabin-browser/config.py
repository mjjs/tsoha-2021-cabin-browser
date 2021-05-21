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


DATABASE_URL = ensure_env_var("DATABASE_URL")
FLASK_SECRET_KEY = ensure_env_var("FLASK_SECRET_KEY")
ENVIRONMENT= env_var_or_default("ENVIRONMENT", "DEV")
UPLOAD_FOLDER = path.join(getcwd(), env_var_or_default("UPLOAD_FOLDER", "static"))
PORT = env_var_or_default("PORT", "5000")
