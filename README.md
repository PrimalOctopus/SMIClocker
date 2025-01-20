# SMIClocker
SMIClocker is a linux overclocking/system monitoring tool made in python that aims to support NVIDIA, AMD and INTEL gpu's!
Windows is currently supported for NVIDIA gpu's ONLY!

Current support:
nvidia-smi: Good, missing a few available features. Ability to set clocks, power limit and temp limit depends on GPU model.
rocm-smi (AMD gpu's): Barebones, setting core clocks and querying temp/power/utilisation supported. Many unsupported features, queries have excessive overhead.

Unsupported:
amd-smi: No support - currently have no device to test this on, it's interface is NOT the same as rocm-smi
xpu-smi (INTEL gpu's): No support - currently have no device to test this on

Nvidia quirks:
  
  GTX 10XX:
  Some (all?) Setting clocks unavailable through nvidia-smi
  
  Laptop:
  Some (all?) mobile gpu's don't allow you to set power limit and temp limit
