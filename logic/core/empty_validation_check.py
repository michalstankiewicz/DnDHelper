def validate_list(data, name):
    if not isinstance(data, list):
        raise ValueError(f"{name} must be a list")
    if len(data) == 0:
        raise ValueError(f"{name} list is empty")


def validate_item(item, error_msg):
    if not isinstance(item, dict):
        raise ValueError(error_msg)
    return item.copy()
