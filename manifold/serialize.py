def serialize(instance):
    """
    Serializes an object to a dictionary recursively,
    so it can be converted to JSON
    :param instance: any python value or instance
    :return: dictionary serialization of instance
    """
    def to_dict(obj):
        if isinstance(obj, dict):
            return {key: to_dict(value) for key, value in obj.items()}
        elif isinstance(obj, (set, list)):
            return [to_dict(item) for item in obj]

        try:
            return {key: to_dict(value) for key, value in obj.__dict__.items()}
        except AttributeError:
            return obj

    return to_dict(instance)
