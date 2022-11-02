def convert_string_bool(str_bool):
    str_bool = str(str_bool)
    print(str_bool.lower().capitalize())
    return eval(str_bool.lower().capitalize())
    