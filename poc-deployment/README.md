# 🏁 POC Deployment Instructions: Run_Card + UNS + Kanban Board

This doc provides everything needed to deploy the full proof-of-concept into your Ignition environment using the GitHub POC files.

---

## 📁 Folder Location (Recommend in Repo Root)



---

## ✅ Step-by-Step Deployment

### 1. 🔧 Import UDTs
- In Ignition Designer:
  - Open Tag Browser
  - Right-click `[default]` → **Import Tag**
  - Select `Run_Card.json`
  - Verify folder: `[default]/RunCards` is created

---

### 2. 🖥️ Import Perspective Views
- Go to Perspective → Views
- Import the following:
  - `RunCardDisplay.json`
  - `WorkcenterColumn.json`
  - `kanban_board_base_layout.json`

---

### 3. 🧠 Add Gateway/Project Scripts
Place the following in the appropriate script areas:

#### Project Library (recommended path: `project.scripts.run_cards`):
- `run_card_creator_script.py`
- `run_card_queue_by_workcenter.py`
- `get_kanban_instances.py`

> These feed the logic for creating and rendering the Kanban board dynamically.

---

### 4. 🧪 Run Sample Creator Script
- Open **Tools → Script Console**
- Paste and run `create_sample_run_cards.py` to create test data:
  - `MFID001`, `MFID002`, etc.
- Tag path: `[default]/RunCards/MFID001/...`

---

### 5. 🧼 Wire Main Perspective Screen
- Make a new screen called `RunCardBoard`
- Drop a **View Canvas or Embedded View** component
- Set it to use `kanban_board_base_layout`
- Pass in workflow order param:
```json
["Cutting", "Layup", "Assembly", "Inspection"]

---

### 🧠 Bonus: Dynamic Workstation → Workcenter Mapping

This POC includes support for **auto-assigning workcenters** based on scanned or typed workstation IDs.

- **Mapping Tag**: `[default]/WorkstationMap` (Memory Tag with dataset)
- **Mapping UI View**: `WorkstationMappingEditor.json`
- **Used In Script**: `run_card_creator_script.py`

To configure:
1. Open the `WorkstationMappingEditor` view in Perspective
2. Edit the workstation → workcenter table directly
3. Click **Save Changes** to update the mapping in real time

✅ The `run_card_creator_script` will automatically use this mapping to assign the correct workcenter to each Run_Card.

> This eliminates manual input and makes the system more scalable, consistent, and future-proof.

---

## ✅ Final Notes
- You can trigger the `run_card_creator_script` from your scan form to auto-instantiate UDTs
- This structure is ready for MQTT publishing using Unified Namespace principles
- To publish to MQTT, add `system.cirruslink.engine.publish()` calls inside `run_card_creator_script`

---

