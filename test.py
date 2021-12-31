import pyfirmata as fir
import time, pickle

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
                self.pul_pin = 0
                self.dir_pin = 1
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

    def setDir(self):
        while True:
            if self.Dir == None:
                self.Dir = str(input("Enter direction (+/-): "))
            if self.Dir == "+":
                return 1
                break
            elif self.Dir == "-":
                return 0
                break
            else:
                print(f"{self.Dir} is not a valid input. Try +/-.")
                self.Dir = str(input("Enter direction (+/-): "))
                
    def onePulse(self):
        pitch = 0.957 # (cm) double start, so this is really pitch * 2
        one_pulse = pitch/(self.pulperrev) # gives cm/pulse
        return one_pulse
    
    def pulseCalc(self):
        if self.dim in ["x", "y", "z"]:
            print(f"Current {self.dim} distance: {self.current_dist} cm.")
            dist_to_go = float(input("Dist (cm) to go to? "))
            balance = (self.current_dist - dist_to_go)
            self.current_dist = dist_to_go
        else:
            print("Invalid input.")
            self.setPins()
        if balance < 0:
            self.setDir()
            num_pulse = abs(balance)/(self.onePulse())
        elif balance >= 0:
            self.setDir()
            num_pulse = balance/(self.onePulse())
        return num_pulse

    def setStop(self):
        if self.dim == "x" or self.dim == "y":
            self.stop = 86.36
        elif self.dim == "z":
            self.stop = 0
        else:
            print("Invalid dimension assigned to axis.")
            self.setPins()

    def AxisMove(self, pul):
        count_Flag = 0

        if __name__ == "__main__":
            board = fir.Arduino(
                "/dev/tty.usbmodem141101")
            print("Connection worked.")

            board.digital[self.dir_pin].write(self.setDir())

            while (count_Flag <= pul):
                board.digital[self.pul_pin].write(1)
                time.sleep(1e-9)
                board.digital[self.pul_pin].write(0)
                time.sleep(1e-9)
                count_Flag += 1

print("Zero point of axis starts from the end without the motor.")
print("------X-axis initialization-------")
X = axis()
X.setPins()
X.initSwitches()
X.setDir()
X.setStop()

print("------Y-axis initialization-------")
Y = axis()
Y.setPins()
Y.initSwitches()
Y.setDir()
Y.setStop()

print("------Z-axis initialization-------")
Z = axis()
Z.setPins()
Z.initSwitches()
Z.setDir()
Z.setStop()

def main():
    """def CreateAxes():
        print("Zero point of axis starts from the end without the motor.")
        print("------X-axis initialization-------")
        X = axis()
        X.setPins()
        X.initSwitches()
        X.setDir()
        X.setStop()

        print("------Y-axis initialization-------")
        Y = axis()
        Y.setPins()
        Y.initSwitches()
        Y.setDir()
        Y.setStop()

        print("------Z-axis initialization-------")
        Z = axis()
        Z.setPins()
        Z.initSwitches()
        Z.setDir()
        Z.setStop()
        """
        
    def AxisMoveSave():
        axis_choose = str(input("Axis to move? (X/Y/Z) "))
        if axis_choose.lower() == "x":
            pul = X.pulseCalc()
            with open("X_pos.dat", "wb") as file:
                pickle.dump(X, file)
            X.ever_saved = 1
            X.AxisMove(pul)

        elif axis_choose.lower() == "y":
            pul = Y.pulseCalc()
            with open("Y_pos.dat", "wb") as file:
                pickle.dump(Y, file)
            Y.ever_saved = 1
            Y.AxisMove(pul)

        elif axis_choose.lower() == "z":
            pul = Z.pulseCalc()
            with open("Z_pos.dat", "wb") as file:
                pickle.dump(Z, file)
            Z.ever_saved = 1
            Z.AxisMove(pul)
            
    def AxisLoadSave():
        axis_choose = str(input("Axis to load? (X/Y/Z) "))
        if axis_choose.lower() == "x":
            saveX = open("X_pos.dat", "rb")
            while True:
                try:
                    X = pickle.load(saveX)
                    print(vars(X))
                    break
                except EOFError:
                    print("No X_pos file found.")
                    break
            saveX.close()
            
        elif axis_choose.lower() == "y":
            saveY = open("Y_pos.dat", "rb")
            while True:
                try:
                    Y = pickle.load(saveY)
                    vars(Y)
                    break
                except EOFError:
                    print("No Y_pos file found.")
                    break
            saveY.close()
                
        elif axis_choose.lower() == "z":
            saveZ = open("Z_pos.dat", "rb")
            while True:
                try:
                    Z = pickle.load(saveZ)
                    vars(Z)
                    break
                except EOFError:
                    print("No Z_pos file found.")
                    break
            saveZ.close()
                
    print("Primitive Gantry UI - by Robin")
    
    while True:
        print("1: Move axes\n2: Load axis from save.")
        choose = str(input("Option (1/2): "))
        if choose == "0":
            CreateAxes()
        elif choose == "1":
            AxisMoveSave()
        elif choose == "2":
            AxisLoadSave()
        elif choose.lower() == "exit":
            break
        else:
            print("Invalid choice.")

#main()
