from datetime import datetime
import filecmp
import json
from pathlib import Path, PosixPath
from typing import Any


class Database:
    def __init__(self, library: str) -> None:

        self.checkpoints = Path().resolve() / ".checkpoints"
        self.library = library
        self.history_path = self.__get_path(f"{self.library}_log")
        self.history = []

    def __get_path(self, filename: str) -> PosixPath:

        return self.checkpoints / (filename + ".json")

    def __log_history(self) -> None:

        current_datetime = str(datetime.now())

        with open(self.history_path, "w") as fp:
            self.history.append(current_datetime)
            json.dump(self.history, fp)

    def __overwrite_history(self) -> None:

        with open(self.history_path, "w") as fp:
            self.history = self.history[:-2] + [self.history[-1]]
            json.dump(self.history, fp)

    def __get_checkpoint_name(self) -> PosixPath:

        return self.__get_path(f"{self.library}-{len(self.history) - 1}")

    def __get_last_checkpoint(self) -> PosixPath | None:

        if len(self.history):
            return self.__get_checkpoint_name()

    def load_history(self) -> None:

        if self.history_path.is_file():
            with open(self.history_path) as fp:
                self.history = json.loads(fp.read())

    def save_checkpoint(self, data: Any) -> None:

        last_checkpoint = self.__get_last_checkpoint()
        self.__log_history()
        new_checkpoint = self.__get_checkpoint_name()

        with open(new_checkpoint, "w") as fp:
            json.dump(data, fp)

        if last_checkpoint:
            if filecmp.cmp(last_checkpoint, new_checkpoint, shallow=False):
                self.__overwrite_history()
                new_checkpoint.unlink()

    def clear_checkpoints(self) -> None:

        for i in range(len(self.history)):
            self.__get_path(f"{self.library}-{i}").unlink(missing_ok=True)

        self.history_path.unlink(missing_ok=True)
