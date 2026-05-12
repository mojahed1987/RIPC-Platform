import json
import pandas as pd


def save_json(data, path):

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"JSON SAVED: {path}")


def save_excel(data, path):

    df = pd.DataFrame(data)

    df.to_excel(path, index=False)

    print(f"EXCEL SAVED: {path}")