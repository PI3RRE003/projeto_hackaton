from functools import wraps
from app.extensions import db  # sua instância do SQLAlchemy()

def transactional(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)  # roda a função
            db.session.commit()             # salva no banco se deu certo
            return result
        except Exception as e:
            db.session.rollback()           # desfaz mudanças se deu erro
            raise e
    return wrapper
