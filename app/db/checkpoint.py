from datetime import datetime
from pathlib import Path, PosixPath
import json

CHECKPOINTS = Path().resolve() / ".checkpoints"


def get_checkpoint_path(library: str) -> PosixPath:

    return CHECKPOINTS / (library + ".json")


def get_history_path(library: str) -> PosixPath:

    return get_checkpoint_path(f"{library}_log")


def log_history(library: str) -> None:

    history_file = get_history_path(library)
    current_datetime = str(datetime.now())

    if history_file.is_file():
        with open(history_file, "r+") as fp:
            history = json.loads(fp.read())
            fp.seek(0)
            history.append(current_datetime)
            json.dump(history, fp)

    else:
        with open(history_file, "w") as fp:
            json.dump([current_datetime], fp)


def get_checkpoint_name(library: str) -> PosixPath:

    history_file = get_history_path(library)
    log_history(library)

    with open(history_file) as fp:
        history = json.loads(fp.read())
        return get_checkpoint_path(f"{library}-{len(history) - 1}")


def clear_checkpoints(library: str) -> None:

    history_file = get_history_path(library)

    if history_file.is_file():
        with open(history_file) as fp:
            history = json.loads(fp.read())
            for i in range(len(history)):
                get_checkpoint_path(f"{library}-{i}").unlink(missing_ok=True)

        history_file.unlink()
