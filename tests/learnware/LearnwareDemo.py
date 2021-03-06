from sklearn.ensemble import IsolationForest
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from learnware.learnwares.anomaly import single_kpi_predict_result, single_kpi_anomaly_result_graph
from learnware.learnwares.base import BaseLearnware
from learnware.learnwares.store import save_matplotlib_pic
from learnware.learnwares.validation import validate_json_parameters


class LearnwareDemo1(BaseLearnware):

    def train(self, task_id):
        # 获取数据
        dataset = self.learnware_record.dataset
        df = dataset.fetch_all_to_dataframe()

        # 参数校验
        settings = self.learnware_record.train_settings
        validate_json_parameters(settings, ["n_estimators", "isStandard"])
        pipeline_list = []

        # 形成PipeLine
        if settings["isStandard"]:
            pipeline_list.append(('scl', StandardScaler()))
        pipeline_list.append(('iForest', IsolationForest(random_state=42, n_estimators=settings["n_estimators"])))
        pipe_clf = Pipeline(pipeline_list)

        # 进行训练
        pipe_clf.fit(df["origin_value"].values.reshape(-1, 1))

        # 生成训练数据的异常结果
        result_df = single_kpi_predict_result(df, pipe_clf)

        plt = single_kpi_anomaly_result_graph(result_df)
        model_file = self.save_model(pipe_clf, task_id, {
            "anomaly_rate": result_df[result_df["anomaly"] == -1]["anomaly"].count() / result_df["anomaly"].count()})
        pic_file = save_matplotlib_pic(plt, task_id)

    def call(self, model_record, data):
        model = self.load_model(model_record)
        return model.predict(data)

        # save_data_to(result_df, dataset.name + "_anomaly_detection", )