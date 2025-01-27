[![codecov](https://codecov.io/gh/deviansg/firewalla_unofficial_sdk/graph/badge.svg?token=8NB3DUUXOW)](https://codecov.io/gh/deviansg/firewalla_unofficial_sdk)

![Build](https://github.com/deviansg/firewalla_unofficial_sdk/actions/workflows/ci.yml/badge.svg)

# Unofficial Firewalla SDK

A simple Python-based SDK for Firewalla. All methods are based on the Firewalla API documentation found here: https://docs.firewalla.net/

The above assumes that you are using Firewalla's MSP service as you will need it to use the API.

All functionality is within one file: firewalla.py making it pretty simple to use.

## Examples:

```
from firewalla import Firewalla

# Initialize the Firewalla instance
firewalla = Firewalla(api_key="your_api_key", firewalla_msp_subdomain="your_firewalla_msp_subdomain")

# Example usage of get_alarms
alarms = firewalla.get_alarms()
print("Alarms:", alarms)

# Example usage of get_alarm
alarm = firewalla.get_alarm(box_id="your_box_id", alarm_id="your_alarm_id")
print("Alarm:", alarm)

# Example usage of delete_alarm
delete_alarm_response = firewalla.delete_alarm(box_id="your_box_id", alarm_id="your_alarm_id")
print("Delete Alarm Response:", delete_alarm_response)

# Example usage of pause_rule
pause_rule_response = firewalla.pause_rule(id="your_rule_id")
print("Pause Rule Response:", pause_rule_response)

# Example usage of resume_rule
resume_rule_response = firewalla.resume_rule(id="your_rule_id")
print("Resume Rule Response:", resume_rule_response)

# Example usage of get_flows
flows = firewalla.get_flows(params={"query": "example_query", "groupBy": "example_group", "sortBy": "example_sort", "limit": 10, "cursor": "example_cursor"})
print("Flows:", flows)

# Example usage of get_target_lists
target_lists = firewalla.get_target_lists()
print("Target Lists:", target_lists)

# Example usage of get_target_list
target_list = firewalla.get_target_list(id="your_target_list_id")
print("Target List:", target_list)

# Example usage of delete_target_list
delete_target_list_response = firewalla.delete_target_list(id="your_target_list_id")
print("Delete Target List Response:", delete_target_list_response)
```
