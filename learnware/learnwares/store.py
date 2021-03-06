import os
import tempfile
import uuid

import joblib
import pyhdfs
from sqlalchemy import create_engine


def save_sklearn_model(clf, train_task_id, name="model"):
    filename = "{}_{}_{}.pkl".format(name, train_task_id, _generate_uuid())
    model_temp_file = os.path.join(tempfile.mkdtemp(), filename)
    joblib.dump(clf, model_temp_file)
    model_file_path = _save_file_to_hdfs(model_temp_file, filename)
    return model_file_path


def load_sklearn_model(remote_model_file_path):
    model_file = os.path.join(tempfile.mkdtemp(), _generate_uuid() + ".pkl")
    fs = pyhdfs.HdfsClient(hosts='127.0.0.1,50070', user_name='root')
    fs.copy_to_local(remote_model_file_path, model_file)
    clf = joblib.load(model_file)
    return clf


def save_matplotlib_pic(plt, train_task_id, name="pic"):
    filename = "{}_{}_{}.png".format(name, train_task_id, _generate_uuid())
    pic_temp_file = os.path.join(tempfile.mkdtemp(), filename)
    plt.savefig(pic_temp_file)
    return _save_file_to_hdfs(pic_temp_file, filename)


def save_data_to(df, datasource, table_name, mode="replace"):
    db_url = datasource.url
    engine = create_engine(db_url, echo=True)
    df.to_sql("machine1933", con=engine, if_exists="replace")


def _generate_uuid():
    return str(uuid.uuid4())


def _save_file_to_hdfs(local_filename, dst_filename=None):
    fs = pyhdfs.HdfsClient(hosts='127.0.0.1,50070', user_name='root')
    home_directory = fs.get_home_directory()
    remote_path = "{}/learnware_model".format(home_directory)

    if dst_filename is None:
        dst_filename = str(uuid.uuid4())

    remote_path_file = os.path.join(remote_path, dst_filename).replace("\\", "/")

    fs.mkdirs(remote_path) if not fs.exists(remote_path) else None
    if fs.exists(remote_path_file):
        fs.delete(remote_path_file)
    fs.copy_from_local(local_filename, remote_path_file)

    return remote_path_file

