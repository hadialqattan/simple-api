import os


BASE_URL = "http://" + os.environ["APP_HOST"] + ":" + os.environ["APP_PORT"] + "/configs"
QUERY_URL = "http://" + os.environ["APP_HOST"] + ":" + os.environ["APP_PORT"] + "/search"
