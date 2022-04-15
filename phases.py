import pyfirmata as fir
import numpy as np
import time, pickle
from lakeshore import Teslameter

class axis(object):
    
    def __init__(self):
        self.dim = None
        self.current_dist = 0
        self.dir_pin = None
        self.pul_pin = None
        self.Dir = None
        self.pulperrev = None
        self.ever_saved = 0
        self.stop = 0
        self.incdist = None

    def initSwitches(self):
        switch_dict = {"456":400, "56":800, "46":1600, "6": 3200, "45":6400, "5":12800,\
                       "4": 4000, "0":8000}
        user_input = input(str("Enter the switch numbers of only the ON switches.\
Enter 0 if all switches are off. Enter: "))
        while True:
            try:
                self.pulperrev = switch_dict[user_input]
                break
            except KeyError:
                self.pulperrev = None
                print("Invalid value entered. Call again.")
                user_input = input(str("Enter the switch numbers of only the ON switches.\
Enter 0 if all switches are off. Enter: "))

    def setPins(self):
        while True:
            if self.dim == None:
                self.dim = str(input("Enter dimension (X/Y/Z): ")).lower()
            if self.dim == "x":
                self.pul_pin = 2
                self.dir_pin = 3
                break
            elif self.dim == "y":
                self.pul_pin = 4
                self.dir_pin = 5
                break
            elif self.dim == "z":
                self.pul_pin = 8
                self.dir_pin = 9
                break
            else:
                print(f"{self.dim} is not a valid input. Try X/Y/Z.")
                self.dim = str(input("Enter dimension (X/Y/Z): ")).lower()

    def onePulse(self):
        # DON'T CHANGE THIS VALUE (used to be 0.957)
        pitch = 1 # (cm) double start, so this is really pitch * 2
        one_pulse = pitch/(self.pulperrev) # gives cm/pulse
        return one_pulse 

    def pulseCalc(self, dist=0):
        if self.dim in ["x", "y", "z"]:
            while True:
                """
                if dist_to_go <= self.stop:
                    balance = abs(self.current_dist - dist_to_go)
                    #print(balance)   for debugging
                    if dist_to_go < self.current_dist:
                        self.Dir = "-"
                        self.current_dist -= balance
                    elif dist_to_go >= self.current_dist:
                        self.Dir = "+"
                        self.current_dist += balance
                """
                num_pulse = abs(dist)/(self.onePulse())
                return num_pulse
                break
                #else:
                    #dist_to_go = float(input(f"Dist (cm) to go to? Must be less than {self.stop} "))
        else:
            print("Invalid input.")
            self.setPins()

    def AxisMove(self, pul, Dir):
        count_Flag = 0

        if __name__ == "__main__":
            try:
                board = fir.Arduino("/dev/tty.usbmodem141101")
                print("Connection worked.")

                board.digital[self.dir_pin].write(Dir)

                while (count_Flag <= (pul-1)):
                    board.digital[self.pul_pin].write(1)
                    time.sleep(1e-4) # <---- Check this value
                    board.digital[self.pul_pin].write(0)
                    time.sleep(1e-4)
                    count_Flag += 1
            except:
                print("Board not connected to/detected by computer.")

    def IncDist(Type):
        self.incdist = float(input(f"Enter {Type} dist in cm: "))
        

def Setup():
        
    def SetJogDist():
        """Sets minimum jog distance. Same for all axes."""
        while True:
            try:
                jog_dist = float(input("Enter jog dist in cm: "))
                pul = X.pulseCalc(jog_dist)
                break
            except TypeError or StopIteration:
                print("Enter a valid value.")
        return pul

    def SetKeysMove():
        pulses = SetJogDist()
        while True:
            key_pressed = str(input(">> "))
            if key_pressed.lower() == "l":
                return False
                break
            elif key_pressed.lower() == "a":
                X.AxisMove(pulses, 0)
            elif key_pressed.lower() == "d":
                X.AxisMove(pulses, 1)
            elif key_pressed.lower() == "r":
                Y.AxisMove(pulses, 0)
            elif key_pressed.lower() == "f":
                Y.AxisMove(pulses, 1)
            elif key_pressed.lower() == "w":
                Z.AxisMove(pulses, 0)
            elif key_pressed.lower() == "s":
                Z.AxisMove(pulses, 1)
            else:
                pass
    
    while True:
        choose = str(input("1. Set the jog distance for all axes.\n2. Move the axes with \
the keyboard.\n3. Exit.\n"))  
        if choose == "1":
            SetJogDist()
        elif choose == "2":
            SetKeysMove()
        elif choose == "3":
            print("Exiting the setup phase.")
            break
        else:
            print("Invalid input. Try 1, 2 or 3.")
    
# Scan should go till about 6 apertures away for a solenoid. Try on-axis? Also
# find Bz and recreate the other components by Maxwell's equations.
def Scan():

    def GetRect():
        # Only need two points to define? Why I am using four?
        """Defines a rectangle in the Z=0 plane."""
        points = []
        print("Enter points in the form (X cm, Y cm). Do bottom-left point and top-right point.")
        for times in range(0, 2):
            X = input(f"Enter point {times+1} X coord: ")
            Y = input(f"Enter point {times+1} Y coord: ")
            points.append([X, Y])
        return points

    def StepDepth(): # CURRENTLY SAME DIST FOR ALL THREE AXES
        step_size = float(input("Enter the minimum distance to travel along each axis (cm): "))
        depth = float(input("Enter the max. depth to scan (cm): "))
        step_pulse = 
        return step_pulse, depth

    def ReadField():        # Work on talking to the probe and put all comms here
        # Code below is from test script; check if that works first!
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

    
    def DirFlag(iteration):
        if iteration == -1:
            return 0
        elif iteration == 1:
            return 1

    def DoScan():
        magnet_name = str(input("Enter magnet name: "))
        # Start with (0,0,0) and immediately move to lower left corner. Wait for 10 seconds and start scanning.
        # By Nathan's advice, I'm doing Y-Z plane and then X.

        left_X = points[0][0]
        right_X = points[1][0]
        bot_Y = points[0][1]
        top_Y = points[1][1]

        # Moving to the bottom left point.
        Y.AxisMove(bot_Y, Dir = 0) # Moves to the bottom
        X.AxisMove(left_X, Dir = 0) # Moves to the left
        
        curr_X = left_X
        curr_Y = bot_Y
        curr_Z = 0 # Change to a +ve Z value as we start BEFORE the Z=0 plane.

        flag = 0
        
        store_file = open(f"{magnet_name}_scan.txt", "a")
        
        while (curr_X <= right_X):
            while (curr_Y <= top_Y):
                while (abs.(curr_Z) <= depth):
                    iterator = (-1)**flag
                    field_val = ReadField()                                 # Read mag field value here from probe; make serial comm function
                    store_file.write(curr_X, curr_Y, curr_Z, field_val)     # Write coords+field values into a file here
                    print(f"({curr_X}, {curr_Y}, {curr_Z}, {field_val})")
                    Z.AxisMove(step_size, Dir = DirFlag(iterator))
                    curr_Z += step_size
                    flag += 1
                curr_Z = 0
                Y.AxisMove(step_size, Dir=1)
                curr_Y += step_size
            curr_Y = bot_Y
            X.AxisMove(step_size, Dir=1)
            curr_X += step_size

        # Close file here
        store_file.close()

        # <OLD CODE>
        """step_numpul, depth = StepDepth()

        # Adding another loop to do the negative side; this needs to bring the probe back to 0,0,0 as well
        times_looped = 0
        while (times_looped <= 1):
            if times_looped == 0:
                temp_X = right_X
            for X in range(0, temp_X + 1, ): # temp_X gets assigned to left_X or right_X depending on which part is being scanned
                for Y in range(bot_Y, top_Y + 1, ):
                    for Z in range(0, depth + 1, ):  # Start case different from this so watch out for that
                        # READING FUNCTION GOES HERE
                        AxisMove(step_pul, dir)
                    AxisMove(step_pul, dir)"""
        # <\OLD CODE>


print("Initialise X-axis")
X = axis()
X.setPins()
X.initSwitches()
print("Initialise Y-axis")
Y = axis()
Y.setPins()
Y.initSwitches()
print("Initialise Z-axis")
Z = axis()
Z.setPins()
Z.initSwitches()

while True:
    print("1. Setup Phase\n2. Scan Phase\n3. Test Phase\n Enter exit to leave.\n")
    choose = str(input("Choose (1/2/3): "))
    if choose == "1":
        Setup()
    elif choose == "2":
        Scan()
    elif choose == "3":
        Test()
    elif choose == "17":
        print("Hello! :3")
    elif choose.lower() == "exit" or choose.lower() == "quit":
        break
    else:
        print("Invalid choice.")
        print("1. Setup Phase\n2. Scan Phase\n3. Test Phase\n Enter exit to leave.")

