"""
Script: run_card_creator_script.py
Description:
    Creates a new Run_Card UDT instance in Ignition based on user input from a Perspective screen.
    Also publishes essential metadata to an MQTT broker using UNS (Unified Namespace) structure.
"""

# These would come from the Perspective screen input fields
workorder = self.getSibling("txt_workorder").props.text
workstation = self.getSibling("txt_workstation").props.text
reporter = session.props.auth.user.username  # assumes user is logged in

# Tag path setup
base_path = "[default]RunCards"
tag_path = f"{base_path}/{workorder}"
udt_type = "Run_Card"

# Check if tag already exists
if not system.tag.exists(tag_path):
    system.tag.configure(
        base_path,
        [
            {
                "name": workorder,
                "type": "UDT_INST",
                "typeId": udt_type,
                "parameters": {},
                "attributes": {},
                "tags": []
            }
        ],
        overwrite=False
    )

# Write initial values
system.tag.writeBlocking([
    f"{tag_path}/workorder",
    f"{tag_path}/workstation",
    f"{tag_path}/reporter",
    f"{tag_path}/status",
    f"{tag_path}/start_time"
], [
    workorder,
    workstation,
    reporter,
    "in_work",
    system.date.now()
])

# OPTIONAL: Publish to MQTT (UNS structure)
mqtt_base = f"joby/santa-cruz/run_cards/{workorder}"
system.cirruslink.engine.publish(f"{mqtt_base}/status", "in_work")
system.cirruslink.engine.publish(f"{mqtt_base}/workstation", workstation)
system.cirruslink.engine.publish(f"{mqtt_base}/reporter", reporter)
