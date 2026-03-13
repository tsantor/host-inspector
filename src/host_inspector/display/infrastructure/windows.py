import ctypes
import ctypes.wintypes


class DisplayDevice(ctypes.Structure):
    _fields_ = [
        ("cb", ctypes.wintypes.DWORD),
        ("DeviceName", ctypes.c_wchar * 32),
        ("DeviceString", ctypes.c_wchar * 128),
        ("StateFlags", ctypes.wintypes.DWORD),
        ("DeviceID", ctypes.c_wchar * 128),
        ("DeviceKey", ctypes.c_wchar * 128),
    ]


class DevMode(ctypes.Structure):
    _fields_ = [
        ("dmDeviceName", ctypes.c_wchar * 32),
        ("dmSpecVersion", ctypes.wintypes.WORD),
        ("dmDriverVersion", ctypes.wintypes.WORD),
        ("dmSize", ctypes.wintypes.WORD),
        ("dmDriverExtra", ctypes.wintypes.WORD),
        ("dmFields", ctypes.wintypes.DWORD),
        ("dmOrientation", ctypes.wintypes.SHORT),
        ("dmPaperSize", ctypes.wintypes.SHORT),
        ("dmPaperLength", ctypes.wintypes.SHORT),
        ("dmPaperWidth", ctypes.wintypes.SHORT),
        ("dmScale", ctypes.wintypes.SHORT),
        ("dmCopies", ctypes.wintypes.SHORT),
        ("dmDefaultSource", ctypes.wintypes.SHORT),
        ("dmPrintQuality", ctypes.wintypes.SHORT),
        ("dmColor", ctypes.wintypes.SHORT),
        ("dmDuplex", ctypes.wintypes.SHORT),
        ("dmYResolution", ctypes.wintypes.SHORT),
        ("dmTTOption", ctypes.wintypes.SHORT),
        ("dmCollate", ctypes.wintypes.SHORT),
        ("dmFormName", ctypes.c_wchar * 32),
        ("dmLogPixels", ctypes.wintypes.WORD),
        ("dmBitsPerPel", ctypes.wintypes.DWORD),
        ("dmPelsWidth", ctypes.wintypes.DWORD),
        ("dmPelsHeight", ctypes.wintypes.DWORD),
        ("dmDisplayFlags", ctypes.wintypes.DWORD),
        ("dmDisplayFrequency", ctypes.wintypes.DWORD),
        ("dmICMMethod", ctypes.wintypes.DWORD),
        ("dmICMIntent", ctypes.wintypes.DWORD),
        ("dmMediaType", ctypes.wintypes.DWORD),
        ("dmDitherType", ctypes.wintypes.DWORD),
        ("dmReserved1", ctypes.wintypes.DWORD),
        ("dmReserved2", ctypes.wintypes.DWORD),
        ("dmPanningWidth", ctypes.wintypes.DWORD),
        ("dmPanningHeight", ctypes.wintypes.DWORD),
    ]


class WindowsDisplayCollector:
    def display_info(self) -> list[dict]:
        user32 = ctypes.windll.user32
        enum_display_devices = user32.EnumDisplayDevicesW
        enum_display_settings = user32.EnumDisplaySettingsW

        output = []
        index = 0
        while True:
            display_device = DisplayDevice()
            display_device.cb = ctypes.sizeof(display_device)
            if not enum_display_devices(None, index, ctypes.byref(display_device), 0):
                break
            if not display_device.DeviceName:
                index += 1
                continue

            devmode = DevMode()
            devmode.dmSize = ctypes.sizeof(devmode)
            if not enum_display_settings(
                display_device.DeviceName, -1, ctypes.byref(devmode)
            ):
                index += 1
                continue

            actual_width = devmode.dmPelsWidth
            actual_height = devmode.dmPelsHeight
            refresh_hz = devmode.dmDisplayFrequency
            pixel_width = devmode.dmPelsWidth
            pixel_height = devmode.dmPelsHeight

            output.append(
                {
                    "name": display_device.DeviceString,
                    "display_id": index,
                    "resolution_actual": (
                        f"{actual_width} x {actual_height}"
                        if actual_width and actual_height
                        else "--"
                    ),
                    "resolution": (
                        f"{pixel_width} x {pixel_height}"
                        if pixel_width and pixel_height
                        else "--"
                    ),
                    "refresh_rate": f"{refresh_hz} Hz" if refresh_hz else "--",
                }
            )
            index += 1

        return output
