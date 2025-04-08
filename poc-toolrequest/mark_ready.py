"""
Script: mark_ready.py
Description:
    Called from the ToolRequestQueue view when a tool is marked as ready.
    Updates the Tool_Request UDT instance with the return time and location.
    Also publishes the status and location to the MQTT Unified Namespace.
"""

def mark_ready(tool_id, location):
    tag_path = f"[default]/ToolRequests/{tool_id}"

    # Write updated values to the tag
    system.tag.writeBlocking([
        f"{tag_path}/status",
        f"{tag_path}/return_time",
        f"{tag_path}/location"
    ], [
        "ready",
        system.date.now(),
        location
    ])

    # Publish updates to MQTT (UNS)
    mqtt_base = f"joby/santa-cruz/tooling/requests/{tool_id}"
    system.cirruslink.engine.publish(f"{mqtt_base}/status", "ready")
    system.cirruslink.engine.publish(f"{mqtt_base}/location", location)
