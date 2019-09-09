class NxLibException(Exception):
    def __init__(self, message, path, error_code):
        # super(NxLibException, self).__init__(message)
        # super().__init__(message)

        self.path = path
        self.error_code = error_code
        self.message = str(message) + str(' at ') + str(self.path) + \
            str(' - error_code ') + str(self.error_code)

    def get_error_code(self):
        return self.error_code

    def get_error_text(self):
        return str(self.message)

    def get_item_path(self):
        return self.path

    def __str__(self):
        return str(self.message)
