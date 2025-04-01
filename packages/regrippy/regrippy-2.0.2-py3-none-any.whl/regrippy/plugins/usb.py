from regrippy import BasePlugin, PluginResult, mactime
from datetime import datetime


class Plugin(BasePlugin):
    """Lists USB drives connected to the computer"""

    __REGHIVE__ = "SYSTEM"

    def run(self):
        key = self.open_key(self.get_currentcontrolset_path() + "\\Enum\\USBSTOR")

        for usb in key.subkeys():
            for instance in usb.subkeys():
                r = PluginResult(key=instance)

                friendly_name = "???"
                for val in instance.values():
                    k = val.name()
                    v = val.value()
                    if k == "FriendlyName":
                        friendly_name = v
                        break

                r.custom={
                    "device": usb,
                    "friendly_name": friendly_name,
                    "vendor": usb.name().split("&Ven_")[1].split("&")[0],
                }
                yield r
    
    def display_human(self, r):
        d = datetime.fromtimestamp(r.mtime)
        print(f"[{r.key_name}] [{r.custom['vendor']}]: {r.custom['friendly_name']} (Last plugged in: {d})")

    def display_machine(self, r):
        print(mactime(mtime=r.mtime, name=f"[{r.key_name}] {r.custom['vendor']} {r.custom['friendly_name']}"))
