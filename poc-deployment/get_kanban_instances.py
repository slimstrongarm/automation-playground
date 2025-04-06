"""
Script: get_kanban_instances.py
Description:
    Generates repeater instances for a Kanban board in Ignition Perspective.
    Each instance represents a column based on a workcenter from a predefined workflow order.
    Pulls active Run_Cards grouped by workcenter using the `run_card_queue_by_workcenter.py` script.
"""

def getKanbanInstances(workflowOrder):
    # Call script that gets active Run_Card tags grouped by workcenter
    grouped_cards = shared.run_cards.getRunCardQueueByWorkcenter()

    # Build list of repeater instances in the defined workflow order
    instances = []
    for workcenter in workflowOrder:
        cards = grouped_cards.get(workcenter, [])
        instances.append({
            "workcenter": workcenter,
            "cardPaths": cards
        })

    return instances
