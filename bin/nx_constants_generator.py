import os
import json

from ensenso_nxlib import NxLibCommand, NxLibException
from ensenso_nxlib.helper import fix_nxlib_prefix, convert_camel_to_upper_snake

from bin import file_appender as appender

GENERATED_FILE_PATH = "constants_generated.py"
DELETE_AND_GENERATE_NEW_FILE = "w"

CONSTANTS_PREFIX = {'Commands': 'cmd', 'Errors': 'err', 'Items': 'itm',
                    'Values': 'val', 'ApiErrors': 'NxLib', 'ItemTypes': 'NxLib'}


def generate_constants_from_loaded_lib():
    print("Generating ensenso_nxlib constants...")
    cmd = NxLibCommand("GetConstants")
    cmd.execute()
    result = cmd.result()
    itm = result.as_json()
    json_object = json.loads(itm)

    # Create the py file
    file_object = open(GENERATED_FILE_PATH, DELETE_AND_GENERATE_NEW_FILE)
    for constant_type in json_object:
        # In order to ignore command results like time etc.
        if(isinstance(json_object[constant_type], list)):

            prefix = CONSTANTS_PREFIX[constant_type]
            for constant in json_object[constant_type]:
                variable_name = None
                value = None
                if isinstance(constant, dict):
                    variable_name = prefix + constant['Name']
                    value = constant['Value']
                else:
                    variable_name = prefix + constant
                    value = str(constant)
                variable_name = convert_camel_to_upper_snake(variable_name)
                if variable_name.startswith('NX_LIB'):
                    variable_name = fix_nxlib_prefix(variable_name)

                if isinstance(value, str):
                    file_object.write(
                        "{} = \"{}\"\n".format(variable_name, value))
                else:
                    file_object.write(
                        "{} = {}\n".format(variable_name, value))

    file_object.close()

    print("...finished.")

    pass


if __name__ == '__main__':
    generate_constants_from_loaded_lib()

    current_directory = os.path.dirname(os.path.realpath(__file__))
    repo_directory = os.path.dirname(current_directory)
    output_name = "constants.py"
    package_name = "ensenso_nxlib"

    print("Writing constants module {} to package {}".format(output_name, package_name))
    appender.file_appender(['header_part.txt', 'constants_generated.py', 'execute_part.txt'],
                           current_directory,
                           output_name,
                           os.path.join(repo_directory + "/" + package_name, output_name))
    print("Please install ensenso_nxlib package now in order to make the new generated {} module available".format(output_name))
