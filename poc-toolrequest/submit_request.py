"""
Script: submit_request.py
Description:
    Called from the ToolRequestForm Perspective view.
    Instantiates a new Tool_Request UDT in the Ignition tag provider
    and publishes request details to the MQTT Unified Namespace (UNS).
"""

# Get user inputs from Perspective components
tool_id = self.getSibling("txt_tool_id").props.text
priority = self.getSibling("dropdown_priority").props.value
due_time = self.getSibling("due_time_picker").props.value
notes = self.getSibling("txt_notes").props.text
requested_by = session.props.auth.user.username
requested_time = system.date.now()

# Tag path setup
base_path = "[default]/ToolRequests"
tag_path = f"{base_path}/{tool_id}"
udt_type = "Tool_Request"

# Create UDT instance if it doesn't exist
if not system.tag.exists(tag_path):
    system.tag.configure(
        base_path,
        [
            {
                "name": tool_id,
                "type": "UDT_INST",
                "typeId": udt_type,
                "parameters": {},
                "attributes": {},
                "tags": []
            }
        ],
        overwrite=False
    )

# Write initial tag values
system.tag.writeBlocking([
    f"{tag_path}/tool_id",
    f"{tag_path}/priority",
    f"{tag_path}/status",
    f"{tag_path}/requested_by",
    f"{tag_path}/requested_time",
    f"{tag_path}/due_time",
    f"{tag_path}/location",
    f"{tag_path}/notes"
], [
    tool_id,
    priority,
    "requested",
    requested_by,
    requested_time,
    due_time,
    "Pending",
    notes
])

# Publish request to MQTT Unified Namespace
mqtt_base = f"joby/santa-cruz/tooling/requests/{tool_id}"
system.cirruslink.engine.publish(f"{mqtt_base}/status", "requested")
system.cirruslink.engine.publish(f"{mqtt_base}/priority", priority)
system.cirruslink.engine.publish(f"{mqtt_base}/requested_by", requested_by)
system.cirruslink.engine.publish(f"{mqtt_base}/due_time", str(due_time))
