import time, sys
from gpu.gpu_nvidia_smi import GpuNvidiaSMI
from gpu.gpu_rocm_smi import GpuROCMSMI
from overlay.overlay import Window
from gpu.get_gpus import get_gpus

#get_gpus()

try:
    gpu = GpuNvidiaSMI()
except Exception as e:
    print(e)
    try:
        gpu = GpuROCMSMI()
    except:
        sys.exit("No gpu's detected")

try:
    if sys.argv[1] == "AMD":
        gpu = GpuROCMSMI()
except:
    pass

overlay = Window()

core, power, temp, usage = gpu.query("core.clock", "power", "core.temp", "core.usage")

default_clock = gpu.get_base_clock()
print("Base clock: " + default_clock)

model_text = overlay.add_text(gpu.name, 10)
stats_text = overlay.add_text(f"CORE TEMP: {temp}c\nCORE CLOCK: {core}mhz\nPOWER: {power}w\nUSAGE: {usage}", 15)

print(gpu.name)
print(gpu.vendor)
print(f"PCI: {gpu.pci_id}")
print(f"default core clock: {gpu.query("core.clock.limit")}")
gpu.set_core_clock(1500)
#gpu.reset_clocks()

while True:
    temp, clock, power, usage = gpu.query("core.temp", "core.clock", "power", "core.usage")
    overlay.change_text(stats_text, f"CORE TEMP: {temp}c\nCORE CLOCK: {clock}mhz\nPOWER: {power}w\nUSAGE: {usage}")
    if float(temp) > 58:
        print(f"Temps too high, dropping clock from! {gpu.core_clock_set}")
        gpu.set_core_clock(gpu.core_clock_set -25)
    time.sleep(2)
