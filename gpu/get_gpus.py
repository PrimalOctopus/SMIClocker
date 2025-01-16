import gpu.gpu_nvidia_smi as nv
import gpu.gpu_rocm_smi as rocm

def get_gpus():
    nvidia = {
        "count" : nv.gpu_count(),
        "gpus" : [],
    }

    for i in range(0, nvidia["count"]):
        nvidia["gpus"].append(nv.GpuNvidiaSMI(i))

    amd = {
        "count" : rocm.gpu_count(),
        "gpus" : [],
    }

    for i in range(0, amd["count"]):
        amd["gpus"].append(rocm.GpuROCMSMI(i))

    print(nvidia)
    print(amd)