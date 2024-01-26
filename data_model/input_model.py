import csv
import gspread as gsp


class ModelLoadStregyBase():
    def __init__(self) -> None:
        pass

    def load(self):
        pass


class LocalLoader(ModelLoadStregyBase):
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        super().__init__()

    def load(self):
        data = []
        with open(self.file_path, "r", encoding="utf-8") as csv_input:
            csv_reader = csv.DictReader(csv_input)
            for row in csv_reader:
                data.append(row)
        return data


class GoogleLoader(ModelLoadStregyBase):
    def __init__(self, file_url: str, sheet_index: int, credential_path: str) -> None:
        self.file_path = file_url
        self.credential_path = credential_path
        self.sheet_index = sheet_index
        super().__init__()

    def load(self):
        data = []
        gc = gsp.service_account(self.credential_path)
        document = gc.open_by_url(self.file_path)
        sheet = document.get_worksheet(self.sheet_index)
        data = sheet.get_all_records()
        return data


def default_parse_func(raw_data):
    return raw_data


class InputModel():
    def __init__(self, load_stregy: ModelLoadStregyBase, parse_func=default_parse_func) -> None:
        self.load_stregy = load_stregy
        self.parse_func = parse_func
        self._questions = None

    def load_get_questions(self):
        if self._questions is None:
            self._questions = self.parse_func(self.load_stregy.load())

        return self._questions

    def reload_get_questions(self):
        self._questions = None
        return self.load_get_questions()
