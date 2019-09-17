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
        self.command_name = command_name
        self.remove_slot_on_destruction = False
        temporary_item = node_name is None

        if temporary_item:
            self.command_item = NxLibItem()[ITM_EXECUTE].make_unique_item()
            self.remove_slot_on_destruction = True
        else:
            self.command_item = NxLibItem()[ITM_EXECUTE][node_name]

    def __del__(self):
        try:
            if self.remove_slot_on_destruction:
                self.command_item.erase()
        except NxLibException:
            pass

    def create_temporary_slot(self, base_name):
        self.remove_slot_on_destruction = True
        exec_item = NxLibItem()[ITM_EXECUTE]
        self.command_item = exec_item.make_unique_item(base_name)

    def parameters(self):
        return self.command_item[ITM_PARAMETERS]

    def result(self):
        return self.command_item[ITM_RESULT]

    def successful(self):
        return not self.result()[ITM_ERROR_SYMBOL].exists()

    def execute(self, command_name=None, wait=True):
        function_item = self.command_item[ITM_COMMAND]
        if not command_name:
            command_name = self.command_name
        function_item.set_t(command_name)

        if wait:
            function_item.wait_for_type(NXLIB_ITEM_TYPE_NULL, True)
            self.assert_successful()

    def finished(self):
        return not self.command_item[ITM_COMMAND].exists() or self.command_item[ITM_COMMAND].type() == NXLIB_ITEM_TYPE_NULL

    def assert_successful(self):
        if not self.finished() or not self.successful():
            raise NxLibException(self.command_item.path, NXLIB_EXECUTION_FAILED, self)
