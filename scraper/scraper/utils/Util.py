

def stripList(list: list[str]) -> list[str]:
    """Takes a list and strips all whitespace from each element.

    Args:
        list (list[str]): A list of strings.

    Returns:
        list[str]: A list of strings with whitespace stripped.
    """    
    return [item.strip() for item in list if str(item).strip().__len__() > 0]    
