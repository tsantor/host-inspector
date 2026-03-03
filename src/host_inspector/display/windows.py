import ctypes
import ctypes.wintypes


def get_display_info() -> list[dict]:
    """
    Returns display info for Windows using EnumDisplayDevices and
    EnumDisplaySettings.
    """
    user32 = ctypes.windll.user32
    enum_display_devices = user32.EnumDisplayDevicesW
    enum_display_settings = user32.EnumDisplaySettingsW

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

    out = []
    i = 0
    while True:
        dd = DisplayDevice()
        dd.cb = ctypes.sizeof(dd)
        if not enum_display_devices(None, i, ctypes.byref(dd), 0):
            break
        if not dd.DeviceName:
            i += 1
            continue
        devmode = DevMode()
        devmode.dmSize = ctypes.sizeof(devmode)
        if not enum_display_settings(dd.DeviceName, -1, ctypes.byref(devmode)):
            i += 1
            continue
        name = dd.DeviceString
        display_id = i
        act_w = devmode.dmPelsWidth
        act_h = devmode.dmPelsHeight
        hz = devmode.dmDisplayFrequency
        px_w = devmode.dmPelsWidth
        px_h = devmode.dmPelsHeight
        resolution_actual = f"{act_w} x {act_h}" if act_w and act_h else "--"
        resolution = f"{px_w} x {px_h}" if px_w and px_h else "--"
        refresh_rate = f"{hz} Hz" if hz else "--"
        out.append(
            {
                "name": name,
                "display_id": display_id,
                "resolution_actual": resolution_actual,
                "resolution": resolution,
                "refresh_rate": refresh_rate,
            }
        )
        i += 1
    return out
