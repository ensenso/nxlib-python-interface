import os


def file_appender(input_file_names, input_directory, output_directory, output_name):
    file_output = os.path.join(output_directory, output_name)
    f_out = open(file_output, "w")

    for file in input_file_names:
        inputfile = os.path.join(input_directory, file)
        f_in = open(inputfile, "r")
        for line in f_in:
            f_out.write(line)
        f_in.close()
    f_out.close()
