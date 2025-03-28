# from .checks import (
#     check_bernoulli_dependence,
#     check_bernoulli_equal_means,
#     check_nans,
#     check_too_less_unique_value,
#     process_too_much_categories,
#     check_leaks_v2,
#     check_leaks,
#     check_correlations,
#     check_train_val_test_split
# )

# __all__ = [
#     "check_bernoulli_dependence",
#     "check_bernoulli_equal_means",
#     "check_nans",
#     "check_too_less_unique_value",
#     "process_too_much_categories",
#     "check_leaks_v2",
#     "check_leaks",
#     "check_correlations",
#     "check_train_val_test_split"
# ]


# нужно перенести в модуль data:
# 1) проверки данных (текущий checks.py)
#         - статистические проверки (бернулли, ...)
#         - проверки разбиения данных на трейн вал тест (возможно в соотв блок но тогда проверки не в одном месте будут)
#         - проверки значений в данных (пропуски, уникальные значения)
#         - отсев признаков по корреляциям ()
# 2) препроцессинг
# 3) разбивка на трейн вал тест