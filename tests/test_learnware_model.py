import pyhdfs

from learnware.learnwares.store import save_sklearn_model
from sklearn import svm
from sklearn import datasets

from learnware.model.models import LearnwareModel


def test_hdfs():
    iris = datasets.load_iris()
    clf = svm.SVC()
    X, y = iris.data, iris.target
    clf.fit(X, y)
    file_path = save_sklearn_model(clf)

    # 确定文件以上上传
    fs = pyhdfs.HdfsClient(hosts='127.0.0.1,50070', user_name='root')
    assert fs.exists(file_path)


def test_model(db, learnware_record_1):
    db.session.add(LearnwareModel(learnware=learnware_record_1))
    db.session.commit()



