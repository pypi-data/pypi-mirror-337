def overfit_abs(metric_valid: float, metric_train: float) -> float:
    """
        function check abs diffirence between metric on train and validation
    Args:
       metric_valid: metric on valid
       metric_train: metric on train

    Returns:
        float: diffirence between metric on train and validation
    """
    return -abs(metric_valid - metric_train)


def overfit_metric_minus_metric_delta(
    metric_valid: float, metric_train: float
) -> float:
    """
        function check metric on validation and considers abs diffirence between metric on train and validation
    Args:
       metric_valid: metric on validation
       metric_train: metric on train

    Returns:
        float: diffirence between metric on train and validation
    """
    return metric_valid - abs(metric_valid - metric_train) / 2
