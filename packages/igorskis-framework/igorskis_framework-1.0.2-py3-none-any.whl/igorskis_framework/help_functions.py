def convert_to_bool(value):
    true_values = ["true", "1", "t", "y", "yes", "on"]
    false_values = ["false", "0", "f", "n", "no", "off"]
    if value.lower() in true_values:
        return True
    elif value.lower() in false_values:
        return False
    else:
        raise ValueError("Неверное значение. Ожидается true или false.")