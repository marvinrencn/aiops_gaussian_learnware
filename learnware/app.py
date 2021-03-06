# import contextlib
# todo: @me 实现migrate，利用alembic
# engine = create_engine('mysql+mysqlconnector://root:root@localhost:3306/giraffe', pool_recycle=3600)
# Session = sessionmaker(bind=engine)
#
#
# @contextlib.contextmanager
# def get_session():
#     s = Session()
#     try:
#         yield s
#         s.commit()
#     except Exception as e:
#         s.rollback()
#         raise e
#     finally:
#         s.close()
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

# extensions
bootstrap = Bootstrap()
_db = SQLAlchemy()


# create app function
def create_app(testing=False):
    app = Flask(__name__)
    app.config.from_object("learnware.config")

    if testing is True:
        app.config["TESTING"] = True

    bootstrap.init_app(app)
    _db.init_app(app)

    return app
