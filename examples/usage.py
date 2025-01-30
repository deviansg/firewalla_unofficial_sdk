from firewalla_unofficial_sdk import Firewalla

firewalla = Firewalla(api_key="71617eb22fa427629de9bc426a685822", firewalla_msp_subdomain="dn-kovnxj")

boxes = firewalla.get_boxes()
print(boxes)

flows = firewalla.get_flows()
print(flows)

devices = firewalla.get_devices(group="8", box="1")
print(devices)