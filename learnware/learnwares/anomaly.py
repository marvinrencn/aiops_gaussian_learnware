import matplotlib.pyplot as plt
import pandas as pd

def single_kpi_anomaly_result_graph(result_df):
    """
    :param result_df: 预测结果的数据, 需要定义为DataFrame类型,anomaly是异常列，-1为异常，1为正常，例子如下：
    |timestamp|value|anomaly|
    |1|33|-1|
    |2|25|1|
    :return:返回plt对象
    """
    map_color = {-1: 'r', 1: 'b'}
    color = list(map(lambda x: map_color[x], result_df["anomaly"]))
    map_size = {-1: 10, 1: 1}
    size = list(map(lambda x: map_size[x], result_df["anomaly"]))
    plt.scatter(result_df["timestamp"], result_df["value"], c=color, s=size, marker="o", zorder=10)
    plt.plot(result_df["timestamp"], result_df["value"], alpha=0.8, zorder=1)

    return plt


def single_kpi_predict_result(df, pipe_clf):
    y_pred_train = pipe_clf.predict(df["origin_value"].values.reshape(-1, 1))
    result_df = pd.DataFrame({"timestamp": df["timestamp"], "value": df["origin_value"], "anomaly": y_pred_train})
    return result_df