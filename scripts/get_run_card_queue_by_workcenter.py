"""
Script: get_run_card_queue_by_workcenter.py
Author: Josh Payne (or your name/org)
Description:
    This script scans all Run_Card UDT instances under [default]RunCards in Ignition.
    It groups them by their 'workcenter' tag value and returns a dictionary for Kanban-style layout.

    Example output:
        {
            "Layup": ["RunCards/MFID123", "RunCards/MFID126"],
            "Cutting": ["RunCards/MFID124"]
        }

    Only Run_Cards with a status other than "complete" are included.
"""

def getRunCardQueueByWorkcenter():
    base_path = "[default]RunCards"
    result = {}

    # Get all run card tag instances
    run_cards = system.tag.browse(base_path)

    for rc in run_cards:
        if rc['hasChildren']:
            card_path = rc['fullPath']
            status_path = f"{card_path}/status"
            workcenter_path = f"{card_path}/workcenter"

            try:
                status = system.tag.readBlocking([status_path])[0].value
                workcenter = system.tag.readBlocking([workcenter_path])[0].value

                # Only show if not complete
                if status.lower() != "complete":
                    if workcenter not in result:
                        result[workcenter] = []
                    result[workcenter].append(card_path.replace("[default]/", ""))

            except Exception as e:
                system.util.getLogger("RunCardQueue").warnf("Error reading %s: %s", card_path, str(e))

    return result
