def cors_allow_credentials():
    def decorator_func(func):
        def wrapper_func(*args, **kwargs):
            retval = func(*args, **kwargs)
            retval['Access-Control-Allow-Credentials'] = 'true'
            return retval
        return wrapper_func
    return decorator_func
