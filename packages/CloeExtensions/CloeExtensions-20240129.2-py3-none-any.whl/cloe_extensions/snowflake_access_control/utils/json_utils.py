import re

CAMEL_TO_SNAKE_PATTERN_FIRST = re.compile(r"(.)([A-Z][a-z]+)")
CAMEL_TO_SNAKE_PATTERN_LAST = re.compile(r"([a-z0-9])([A-Z])")


def camel_to_snake(name: str):
    name = re.sub(CAMEL_TO_SNAKE_PATTERN_FIRST, r"\1_\2", name)
    return re.sub(CAMEL_TO_SNAKE_PATTERN_LAST, r"\1_\2", name).lower()


def dict_keys_to_snake(model: dict | list):
    if isinstance(model, list):
        return [
            dict_keys_to_snake(i) if isinstance(i, (dict, list)) else i for i in model
        ]
    return {
        camel_to_snake(a): dict_keys_to_snake(b) if isinstance(b, (dict, list)) else b
        for a, b in model.items()
    }


def read_model_from_json(json_input: dict) -> dict[str, list]:
    """Central endpoint for all functions/classes
    to read multiple json files from disk.

    Args:
        file_paths (list): _description_

    Returns:
        dict[str, dict | list]: _description_
    """
    all_jsons = {}
    content = json_input
    if isinstance(content, dict) and "modelID" in content and "modelContent" in content:
        trans_content = dict_keys_to_snake(content["modelContent"])
        all_jsons[content["modelID"]] = trans_content
    return all_jsons
