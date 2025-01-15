class GpuVendor:
    """
        base class for handling interaction with gpu driver
    """

    vendor = None
    name = None
    pci_id = None
    core_clock_set = None
    mem_clock_set = None

    def __init__(self):
        """
            Grab GPU info
        """
        self.name, self.pci_id = self.query("name", "pci_id")

    def get_card_name(self):
        """
            Replace with vendor specific implementation
        """
        return "novideo"

    def get_core_clock(self):
        """
            Replace with vendor specific implementation
        """
        raise NotImplementedError()

    def get_mem_clock(self):
        """
            Replace with vendor specific implementation
        """
        raise NotImplementedError()

    def set_core_clock(self):
        """
            Replace with vendor specific implementation
        """
        raise NotImplementedError()

    def set_mem_clock(self):
        """
            Replace with vendor specific implementation
        """
        raise NotImplementedError()

    def get_supported_mem_clocks(self):
        """
            Replace with vendor specific implementation
        """
        raise NotImplmentedError()

    def get_supported_core_clocks(self):
        """
            Replace with vendor specific implementation
        """
        raise NotImplmentedError()

    def reset_core_clock(self):
        """
            Replace with vendor specific implementation
        """
        raise NotImplmentedError()

    def reset_mem_clock(self):
        """
            Replace with vendor specific implementation
        """
        raise NotImplmentedError()

    def reset_clocks(self):
        """
            Reset core and memory clocks to default
        """
        self.reset_core_clock()
        self.reset_mem_clock()

    def assure_int(self, *a):
        """
            Raises exception if any arg is not an int
        """
        try:
            for i in a:
                int(i)
        except:
            raise ValueError("attemted to input non integer value")

