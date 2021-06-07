from os import getenv

port = getenv("PORT") or "5000"

bind = f"0.0.0.0:{port}"
workers = 4
threads = 4
timeout = 120
