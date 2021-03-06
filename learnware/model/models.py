# coding=utf-8
import datetime
import importlib

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from learnware.app import _db
from sqlalchemy import create_engine
import pandas as pd

DATASOURCE_TYPE_MYSQL = "mysql"
DATASOURCE_TYPE_HDFS = "hdfs"


class BaseMixin:
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.now)
    created_by = Column(String(length=255))
    updated_at = Column(DateTime, nullable=False, default=datetime.datetime.now, onupdate=datetime.datetime.now,
                        index=True)
    updated_by = Column(String(length=255))


class DataSource(_db.Model, BaseMixin):
    __tablename__ = "aiops_datasource"
    name = Column(String(length=255))
    type = Column(String(length=128))
    url = Column(String(length=1024))
    username = Column(String(length=128))
    password = Column(String(length=128))
    notes = Column(String(length=1024))
    datasets = relationship("DataSet", back_populates="datasource")

    def __repr__(self):
        return "<DataSource %s> ID:%d" % (self.name, self.id)


class DataSet(_db.Model, BaseMixin):
    __tablename__ = "aiops_dataset"
    name = Column(String(length=255))
    sql = Column(String(length=2048))
    filepath = Column(String(length=2048))
    notes = Column(String(length=1024))
    datasource_id = Column(Integer, ForeignKey('aiops_datasource.id'))
    datasource = relationship("DataSource", back_populates="datasets")
    learnwares = relationship("Learnware", back_populates="dataset")

    def __repr__(self):
        return "<DataSet %s> ID:%d" % (self.name, self.id)

    def fetch_all_to_dataframe(self):
        if self.datasource.type == DATASOURCE_TYPE_MYSQL:
            engine = create_engine(self.datasource.url, echo=True)
            return pd.read_sql_query(self.sql, con=engine)


class Learnware(_db.Model, BaseMixin):
    __tablename__ = "aiops_learnware"
    name = Column(String(length=255))
    notes = Column(String(length=1024))
    module_path = Column(String(length=1024))
    class_name = Column(String(length=1024))
    dataset = relationship("DataSet", back_populates="learnwares")
    dataset_id = Column(Integer, ForeignKey('aiops_dataset.id'))
    learnware_models = relationship("LearnwareModel", back_populates="learnware")
    train_settings = Column(JSON)

    def __repr__(self):
        return "<Learnware %s> ID: %d" % (self.name, self.id)

    @property
    def learnware_class(self):
        mod = importlib.import_module(self.module_path)
        clazz = getattr(mod, self.class_name)
        return clazz


class LearnwareModel(_db.Model, BaseMixin):
    __tablename__ = "aiops_learnware_model"
    name = Column(String(length=255))
    learnware_id = Column(Integer, ForeignKey('aiops_learnware.id'))
    learnware = relationship("Learnware", back_populates="learnware_models")
    task_id = Column(Integer, ForeignKey('aiops_learnware_train_task.id'))
    task = relationship("LearnwareTrainTask", back_populates="learnware_models")
    model_file_path = Column(String(length=4096))
    model_estimate_result = Column(JSON)

    def __repr__(self):
        return "<Learnware Model %s>" % self.name


class LearnwareTrainTask(_db.Model, BaseMixin):
    __tablename__ = "aiops_learnware_train_task"
    learnware_id = Column(Integer)
    learnware_models = relationship("LearnwareModel", back_populates="task")

    def __repr__(self):
        return "<Learnware Train Task: %s>" % self.id
