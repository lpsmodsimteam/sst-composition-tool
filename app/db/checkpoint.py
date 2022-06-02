from datetime import datetime
from pathlib import Path
import json

checkpoints = Path().resolve() / ".checkpoints"


def log_history(library: str):

    fp = checkpoints / (library + ".json")
    if fp.is_file():
        with open(fp) as history_file:
            history = json.loads(history_file.read())
            history.append(1)
            json.dump(history, history_file)

    else:
        with open(fp, "w") as history_file:
            return 0


def get_last_checkpoint_name(library: str):
    pass


print(log_history("adder"))
