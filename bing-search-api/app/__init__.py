# make this a real package
from . import schemas, providers  # noqa
try:
    from .main import app  # 方便 uvicorn 用 app:app 形式
except Exception:
    pass
