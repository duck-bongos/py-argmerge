# import pytest

# from argmerge.decorator import threshold
# from tests.utils import no_error

# default_threshold_tasks_no_runtime = [(pytest.raises(TypeError))]
# default_threshold_tasks_w_runtime = [(1, "hello", 0.0, no_error)]


# @pytest.mark.parametrize("context", default_threshold_tasks_no_runtime)
# def test_default_threshold_no_runtime_args(context):
#     @threshold
#     def fake_function(a: int, b: str, c: float = 3.14):
#         pass

#     with context:
#         fake_function()  # when we don't provide 'a' or 'b', this breaks


# @threshold
# def fake_function(a: int, b: str, c: float = 3.14):
#     pass


# @pytest.mark.parametrize("a,b,c,context", default_threshold_tasks_w_runtime)
# def test_default_threshold_w_runtime_args(a, b, c, context):
#     with context:
#         fake_function(a=a, b=b, c=c)
