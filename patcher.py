from dataclasses import dataclass
import os
import sys

# Needed for making executeable file
def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

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
    DriverData("Kyle Larson", 0x1B3A3, 31), # NOTE: Overwrites strings containing "Window", "Side", and "Career Schemes".
    DriverData("Justin Allgaier", 0x1C0A7, 31), # NOTE: going beyond 28 characters overwrites string containing "Engine"
    DriverData("Michael Annett", 0x1C133, 31),  # NOTE: Beyond 29 overwrites Brake Indicator tooltip
    DriverData("Chase Elliott", 0x1C1C8, 31),
    DriverData("Bubba Wallace Jr.", 0x1C23C, 31),
    DriverData("Ty Dillon", 0x1C796, 9),
    DriverData("Ryan Blaney", 0x1C7A0, 31), # NOTE: Beyond 11 overwrites HScott Motorsports's name
    DriverData("Erik Jones", 0x1C7CC, 19),
    DriverData("Jeb Burton", 0x1C7E0, 31) # NOTE: Beyond 24 overwrites Go Green Racing's name
]

# Function for patching ARCHIVE0.AR file
def patch_file(replacements: dict,
               safe_mode: bool = True,
               game_dir: str | None = None):

    # Open ARCHIVE0.AR file in binary
    with open(f"{game_dir}/ARCHIVE0.AR", "r+b") as archive_file:
        # TEXT0500.LDA in ARCHIVE0.AR starts at 0x2C7A1498
        offset = 0x2C7A1498

        # iterate over drivers
        for d in drivers:
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
            
            # Go to location of driver name in ARCHIVE0.AR and write
            archive_position = offset + d.start_byte
            archive_file.seek(archive_position)

            # Write replacement name and NULL byte
            archive_file.write(encoded_name + b'\x00')