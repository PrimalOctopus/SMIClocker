import os
import sys

def main():
    getGpus()
    getBaseClock()
    while True:
        minCore = "210"
        maxCore = str(getInt("Enter max gpu clock (mhz): "))
        f = setClock(minCore, maxCore)
        print(f)
        getBaseClock()
        gpuStatus()

def getInt(prompt):
    while True:
        try:
            return int(input(prompt))
        except EOFError:
            sys.exit("Goodbye")
        except:
            pass

def setClock(min, max):
    res = os.system("sudo nvidia-smi -i 0 -lgc " + min + "," + max)
    return res

def getBaseClock():
    print(os.system("nvidia-smi base-clocks -i 0"))

def getGpus():
    print(os.system("nvidia-smi -L"))

def getSupportedClocks():
    core = os.system("nvidia-smi --query-supported-clocks gr --format=csv,noheader,nounits")
    mem = os.system("nvidia-smi --query-supported-clocks mem --format=csv,noheader,nounits")


def gpuStatus():
    print(os.system("nvidia-smi dmon -s pc"))
#-L list all gpu's
#-B list excluded gpu's 
#-gtt target temp
#-lmc lock memory clock
#-pl powerlimit
#-rac reset app clocks
#-ac set app clocks
#-rgc reset gpu clocks
#-rmc reset mem clocks
#-r reset gpu
#-pm toggle persistance mode 0/1

#-q CLOCK POWER TEMPERATURE UTILIZATION PERFORMANCE

if __name__ == "__main__":
    main()
