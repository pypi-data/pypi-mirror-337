from .bmp_management_base import BMPManagementBase

class ManureSpringApplicationRatherThanFallApplicationManagement(BMPManagementBase):
    """Distribution Table for BMP: Spring application rather than fall application (24)"""
    def __init__(self):
        super().__init__()
        self.StartYear = 1900
        self.StartMon = 1 
        self.StartDay = 1
        self.EndYear = 2100
        self.EndMon = 12
        self.EndDay = 31
        self.IsAnnually = 1
