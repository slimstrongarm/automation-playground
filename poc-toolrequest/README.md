# 🛠️ Tool Request POC: Ignition + Unified Namespace

This proof-of-concept (POC) enables tracking of Tool/Mold requests in a factory using Ignition and Unified Namespace (UNS) principles. Operators can submit requests and tooling teams can respond, all while data is structured, visible, and MQTT-ready.

---

## 📁 Folder Contents (`poc-toolrequest/`)

```
/ToolRequestForm.json           ← Perspective view for submitting tool requests
/ToolRequestQueue.json          ← Perspective view for tooling team queue
/submit_request.py              ← Script to create Tool_Request tag + publish to MQTT
/mark_ready.py                  ← Script to mark a tool as ready with return info
```

---

## ✅ Step-by-Step Deployment Instructions

### 1. 🔧 Import the `Tool_Request` UDT
- Open Ignition Designer
- Go to the Tag Browser
- Right-click `[default]` → **Import Tags**
- Import the `Tool_Request.json` file (you may need to create this UDT based on your schema if not provided)
- Confirm tag folder: `[default]/ToolRequests` is created

### 2. 🖥️ Import Perspective Views
- Go to Perspective → Views
- Import:
  - `ToolRequestForm.json`
  - `ToolRequestQueue.json`

### 3. 🧠 Add Project Scripts
Place these scripts in the appropriate project library path:
- `submit_request.py` → `project.scripts.tool_request_creator`
- `mark_ready.py` → `project.scripts.tool_request_actions`

> These scripts power UDT creation and status transitions, and publish to MQTT topics in a UNS structure.

### 4. 🧪 Test It!
- Open the `ToolRequestForm` screen as an operator
- Submit a request with Tool ID, priority, and due time
- Open the `ToolRequestQueue` screen as tooling team
- Enter the "Ready Location" and click **Mark Ready**

✅ Tags are created under `[default]/ToolRequests/{tool_id}`
✅ MQTT publishes to `joby/santa-cruz/tooling/requests/{tool_id}/...`

---

## 🧩 MQTT UNS Topics Used

Tool request data is published to:
```
joby/santa-cruz/tooling/requests/{tool_id}/status
joby/santa-cruz/tooling/requests/{tool_id}/priority
joby/santa-cruz/tooling/requests/{tool_id}/requested_by
joby/santa-cruz/tooling/requests/{tool_id}/due_time
joby/santa-cruz/tooling/requests/{tool_id}/location
```

---

## 🧰 Optional Enhancements
- Add QR code scanning for Tool ID
- Display tool preview image dynamically
- Add notifications via Slack or SMS from Ignition alarms or MQTT
- Log tooling history to a database or cloud for traceability

---

Let’s go make tool tracking real. 🔩🚀

