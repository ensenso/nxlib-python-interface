# -*- coding: utf-8 -*-

from .exception import NxLibException
from .item import NxLibItem

__all__ = ["NxLibCommand"]

ITM_EXECUTE = "Execute"
ITM_RESULT = "Result"
ITM_COMMAND = "Command"
ITM_PARAMETERS = "Parameters"
ITM_ERROR_SYMBOL = "ErrorSymbol"

NXLIB_OPERATION_SUCCEEDED = 0
NXLIB_EXECUTION_FAILED = 17
NXLIB_ITEM_TYPE_NULL = 1


class NxLibCommand:
    def __init__(self, command_name, node_name=None):
        self._command_name = command_name
        self._remove_slot_on_destruction = False

        if node_name is None:
            self.create_temporary_slot()
        else:
            self._command_item = NxLibItem()[ITM_EXECUTE][node_name]

    def __del__(self):
        try:
            if self._remove_slot_on_destruction:
                self._command_item.erase()
        except NxLibException:
            pass

    def create_temporary_slot(self, base_name=None):
        self._command_item = NxLibItem()[ITM_EXECUTE].make_unique_item(base_name)
        self._remove_slot_on_destruction = True

    def slot(self):
        return self._command_item

    def parameters(self):
        return self.slot()[ITM_PARAMETERS]

    def result(self):
        return self.slot()[ITM_RESULT]

    def successful(self):
        return not self.result()[ITM_ERROR_SYMBOL].exists()

    def execute(self, command_name=None, wait=True):
        if not command_name:
            command_name = self._command_name

        function_item = self.slot()[ITM_COMMAND]
        function_item.set_t(command_name)

        if wait:
            function_item.wait_for_type(NXLIB_ITEM_TYPE_NULL, True)
            self.assert_successful()

    def finished(self):
        return not self.slot()[ITM_COMMAND].exists() or self.slot()[ITM_COMMAND].is_null()

    def assert_successful(self):
        if not self.finished() or not self.successful():
            raise NxLibException(self.slot().path, NXLIB_EXECUTION_FAILED, self)
