"""
Script: run_card_queue_by_workcenter.py
Description:
    Groups all active Run_Card UDT instances by their `workcenter` tag.
    Only includes cards that are not marked as "complete".
    Returns a dictionary like:
        {
            "Cutting": ["RunCards/MFID002", "RunCards/MFID005"],
            "Layup": ["RunCards/MFID001"]
        }
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

                # Only include if status is not 'complete'
                if status.lower() != "complete":
                    if workcenter not in result:
                        result[workcenter] = []
                    result[workcenter].append(card_path.replace("[default]/", ""))

            except Exception as e:
                system.util.getLogger("RunCardQueue").warnf("Error reading %s: %s", card_path, str(e))

    return result
