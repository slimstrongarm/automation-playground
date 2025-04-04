# Gateway Tag Change Script for `work_stoppage`
# Attach this script to a tag change event for:
# [default]/Runs/*/work_stoppage

from java.util import Date

# Get the full tag path
fullPath = event.tagPath.toString()
basePath = fullPath.replace("/work_stoppage", "")

# Read current and previous values
current = currentValue.value
previous = previousValue.value

# Only run if status actually changed
if current != previous:
    if current in ["high", "low"]:
        # Start of stoppage
        system.tag.writeAsync([basePath + "/stoppage_start_time"], [system.date.now()])

    elif current == "none" and previous in ["high", "low"]:
        # End of stoppage
        try:
            start_time = system.tag.readBlocking([basePath + "/stoppage_start_time"])[0].value
            now = system.date.now()
            duration_minutes = int((now.getTime() - start_time.getTime()) / 60000)

            # Write duration
            system.tag.writeBlocking([
                basePath + "/work_stoppage_duration",
                basePath + "/total_work_stoppage",
                basePath + "/work_stoppage_count"
            ], [
                duration_minutes,
                system.tag.readBlocking([basePath + "/total_work_stoppage"])[0].value + duration_minutes,
                system.tag.readBlocking([basePath + "/work_stoppage_count"])[0].value + 1
            ])

        except Exception as e:
            system.util.getLogger("Stoppage Script").error("Error calculating stoppage duration: " + str(e))
