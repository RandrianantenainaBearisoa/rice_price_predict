import joblib
import numpy as np

def post_process_result(val: float):
    pt = joblib.load('./artifacts/transformation/box_cox/box_cox.joblib')
    val = np.array(val).reshape(-1, 1)
    return pt.inverse_transform(val).item()