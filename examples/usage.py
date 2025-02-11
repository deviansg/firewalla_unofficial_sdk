from firewalla_unofficial_sdk import Firewalla

def main():
    API_KEY = "YOUR_API_KEY"
    MSP_SUBDOMAIN = "YOUR_MSP_SUBDOMAIN"
    QUERY = "YOUR_QUERY"
    BOX_ID = "YOUR_BOX_ID"
    RULE_ID = "YOUR_RULE_ID"
    ALARM_ID = "YOUR_ALARM_ID"
    GROUP_ID = "YOUR_GROUP_ID"
    GROUP_BY = "YOUR_GROUP_BY"
    OWNER_ID = "YOUR_OWNER_ID"

    firewalla = Firewalla(api_key=API_KEY, firewalla_msp_subdomain=MSP_SUBDOMAIN)

    alarms = firewalla.get_alarms(params={"query": QUERY, "groupBy": GROUP_BY, "limit": 10})
    print("Alarms:", alarms)

    alarm = firewalla.get_alarm(box_id=BOX_ID, alarm_id=ALARM_ID)
    print("Alarm:", alarm)

    delete_alarm = firewalla.delete_alarm(box_id=BOX_ID, alarm_id=ALARM_ID)
    print("Alarm deleted:", delete_alarm)

    # Rules
    resume_rule = firewalla.resume_rule(id=RULE_ID)
    print("Rule started:", resume_rule)

    pause_rule = firewalla.pause_rule(id=RULE_ID)
    print("Rule stopped:", pause_rule)

    # Flows
    get_flows = firewalla.get_flows(params={"query": QUERY, "groupBy": GROUP_BY, "limit": 10})
    print("Flows:", get_flows)

    # Target List
    target_lists = firewalla.get_target_lists()
    print("Target Lists:", target_lists[0]["id"])

    target_list = firewalla.get_target_list(id=target_lists[0]["id"])
    print("Target List:", target_list)

    new_target_list = firewalla.create_target_list(
        name="Example Target List", 
        targets=["example.com", "example.org"], 
        category="ad", 
        owner=OWNER_ID,
        notes="This is an example target list."
    )

    if new_target_list is list:
        new_target_list = new_target_list[0]
        if new_target_list is dict and hasattr(new_target_list, "id"):
            new_target_list = new_target_list["id"]
            print("Get Target List:", new_target_list)
            update_target_list = firewalla.update_target_list(
                id=new_target_list[0]["id"], 
                data={
                    "name": "Test Target List Updated", 
                    "targets": ["foo.com", "bar.com"], 
                    "category": "vpn",
                    "notes": "This is a test target list updated"
                    }
                )
            print("Updated Target List:", update_target_list)
            delete_target_list = firewalla.delete_target_list(id=new_target_list[0]["id"])
            print("Deleted Target List:", delete_target_list)
        else:
            print("Target List not found")
    else:
        print(new_target_list)

    # Devices
    devices = firewalla.get_devices()
    print("Devices:", devices)

    # Stats
    stats = firewalla.get_stats(type="topBoxesByBlockedFlows", params={"group": GROUP_ID, "limit": 10})
    print("Stats:", stats)

    simple_stats = firewalla.get_simple_stats(params={"group": GROUP_ID, "limit": 10})
    print("Simple Stats:", simple_stats)

    # Additional Trends
    flow_trends = firewalla.get_flow_trends()
    print("Flow Trends:", flow_trends)

    alarm_trends = firewalla.get_alarm_trends()    
    print("Alarm Trends:", alarm_trends)
    
    rule_trends = firewalla.get_rule_trends()
    print("Rule Trends:", rule_trends)

if __name__ == "__main__":
    main()

