def example_args_kwargs(arg1, *args, kwarg1="default", **kwargs):
    print(f"arg1: {arg1}")
    print(f"args: {args}")
    print(f"kwarg1: {kwarg1}")
    print(f"kwargs: {kwargs}")

example_args_kwargs(1, 2, 3, kwarg1="123", name="Alice", age=30)