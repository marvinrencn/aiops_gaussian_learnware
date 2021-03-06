# -*- coding:utf-8 -*-
import os
import sys

import joblib

from learnware.model.models import LearnwareModel, LearnwareTrainTask

sys.path.append(os.getcwd())


def test_learnware_train(db, learnware_record_1):
    task = LearnwareTrainTask(learnware_id=learnware_record_1.id)
    db.session.add(task)
    db.session.flush()
    db.session.commit()

    learnware = learnware_record_1.learnware_class(learnware_record_1, db)
    learnware.train(task.id)

    models = LearnwareModel.query.filter(LearnwareModel.learnware == learnware_record_1).order_by(
        LearnwareModel.created_at.desc()).all()
    assert len(models) > 0
    model = models[0]
    print(model.name)
    print(model.model_file_path)
    print(model.model_estimate_result["anomaly_rate"])
    # 判断model存储正确
    assert (model.name is not None and len(model.name) > 0)
    assert (model.model_file_path is not None and len(model.model_file_path) > 0)
    assert (model.model_file_path.endswith(".pkl"))
    assert (model.model_estimate_result["anomaly_rate"] is not None)


def test_learnware_call(db, learnware_record_1, mocker):
    clf = joblib.load("data/model_2_025c3ce8-ef92-4caf-a905-ff0005662918.pkl")
    # load_model_method = mocker.patch('learnware.learnwares.store.load_sklearn_model', return_value=clf)

    model = LearnwareModel(learnware=learnware_record_1)

    learnware = learnware_record_1.learnware_class(learnware_record_1, db)
    load_model_method = mocker.patch.object(learnware, "load_model", return_value=clf)
    result = learnware.call(model, [[4], [5], [6], [7]])

    print(result)
    load_model_method.assert_called_once()
    assert result[0] == -1
    assert result[1] == 1
    assert result[2] == 1
    assert result[3] == -1
