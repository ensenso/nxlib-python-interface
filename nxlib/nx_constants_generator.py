import os, sys

from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))

from nxlib.nx_proxy import NxLib, NxLibItem, NxLibCommand

import json

GENERATED_FILE_PATH = "nxlib/nx_constants.py"
DELETE_AND_GENERATE_NEW_FILE = "w"


if __name__ == "__main__":
    nxLib = NxLib('libNxLib64.so')

    cmd = NxLibCommand("GetConstants")
    cmd.execute()
    result = cmd.result()
    itm = result.asJson()
    json_object = json.loads(itm)

    # Create the py file
    file_object = open(GENERATED_FILE_PATH, DELETE_AND_GENERATE_NEW_FILE)
    for constantType in json_object:
        # In order to ignore command results like time etc.
        if(isinstance(json_object[constantType], list)):
            file_object.write("class {}(object):\n".format(constantType))
            for constant in json_object[constantType]:

                # Check if entry is string value or a string mapped to a value (dictionary)
                if isinstance(constant, dict):
                    file_object.write(
                        "    {} = {}\n".format(constant["Name"], constant["Value"]))
                else:
                    file_object.write(
                        "    {} = \"{}\"\n".format(constant, constant))

    file_object.close()
