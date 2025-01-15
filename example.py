import time
from gpu.gpu_nvidia_smi import GpuNvidiaSMI
from overlay.overlay import Window
from gpu.get_gpus import get_gpus

get_gpus()

gpu = GpuNvidiaSMI()
overlay = Window()

core, power, temp = gpu.query("core.clock", "power", "core.temp")

default_clock = gpu.get_base_clock()
print("Base clock: " + default_clock)

model_text = overlay.add_text(gpu.name, 10)
stats_text = overlay.add_text(f"CORE TEMP: {temp}c\nCORE CLOCK: {core}mhz\nPOWER: {power}w", 15)

print(gpu.name)
print(gpu.vendor)
print(f"PCI: {gpu.pci_id}")
print(f"default core clock: {gpu.query("core.clock.limit")}")
gpu.set_core_clock(1500)
gpu.reset_clocks()

while True:
    temp, clock, power = gpu.query("core.temp", "core.clock", "power")
    overlay.change_text(stats_text, f"CORE TEMP: {temp}c\nCORE CLOCK: {clock}mhz\nPOWER: {power}w")
    if float(power) > 45:
        print(f"Temps too high, dropping clock from! {gpu.core_clock_set}")
        gpu.set_core_clock(gpu.core_clock_set -25)
    time.sleep(2)
