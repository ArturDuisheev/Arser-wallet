from global_modules.exeptions import CodeDataException


def get_field_in_dict_or_exception(data: dict, field, message, code=400):
    if data.get(field):
        return data[field]
    else:
        raise CodeDataException(error=message, status=code)