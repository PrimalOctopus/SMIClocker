import subprocess, csv
from gpu.gpu_vendor import GpuVendor, SMIException
from io import StringIO

class GpuROCMSMI(GpuVendor):
    """Class for handling AMD gpu's with ROCM

    Constructor
    -----------
    GpuROCMSMI(index: int = 0)
        Raises
        ------
            SMIException

    Methods
    -------
    query(*stats: str)
        Query gpu for current stats

    set_core_clock(max: int, min: int = 0)
        Set the core clock

    set_mem_clock(max: int, min: int = 0)
        Set the memory clock

    set_persistence_mode(flag: bool)
        Make nvidia driver persist even when not in use
    """

    def __init__(self, index: int = 0):
        if index >= gpu_count():
            raise SMIException(f"Index: {index} exceeds gpu_count: {gpu_count()}")

        self.index = index
        self.vendor = "AMD_ROCM"

        super().__init__()

        self.core_clock_set, self.mem_clock_set = self.query("core.clock.limit", "mem.clock.limit")

        #NEEDED TO SET CLOCKS
        self.core_clock_min = self.query("core.clock.min")

    def _runCLI(self, command, error = False):
        return runCLI(f"{command} -d {self.index}")

    def _query_smi(self, command, *keys):
        #print(f"{command} -d {self.index} --csv")

        r = runCLI(f"{command} --csv -d {self.index}")

        data = next(csv.DictReader(StringIO(r)))

        data_list = []
        for key in keys:
            data_list.append(data[key])

        return data_list if len(data_list) > 1 else data_list[0]

    def query(self, *stats: str):
        """Query gpu for current stats
        
        Parameters
        ----------
        *stats : str

            The stats to query:

                core.clock, core.temp, core.clock.limit
                mem.clock, mem.temp, mem.clock.limit
                power, power.average, power.instant,
                name, pci_id

        Returns
        -------
        tuple
        
            A tuple of str containing queried values
        """

        query = ""
        results = []
        for stat in stats:
            match stat:
                #Core
                case "core.clock":
                    results.append(self._query_smi("-c", "sclk clock speed:")[1:-4])
                case "core.temp":
                    results.append(self._query_smi("-t", "Temperature (Sensor edge) (C)"))
                case "core.temp.limit":
                    query += "temperature.gpu.tlimit,"
                case "core.clock.limit":
                    results.append(self._query_smi("--showsclk", "Valid sclk range").split(" - ")[1][:-3])
                case "core.clock.min":
                    results.append(self._query_smi("--showsclk", "Valid sclk range").split(" - ")[0][:-3])
                case "core.usage":
                    query += "utilization.gpu,"

                #SM
                case "sm.clock":
                    query += "clocks.sm,"
                case "sm.clock.limit":
                    query += "clocks.max.sm,"

                #Mem
                case "mem.clock":
                    query += "clocks.mem,"
                case "mem.temp":
                    query += "temperature.mem,"
                case "mem.clock.limit":
                    results.append(self._query_smi("--showmclk", "Valid mclk range").split(" - ")[0][:-3])
                case "mem.total":
                    query += "memory.total,"
                case "mem.used":
                    query += "memory.used,"
                case "mem.free":
                    query += "memory.free,"
                case "mem.reserved":
                    query += "mem.reserved,"

                #Power
                case "power":
                    results.append(self._query_smi("-P", "Current Socket Graphics Package Power (W)"))
                case "power.average":
                    query += "power.draw.average,"
                case "power.instant":
                    query += "power.draw.instant,"
                case "power.limit.max":
                    query += "power.max_limit,"
                case "power.limit.min":
                    query += "power.min_limit,"
                case "power.limit.default":
                    query += "power.default_limit,"
                case "power.limit":
                    query += "power.limit,"
                case "power.limit.enforced":
                    query += "enforced.power.limit,"
                case "power.management":
                    query += "power.management,"

                #Fan
                case "fan.speed":
                    query += "fan.speed,"

                #Utilization
                case "utilization.jpeg":
                    query += "utilization.jpeg,"
                case "utilization.ofa":
                    query += "utilization.ofa,"
                case "utilization.decoder":
                    query += "utilization.decoder,"
                case "utilization.memory":
                    query += "utilization.memory,"
                case "utilization.gpu":
                    query += "utilization.gpu,"

                #throttle
                case "throttle.supported":
                    query += "clocks_throttle_reasons_supported,"
                case "throttle.active":
                    query += "clocks_throttle_reasons_active,"
                case "throttle.idle":
                    query += "clocks_throttle_reasons.gpu_idle,"
                case "throttle.application":
                    query += "clocks_event_reasons.applications_clocks_setting,"
                case "throttle.sw.power":
                    query += "clocks_throttle_reasons.sw_power_cap,"
                case "throttle.sw.thermal":
                    query += "clocks_throttle_reasons.sw_thermal_slowdown,"
                case "throttle.hw.thermal":
                    query += "clocks_throttle_reasons.hw_thermal_slowdown,"
                case "throttle.hw.power":
                    query += "clocks_throttle_reasons.hw_power_brake_slowdown,"
                case "pstate":
                    query += "pstate,"

                #Identification
                case "count":
                    query += "count,"
                case "name":
                    results.append(self._query_smi("-i", "Device Name"))
                case "pci_id":
                    results.append(self._query_smi("--showbus", "PCI Bus"))
                case "vbios":
                    query += "vbios_version,"
                case "index":
                    query += "index,"
                case "uuid":
                    query += "uuid,"
                case "serial":
                    query += "serial,"
                case "driver":
                    query += "driver_version,"

                #ECC
                case "ecc.mode":
                    query += "ecc.mode.current,"
                case "ecc.mode.pending":
                    query += "ecc.mode.pending,"
                case "ecc.corrected.total":
                    query += "ecc.errors.corrected.aggregate.total,"
                case "ecc.uncorrected.total":
                    qery += "ecc.errors.uncorrected.aggregate.total,"

                #Encoder
                case "encoder.sessions":
                    query += "encoder.stats.sessionCount,"
                case "encoder.FPS":
                    query += "encoder.stats.averageFps,"
                case "encoder.latency":
                    query += "encoder.stats.averageLatency,"

                #PCIE
                case "pcie.gen.current":
                    query += "pcie.link.gen.gpucurrent,"
                case "pcie.gen.max":
                    query += "pcie.link.gen.max,"
                case "pcie.gen.gpu":
                    query += "pcie.link.gen.gpumax,"
                case "pcie.gen.host":
                    query += "pcie.link.gen.hostmax,"
                case "pcie.width.current":
                    query += "pcie.link.width.current,"
                case "pcie.width.max":
                    query += "pcie.link.width.max,"


                #Other
                case "persist":
                    query += "persistance_mode,"
                case "display.mode":
                    query += "display_mode,"
                case "display.active":
                    query += "display.active,"
                case "time":
                    query += "timestamp,"

        if len(results) == 1:
            return results[0]
        else:
            return (*results,)

    def set_core_clock(self, max_clock, min_clock = 0):
        if min_clock == 0:
            min_clock = self.core_clock_min
        self.assure_int(max_clock, min_clock)

        stdout = self._runCLI(f"-setsrange {min_clock} {max_clock} --autorespond y")
        self.core_clock_set = int(max_clock)
        return stdout

    def set_mem_clock(self, max_clock, min_clock = 0):
        self.assure_int(max_clock, min_clock)

        stdout = self._runCLI(f"-lmc {min_clock},{max_clock}")
        self.mem_clock_set = int(max_clock)

        return stdout

    def reset_core_clock(self):
        return self._runCLI("-r")

    def reset_mem_clock(self):
        return self._runCLI("-r")

    def set_temp_target(self, target):
        self.assure_int(target)
        return self._runCLI("-gtt {target}", error=True)

    def set_persistence_mode(self, flag: bool):
        try:
            assert 0 <= flag <= 1
        except:
            raise ValueError("persistence mode must be a bool")
        subprocess.run(f"nvidia-smi -pm {flag}")

    def get_base_clock(self):
        return self._query_smi("--showsclk", "Valid sclk range").split(" - ")[1][:-3]

def gpu_count():
    return runCLI("--showbus --csv").count("\n")
    
def runCLI(command, error = False):
    try:
        r = subprocess.run(f"rocm-smi {command}", shell = True, capture_output = True, text = True, check = True)
    except subprocess.CalledProcessError as e:
        raise SMIException(e.stdout)
    return r.stdout.strip()