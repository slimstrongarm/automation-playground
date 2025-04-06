"""
Script: create_sample_run_cards.py
Description:
    Bulk-creates sample Run_Card UDT instances in Ignition for testing and POC visualization.
    This can be run from the Script Console or as a shared script during initial setup.

    Creates three test jobs with different workcenters and priorities.
"""

run_ids = ["MFID001", "MFID002", "MFID003"]
base_path = "[default]/RunCards"
udt_type = "Run_Card"

configs = []

for run_id in run_ids:
    configs.append({
        "name": run_id,
        "type": "UDT_INST",
        "typeId": udt_type,
        "parameters": {},
        "tags": [
            {"name": "workorder", "value": run_id},
            {"name": "workstation", "value": f"WS-{run_id[-1]}"},
            {"name": "reporter", "value": "demo.user"},
            {"name": "workcenter", "value": "Layup" if run_id.endswith("1") else "Cutting"},
            {"name": "priority", "value": "High" if run_id.endswith("1") else "Medium"},
            {"name": "status", "value": "in_work"},
            {"name": "product_code", "value": "CF-PART-00" + run_id[-1]}
        ]
    })

# Deploy to Ignition
system.tag.configure(base_path, configs, overwrite=False)

# Optional: log the success
system.util.getLogger("RunCardSetup").info("Sample Run_Card instances created.")
