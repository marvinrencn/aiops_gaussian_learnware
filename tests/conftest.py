import pytest
from sqlalchemy import create_engine

from learnware.app import create_app, _db
from learnware.model.models import DataSource, DataSet, Learnware, DATASOURCE_TYPE_MYSQL, LearnwareModel
import pandas as pd


@pytest.fixture(scope="session")
def app():
    # load_dotenv(".testenv")
    app = create_app(testing=True)
    return app


@pytest.fixture
def db(app):
    _db.app = app

    with app.app_context():
        _db.create_all()

    yield _db

    _db.session.close()
    _db.drop_all()


@pytest.fixture
def learnware_record_1(db):
    db_url = "mysql+mysqlconnector://root:root@localhost:3306/giraffe"

    engine = create_engine(db_url, echo=True)
    df = pd.read_csv("data/machine1933.csv")
    df.to_sql("machine1933", con=engine, if_exists="replace")

    datasource = DataSource(name="mysql测试数据源", type=DATASOURCE_TYPE_MYSQL, url=db_url, notes="测试用数据源")
    dataset = DataSet(name="machine1933", sql="select timestamp, cpu as origin_value from machine1933",
                      datasource=datasource)
    learnware = Learnware(name="学件1", dataset=dataset,
                          module_path="learnware.LearnwareDemo",
                          class_name="LearnwareDemo1",
                          train_settings={
                              "isStandard": True,
                              "n_estimators": 20
                          })

    db.session.add(datasource)
    db.session.add(dataset)
    db.session.add(learnware)
    db.session.commit()

    return learnware
