import importlib
import json
from pathlib import Path


def test_selected_model_ids_and_parameters_exist_in_backend_source():
    data = json.loads((Path(__file__).parents[1] / "contracts.json").read_text())
    classes = {
        "suno": "Suno",
        "seedance": "Seedance",
        "happyhorse": "HappyHorse",
        "gpt_image": "GPTImage",
        "nano_banana": "NanoBanana",
    }
    for contract in data["contracts"]:
        module = importlib.import_module(f"langchain_{contract['service']}_acedatacloud")
        schema = getattr(module, classes[contract["service"]] + "Input").model_json_schema()
        for field, definition in schema["properties"].items():
            official = contract["fields"].get(field)
            if official and "enum" in definition and "enum" in official:
                assert set(definition["enum"]) <= set(official["enum"])
            if official and "default" in definition and "enum" in official:
                assert definition["default"] in official["enum"]
