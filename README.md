# Unofficial Firewalla SDK

A simple Python-based SDK for Firewalla. All methods are based on the Firewalla API documentation found here: https://docs.firewalla.net/

The above assumes that you are using Firewalla's MSP service as you will need it to use the API.

All functionality is within one file: firewalla.py making it pretty simple to use.

### Examples:

```
from firewalla import Firewalla

# Initialize the Firewalla instance
firewalla = Firewalla(api_key="your_api_key", firewalla_msp_subdomain="your_firewalla_msp_subdomain")

# Get alarms
alarms = firewalla.get_alarms()

# Get a specific alarm
alarm = firewalla.get_alarm(box_id="your_box_id", alarm_id="your_alarm_id")

# Delete an alarm
response = firewalla.delete_alarm(box_id="your_box_id", alarm_id="your_alarm_id")

# Pause a rule
response = firewalla.pause_rule(id="your_rule_id")

# Resume a rule
response = firewalla.resume_rule(id="your_rule_id")

# Get flows
flows = firewalla.get_flows()

# Get target lists
target_lists = firewalla.get_target_lists()

# Get a specific target list
target_list = firewalla.get_target_list(id="your_target_list_id")
```

If you run into any problems feel free to open an issue.
