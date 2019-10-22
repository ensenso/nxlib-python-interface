import ensenso_nxlib

__all__ = [
    "NxLibError",
    "NxLibException"
]


class NxLibError(Exception):
    def __init__(self, message=None):
        self._message = message

    def __str__(self):
        return self._message


class NxLibException(NxLibError):
    def __init__(self, path, error_code, command=None):
        self._path = path
        self._error_code = error_code

        # Save command object in the exception to keep temporary slots alive while an exception exists.
        self._command = command

    def get_error_code(self):
        return self._error_code

    def get_error_text(self):
        return ensenso_nxlib.api.translate_error_code(self._error_code)

    def get_item_path(self):
        return self._path

    def __str__(self):
        message = "NxLib error {} ({}) for item {}".format(self._error_code, self.get_error_text(), self._path)

        try:
            if self._path:
                message += "\nCurrent item value: {}".format(ensenso_nxlib.NxLibItem(self._path).as_json(True))
        except NxLibError:
            pass

        return message
