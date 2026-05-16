from pathlib import Path
import re
import csv

from universal_model import ShowFile, Channel, Bus, FX

print("ShowBridge DiGiCo Explorer")

test_folder = Path("test_sessions")

if not test_folder.exists():
    print("ERROR: test_sessions folder not found.")
    exit()

files = list(test_folder.iterdir())

for file_path in files:

    if file_path.is_file() and file_path.suffix == ".ses":

        print("\nReading:", file_path.name)

        data = file_path.read_bytes()

        raw_strings = re.findall(rb"[\x20-\x7E]{3,}", data)

        decoded_strings = []

        for s in raw_strings:
            try:
                decoded_strings.append(s.decode("utf-8"))
            except UnicodeDecodeError:
                pass

        session_name = file_path.stem

        strings_output = f"{session_name}_strings.txt"

        with open(strings_output, "w") as f:
            for i, s in enumerate(decoded_strings):
                f.write(f"{i}: {s}\n")

        print("Saved:", strings_output)

        # -------------------------------------------------
        # CREATE UNIVERSAL SHOW MODEL
        # -------------------------------------------------

        show = ShowFile("DiGiCo", session_name)

        # -------------------------------------------------
        # FIND INPUT CHANNELS
        # -------------------------------------------------

        channel_start = None

        for i, s in enumerate(decoded_strings):
            if s == "Input Channels":
                channel_start = i
                print("Found Input Channels block at line", i)
                break

        if channel_start:

            for ch_num in range(1, 129):

                line_index = channel_start + ch_num + 2

                if line_index < len(decoded_strings):

                    name = decoded_strings[line_index].strip()

                    if (
                        name
                        and name != "Arial"
                        and not name.startswith("Ch ")
                    ):

                        channel = Channel(ch_num, name)
                        show.channels.append(channel)

                    else:
                        channel = Channel(ch_num, f"Ch {ch_num}")
                        show.channels.append(channel)

        # -------------------------------------------------
        # FIND BUSES
        # -------------------------------------------------

        bus_keywords = [
            "Aux",
            "Grp",
            "Matrix",
            "Master",
            "FX",
        ]

        bus_num = 1

        for s in decoded_strings:

            if any(keyword in s for keyword in bus_keywords):

                if len(s) < 40:

                    exists = False

                    for b in show.buses:
                        if b.name == s:
                            exists = True

                    if not exists:

                        bus = Bus(bus_num, s)
                        show.buses.append(bus)
                        bus_num += 1

        # -------------------------------------------------
        # FIND FX
        # -------------------------------------------------

        fx_keywords = [
            "Reverb",
            "Delay",
            "Plate",
            "room",
            "Room",
        ]

        fx_num = 1

        for s in decoded_strings:

            if any(keyword in s for keyword in fx_keywords):

                if len(s) < 40:

                    exists = False

                    for fx in show.fx:
                        if fx.name == s:
                            exists = True

                    if not exists:

                        fx_obj = FX(fx_num, s)
                        show.fx.append(fx_obj)
                        fx_num += 1

        # -------------------------------------------------
        # FIND SNAPSHOTS
        # -------------------------------------------------

        snapshots = []

        for i, s in enumerate(decoded_strings):

            if (
                i + 1 < len(decoded_strings)
                and decoded_strings[i + 1] == "Arial"
            ):

                if len(s) < 40:

                    if not s.startswith("Ch "):

                        if s not in snapshots:

                            snapshots.append(s)

        # -------------------------------------------------
        # EXPORT CHANNELS
        # -------------------------------------------------

        channel_output = f"{session_name}_channel_list.csv"

        with open(channel_output, "w", newline="") as csvfile:

            writer = csv.writer(csvfile)

            writer.writerow(["Channel", "Name"])

            for channel in show.channels:
                writer.writerow([channel.number, channel.name])

        print("Saved:", channel_output)

        # -------------------------------------------------
        # EXPORT BUSES
        # -------------------------------------------------

        bus_output = f"{session_name}_bus_list.csv"

        with open(bus_output, "w", newline="") as csvfile:

            writer = csv.writer(csvfile)

            writer.writerow(["Bus", "Name"])

            for bus in show.buses:
                writer.writerow([bus.number, bus.name])

        print("Saved:", bus_output)

        # -------------------------------------------------
        # EXPORT FX
        # -------------------------------------------------

        fx_output = f"{session_name}_fx_list.csv"

        with open(fx_output, "w", newline="") as csvfile:

            writer = csv.writer(csvfile)

            writer.writerow(["FX", "Name"])

            for fx in show.fx:
                writer.writerow([fx.number, fx.name])

        print("Saved:", fx_output)

        # -------------------------------------------------
        # EXPORT SNAPSHOTS
        # -------------------------------------------------

        snapshot_output = f"{session_name}_snapshot_list.csv"

        with open(snapshot_output, "w", newline="") as csvfile:

            writer = csv.writer(csvfile)

            writer.writerow(["Snapshot", "Name"])

            for i, snap in enumerate(snapshots, start=1):
                writer.writerow([i, snap])

        print("Saved:", snapshot_output)

        # -------------------------------------------------

        print("\nUniversal Show Model Created")
        print("Console:", show.console_type)
        print("Session:", show.session_name)
        print("Channels:", len(show.channels))
        print("Buses:", len(show.buses))
        print("FX:", len(show.fx))
        print("Snapshots:", len(snapshots))

print("\nDone.")