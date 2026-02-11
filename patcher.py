from dataclasses import dataclass
import os
import subprocess
import sys

# Disable if wanting to check the LDA file afterwards
DELETE_OUTPUT = True

# Needed for making executeable file
def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

INPUT_FILE = resource_path("Quickbms/text.bin")
OUTPUT_FILE = resource_path("Quickbms/Patch/NAS4/LANG/TEXT0500.LDA")

quickbms = resource_path("Quickbms/quickbms.exe")
bms_script = resource_path("Quickbms/nascar2011.bms")
patch_dir = resource_path("Quickbms/Patch")

@dataclass
class DriverData:
    driver_name: str
    start_byte: int
    max_length: int

# Drivers are ordered by appearance in TEXT0500.LDA (max length is for safe mode being off)
drivers = [
    DriverData("AJ Allmendinger", 0x4E60, 15),
    DriverData("Aric Almirola", 0x4E70, 31),
    DriverData("Greg Biffle", 0x4EC0, 23),
    DriverData("Clint Bowyer", 0x4ED8, 31),
    DriverData("Kurt Busch", 0x4EFD, 10),
    DriverData("Kyle Busch", 0x4F08, 31),
    DriverData("Dale Earnhardt Jr.", 0x4F43, 18),
    DriverData("Carl Edwards", 0x4F56, 31),
    DriverData("David Gilliland", 0x4F7C, 15),
    DriverData("Jeff Gordon", 0x4F8c, 24),
    DriverData("Denny Hamlin", 0x4FA5, 12),
    DriverData("Kevin Harvick", 0x4FB2, 13), # NOTE: Harvick can be extended to 31 if Sam Hornish's name is overwritten. Hornish is never used by the AI, so the only impact on gameplay would be if the player picked Hornish
    DriverData("Sam Hornish Jr.", 0x4FC0, 28),
    DriverData("Jimmie Johnson", 0x4FDD, 25),
    DriverData("Kasey Kahne", 0x4FF7, 11),
    DriverData("Matt Kenseth", 0x5003, 12),
    DriverData("Brad Keselowski", 0x5010, 15),
    DriverData("Joey Logano", 0x5020, 11),
    DriverData("Bobby Labonte", 0x502C, 31),
    DriverData("Jamie McMurray", 0x505D, 14),
    DriverData("Casey Mears", 0x506C, 11),
    DriverData("Paul Menard", 0x5078, 31),
    DriverData("Ryan Newman", 0x50A4, 21),
    DriverData("David Ragan", 0x50BA, 31),
    DriverData("Regan Smith", 0x50FC, 25),
    DriverData("Tony Stewart", 0x5116, 26),
    DriverData("Martin Truex Jr.", 0x5131, 16),
    DriverData("Brian Vickers", 0x5142, 26),
    DriverData("Michael Waltrip", 0x515d, 15),
    DriverData("J.J. Yeley", 0x516d, 31),
    DriverData("Michael McDowell", 0x6247, 31),
    DriverData("Danica Patrick", 0xDE46, 31),
    DriverData("Trevor Bayne", 0xDE6F, 31),
    DriverData("Ricky Stenhouse Jr.", 0x1153F, 19),
    DriverData("Josh Wise", 0x11553, 31),
    DriverData("Austin Dillon", 0x14DE7, 29),
    DriverData("Cole Whitt", 0x14E05, 31),
    DriverData("Kyle Larson", 0x1B3A3, 31), # NOTE: Overwrites strings saying "Window", "Side", and "Career Schemes".
    DriverData("Justin Allgaier", 0x1C0A7, 31), # NOTE: going beyond 28 characters overwrites string saying "Engine"
    DriverData("Michael Annett", 0x1C133, 31),  # NOTE: Beyond 29 overwrites Brake Indicator tooltip
    DriverData("Chase Elliott", 0x1C1C8, 31),
    DriverData("Bubba Wallace Jr.", 0x1C23C, 31),
    DriverData("Ty Dillon", 0x1C796, 9),
    DriverData("Ryan Blaney", 0x1C7A0, 31), # NOTE: Beyond 11 overwrites HScott Motorsports's name
    DriverData("Erik Jones", 0x1C7CC, 19),
    DriverData("Jeb Burton", 0x1C7E0, 31) # NOTE: Beyond 24 overwrites Go Green Racing's name
]

# Create a map from the list
driver_map = {d.start_byte: d for d in drivers}

# Function for patching LDA file
def patch_file(replacements: dict,
               input_file: str = INPUT_FILE,
               output_file: str = OUTPUT_FILE,
               safe_mode: bool = True,
               game_dir: str | None = None):

    # Open input and output files as binary
    with open(input_file, "rb") as src, open(output_file, "wb") as out:
        # offset will track where we are in the file
        offset = 0

        while True:
            # Read one byte at a time
            byte = src.read(1)
            if not byte:
                # End of file
                break

            # If the byte we're at is in one of the 46 where a driver name starts, we need to replace the name
            if offset in driver_map:
                # Get replacement name from driver map
                d = driver_map[offset]
                new_name = replacements.get(d.driver_name, d.driver_name)

                # Encode name to place as bytes
                encoded_name = new_name.encode("ascii")

                # Safe mode: restrict max_length to original name length
                effective_max = len(d.driver_name) if safe_mode else d.max_length

                # Raise error if value exceeds expected max, shouldn't be possible through the text validation
                # Ignore this check on Harvick. Bad solution but that's how it be sometimes.
                if len(encoded_name) > effective_max and d.driver_name != "Kevin Harvick":
                    raise ValueError(
                        f"'{new_name}' too long for field '{d.driver_name}' "
                        f"(max {effective_max})"
                    )

                # Bytes that will be overwritten: replacement length + 1 (for NULL)
                overwrite_len = len(encoded_name) + 1

                # Append null byte to replacement
                data = encoded_name + b'\x00'

                # Write replacement bytes
                out.write(data)

                # Skip over the bytes we've written to maintain alignment
                src.seek(overwrite_len - 1, 1)
                offset += overwrite_len

            else:
                # Write unchanged data to file as is
                out.write(byte)
                offset += 1

    # Once new LDA file is made, use quickbms to apply patch to ARCHIVE0.AR file
    subprocess.run([
        quickbms,
        "-w",
        "-r",
        bms_script,
        f"{game_dir}/cdfiles.DAT",
        patch_dir
    ])

    # Remove LDA files
    if (DELETE_OUTPUT):
        os.remove(OUTPUT_FILE)