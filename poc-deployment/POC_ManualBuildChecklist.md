# 🧱 Manual Build Checklist – Run Card POC (Ignition Perspective)

This guide helps you manually recreate the three core views in Ignition Designer in case JSON import fails. These views support Run Card creation, display, and dynamic Kanban board layout.

---

## 1️⃣ Run Card Entry View

**View Name:** `run_card_entry_view`

### Components:
| Component      | Name             | Notes |
|----------------|------------------|-------|
| Label          | `lbl_title`      | Text: "Run Card Entry" |
| Text Field     | `txt_workorder`  | Label: "Work Order (MFID)" |
| Text Field     | `txt_workstation`| Label: "Workstation" |
| Button         | `btn_submit`     | Text: "Submit"<br>**onClick script:**
```python
runScript(
  'project.scripts.run_card_creator.run',
  {
    'workorder': self.view.getChild("txt_workorder").props.text,
    'workstation': self.view.getChild("txt_workstation").props.text
  }
)
```

> Optional: Auto-fill reporter using `session.props.auth.user.username`

---

## 🧠 Python Script Breakdown: Run Card Creation

### Script: `project.scripts.run_card_creator.run(workorder, workstation)`
**Called by:** Button in `run_card_entry_view`

**Purpose:**
- Checks if a Run_Card UDT instance exists in `[default]/RunCards`
- If not, creates it using `system.tag.configure()`
- Writes initial values like workorder, workstation, reporter, status, and start time
- Publishes Run Card data to MQTT under the UNS path:
  - `joby/santa-cruz/run_cards/{workorder}/status`
  - `joby/santa-cruz/run_cards/{workorder}/workstation`
  - etc.

---

## 2️⃣ Run Card Display View

**View Name:** `RunCardDisplay`

**View Parameters:**
- `runCardPath` (String) → used as base tag path

### Components:
| Component  | Binding Example                                 | Notes |
|------------|--------------------------------------------------|-------|
| Label      | `Run Card` title                                | Style: bold, 20px |
| Label      | `Workorder: {view.params.runCardPath}/workorder`| One label per tag |
| Label      | `Product Code`, `Workstation`, `Workcenter`, `Priority`, `Status`, etc. | Bind each to respective tag path |
| Label      | `Elapsed Time: {view.params.runCardPath}/duration_minutes` | Optional live value |

---

## 3️⃣ Kanban Board Base Layout

**View Name:** `kanban_board_base_layout`

**View Parameters:**
- `workflowOrder` (Array of strings)

### Components:
| Component   | Name                | Notes |
|-------------|---------------------|-------|
| Repeater    | `workcenterRepeater`| Template Path: `WorkcenterColumn`<br>Instances from:
```python
@script:getKanbanInstances(view.params.workflowOrder)
```

---

## 🧠 Python Script Breakdown: Kanban Logic

### Script: `project.scripts.run_cards.getKanbanInstances(workflowOrder)`
**Called by:** `kanban_board_base_layout` repeater binding

**Purpose:**
- Calls `getRunCardQueueByWorkcenter()` to group active Run_Card tags by workcenter
- Returns a list of instances to feed into the WorkcenterColumn repeater

### Script: `project.scripts.run_cards.getRunCardQueueByWorkcenter()`
**Purpose:**
- Browses `[default]/RunCards` for UDT instances
- Reads `status` and `workcenter` tags
- Returns a dictionary like:
```python
{
  "Cutting": ["RunCards/MFID001"],
  "Layup": ["RunCards/MFID002", "RunCards/MFID003"]
}
```
- Only includes Run Cards that are **not marked as complete**

---

## 4️⃣ Workcenter Column View

**View Name:** `WorkcenterColumn`

**View Parameters:**
- `workcenter` (String)
- `cardPaths` (Array of tag paths)

### Components:
| Component   | Name         | Notes |
|-------------|--------------|-------|
| Label       | `header`     | Text: `{view.params.workcenter}` |
| Repeater    | `cardRepeater` | Template: `RunCardDisplay`<br>Instances:
```python
@script:[{'runCardPath': path} for path in view.params.cardPaths]
```

---



