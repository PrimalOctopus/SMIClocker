import gpu.gpu_nvidia_smi as nv

def get_gpus():
    nvidia = {
        "count" : nv.gpu_count(),
        "gpus" : [],
    }

    for i in range(0, nvidia["count"]):
        nvidia["gpus"].append(nv.GpuNvidiaSMI(i))

    amd = {
        #"count" : amd.gpu_count(),
        "gpus" : [],
    }

    print(nvidia)