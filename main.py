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

        raw_strings = re.findall(rb"[ -~]{3,}", data)

        decoded_strings = []

        for s in raw_strings:
            try:
                decoded_strings.append(s.decode("utf-8"))
            except UnicodeDecodeError:
                pass

        strings_output = Path(file_path.stem + "_strings.txt")

        with strings_output.open("w", encoding="utf-8") as f:
            for i, item in enumerate(decoded_strings, start=1):
                f.write(f"{i}: {item}\n")

        print("Saved:", strings_output)

        input_index = None

        for i, item in enumerate(decoded_strings):
            if item.strip() == "Input Channels":
                input_index = i
                break

        if input_index is None:
            print("Could not locate Input Channels block.")
            continue

        print("Found Input Channels block at line", input_index + 1)

        start_index = input_index + 3

        channel_names = []

        for item in decoded_strings[start_index:start_index + 128]:

            clean_item = item.strip()

            if clean_item.startswith("Grp"):
                break

            if clean_item == "":
                continue

            channel_names.append(clean_item)

        bus_names = []

        for item in decoded_strings:

            clean_item = item.strip()

            if clean_item.startswith("Grp"):
                bus_names.append(clean_item)

            elif clean_item.startswith("Aux"):
                bus_names.append(clean_item)

            elif clean_item.startswith("Matrix"):
                bus_names.append(clean_item)

            elif clean_item == "Master":
                bus_names.append(clean_item)

        bus_names = list(dict.fromkeys(bus_names))

        fx_names = []

        for item in decoded_strings:

            clean_item = item.strip()
            lower_item = clean_item.lower()

            if clean_item.startswith("FX"):
                fx_names.append(clean_item)

            elif "reverb" in lower_item:
                fx_names.append(clean_item)

            elif "delay" in lower_item:
                fx_names.append(clean_item)

            elif "plate" in lower_item:
                fx_names.append(clean_item)

            elif "room" in lower_item:
                fx_names.append(clean_item)

        fx_names = list(dict.fromkeys(fx_names))

        show = ShowFile(
            console_type="DiGiCo",
            session_name=file_path.stem
        )

        for channel_number, channel_name in enumerate(channel_names, start=1):
            show.channels.append(
                Channel(
                    number=channel_number,
                    name=channel_name
                )
            )

        for bus_number, bus_name in enumerate(bus_names, start=1):
            show.buses.append(
                Bus(
                    number=bus_number,
                    name=bus_name
                )
            )

        for fx_number, fx_name in enumerate(fx_names, start=1):
            show.fx.append(
                FX(
                    number=fx_number,
                    name=fx_name
                )
            )

        print("\nUniversal Show Model Created")
        print("Console:", show.console_type)
        print("Session:", show.session_name)
        print("Channels:", len(show.channels))
        print("Buses:", len(show.buses))
        print("FX:", len(show.fx))

        channel_output = Path(file_path.stem + "_channel_list.csv")

        with channel_output.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Channel", "Name"])

            for channel in show.channels:
                writer.writerow([channel.number, channel.name])

        print("Saved:", channel_output)

        bus_output = Path(file_path.stem + "_bus_list.csv")

        with bus_output.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Bus", "Name"])

            for bus in show.buses:
                writer.writerow([bus.number, bus.name])

        print("Saved:", bus_output)

        fx_output = Path(file_path.stem + "_fx_list.csv")

        with fx_output.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["FX", "Name"])

            for fx in show.fx:
                writer.writerow([fx.number, fx.name])

        print("Saved:", fx_output)

print("\nDone.")