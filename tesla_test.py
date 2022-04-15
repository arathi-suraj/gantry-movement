from lakeshore import Teslameter
from csv import writer

sol_teslameter = Teslameter()
sol_teslameter.command("SENSE:MODE DC")

serial_num = sol_teslameter.query("PROBE:SNUMBER?")
probe_field = sol_teslameter.get_dc_field()

field_file = open("teslameter_data.txt", "w")
writer = csv.writer(field_file)

word = ""
while (word != "Y" or word != "y"):
    writer.writerow(serial_num, probe_field)
    word = str(input("Quit? (Y/N) "))

sol_teslameter.log_buffered_data_to_file(10, 10, field_file)
field_file.close()
