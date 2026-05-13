import joblib
import numpy as np
from src.core.inference.WrappedException import WrappedException

def post_process_result(val: float):
    try:
        pt = joblib.load('./artifacts/transformation/box_cox/box_cox.joblib')
        val = np.array(val).reshape(-1, 1)
        return pt.inverse_transform(val).item()
    except Exception as e:
        raise WrappedException(original_exception=e, exception_location="post_process_result()", entry=val) from e