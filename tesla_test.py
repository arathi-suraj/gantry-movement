from lakeshore import Teslameter
import numpy as np
import csv
"""
# Un-comment any code if you want to use it!
# This checks if the probe is connected and what kind of data it gives.

sol_teslameter = Teslameter()
sol_teslameter.command("SENSE:MODE DC")

serial_num = sol_teslameter.query("PROBE:SNUMBER?")
probe_field = sol_teslameter.get_dc_field()

field_file = open("teslameter_data.txt", "w")
write = csv.writer(field_file)

word = ""
for times in range(0, 2):
    write.writerow("")

sol_teslameter.log_buffered_data_to_file(10, 10, field_file)
field_file.close()

field_fix = np.loadtxt("/Users/arathisuraj/Desktop/teslameter_data.txt", \
                       delimiter=",", skiprows=3, usecols=(4,5,6))

x_array = field_fix[:,0]
y_array = field_fix[:,1]
z_array = field_fix[:,2]
"""
"""
sol_teslameter = Teslameter()
sol_teslameter.command("SENSE:MODE DC")

field_file = open("tesla_test.txt", "w")
write = csv.writer(field_file)

while True:
    probe_field = sol_teslameter.get_dc_field()
    write.writerow(probe_field)
    stop = str(input("Quit? (Y/N) "))
    if stop.lower() == "y":
        break
    elif stop.lower != "y":
        pass
"""
sol_teslameter = Teslameter()
sol_teslameter.command("SENSE:MODE DC")

word = "Y"
new_file = open("new_file.txt", "a")

while (word.upper() == "Y"):
    probe_field = sol_teslameter.get_dc_field()
    new_file.write(f"{probe_field}\n")
    word = str(input("Continue? (Y/N) "))

new_file.close()
