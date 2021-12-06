import functools


def wrapper(*args,**kwargs):
    print(f"Fields: {args}")
    def decorator(func):
        def inner(*args2,**kwargs2):
            dataf = func()
            print("In func inner")
            return f"Data returned from func: {dataf} with param {args}-{kwargs}"
        return inner

    return decorator


@wrapper("idgrupo2","nombre2",param=11,id=21)
@wrapper(*["idgrupo","nombre"],param=10,id=1)
def hello():
    return "Hello"

print(hello())