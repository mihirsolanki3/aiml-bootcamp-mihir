# TASK 06
# Parse a real log file

import re
from collections import Counter, defaultdict
from datetime import datetime

# --------------------------------------------------
# 1. Generate a log file with 200+ lines
# --------------------------------------------------

levels = ["INFO", "WARN", "ERROR"]

messages = {
    "INFO": [
        "User logged in",
        "Request completed successfully",
        "Database connection established",
        "File uploaded successfully",
        "User logged out"
    ],
    "WARN": [
        "High memory usage detected",
        "Slow response time",
        "Connection retry",
        "Disk space is getting low",
        "Invalid input received"
    ],
    "ERROR": [
        "Database connection failed",
        "File not found",
        "Database connection failed",
        "Authentication failed",
        "Database connection failed",
        "Server timeout"
    ]
}

# Create 250 log entries
with open("server.log", "w") as file:
    for i in range(250):

        day = (i % 3) + 1
        hour = i % 24
        minute = (i * 7) % 60
        second = (i * 13) % 60

        timestamp = (
            f"2026-09-{day:02d} "
            f"{hour:02d}:{minute:02d}:{second:02d}"
        )

        level = levels[i % len(levels)]
        message = messages[level][i % len(messages[level])]

        file.write(f"{timestamp} {level} {message}\n")


# --------------------------------------------------
# 2. Read the log file
# --------------------------------------------------

with open("server.log", "r") as file:
    lines = file.readlines()


# --------------------------------------------------
# 3. Regex pattern
# --------------------------------------------------

pattern = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+(\w+)\s+(.*)"


entries = []

# defaultdict groups entries by level
grouped_by_level = defaultdict(list)

# Counter for levels
level_counter = Counter()

# Counter for hours
hour_counter = Counter()

# Counter for ERROR messages
error_messages = Counter()


# --------------------------------------------------
# 4. Parse every line
# --------------------------------------------------

for line in lines:

    m = re.match(pattern, line.strip())

    if m:
        # Capture groups
        ts, level, message = m.groups()

        # Convert string to datetime
        timestamp = datetime.strptime(
            ts,
            "%Y-%m-%d %H:%M:%S"
        )

        # Store parsed information
        entry = {
            "timestamp": timestamp,
            "level": level,
            "message": message
        }

        entries.append(entry)

        # Count levels
        level_counter[level] += 1

        # Count entries by hour
        hour_counter[timestamp.hour] += 1

        # Group entries by level
        grouped_by_level[level].append(entry)

        # Count ERROR messages
        if level == "ERROR":
            error_messages[message] += 1


# --------------------------------------------------
# 5. Display number of entries per level
# --------------------------------------------------

print("\nEntries per level:")

for level, count in level_counter.items():
    print(f"{level}: {count}")


# --------------------------------------------------
# 6. Find busiest hour
# --------------------------------------------------

busiest_hour, busiest_count = hour_counter.most_common(1)[0]

print("\nBusiest hour:")
print(f"{busiest_hour:02d}:00 - {busiest_count} entries")


# --------------------------------------------------
# 7. Most frequently repeated ERROR message
# --------------------------------------------------

if error_messages:

    most_common_error, error_count = (
        error_messages.most_common(1)[0]
    )

    print("\nMost frequent ERROR message:")
    print(f"{most_common_error} ({error_count} times)")


# --------------------------------------------------
# 8. Display groups created using defaultdict
# --------------------------------------------------

print("\nEntries grouped by level:")

for level, group in grouped_by_level.items():

    print(f"{level}: {len(group)} entries")


# --------------------------------------------------
# 9. BONUS:
#    Find longest gap between ERROR entries
# --------------------------------------------------

error_entries = grouped_by_level["ERROR"]

# Sort ERROR entries by timestamp
error_entries.sort(
    key=lambda entry: entry["timestamp"]
)

longest_gap = None
gap_start = None
gap_end = None

for i in range(1, len(error_entries)):

    previous_time = error_entries[i - 1]["timestamp"]
    current_time = error_entries[i]["timestamp"]

    gap = current_time - previous_time

    if longest_gap is None or gap > longest_gap:

        longest_gap = gap
        gap_start = previous_time
        gap_end = current_time


if longest_gap:

    print("\nLongest gap between ERROR entries:")
    print(f"From: {gap_start}")
    print(f"To:   {gap_end}")
    print(f"Gap:  {longest_gap}")