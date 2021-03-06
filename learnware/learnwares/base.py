from learnware.learnwares.store import save_sklearn_model, load_sklearn_model
from learnware.model.models import LearnwareModel


class BaseLearnware(object):

    def __init__(self, learnware_record, db):
        self.learnware_record = learnware_record
        self.db = db

    def train(self, task_id):
        pass

    def call(self, model_record, data):
        pass

    def save_model(self, clf, task_id, model_estimate_result):
        model_file_path = save_sklearn_model(clf, task_id)

        self.db.session.add(LearnwareModel(
            name=self.learnware_record.name + "_" + str(task_id) + "_model",
            model_file_path=model_file_path,
            learnware=self.learnware_record,
            task_id=task_id,
            model_estimate_result=model_estimate_result
        ))
        self.db.session.commit()

        return model_file_path

    def load_model(self, model):
        assert model is not None
        return load_sklearn_model(model.model_file_path)
