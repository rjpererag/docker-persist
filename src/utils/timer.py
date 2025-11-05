def set_timer(
        min_time: int = 1,
        max_time: int = 2
) -> tuple[int, int]:
    """
    Validates and returns a tuple with the min and max time in seconds.
    :param min_time:
    :param max_time:
    :return:
    """
    def validate_time() -> bool:
        if (not isinstance(min_time, int)) or (not isinstance(max_time, int)):
            return False

        elif min_time >= max_time:
            return False

        return True

    min_default, max_default = 1, 2
    if not validate_time():
        return min_default, max_default
    return min_time, max_time
