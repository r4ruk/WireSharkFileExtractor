import binascii
import argparse

def parse_hexdump(hexdump_str):
    try:
        hex_data = ""
        for line in hexdump_str.split("\n"):
            hex_data = hex_data + line[10:59]
        content_stripped = hex_data.replace(" ", "").replace("\n", "").strip()

        return content_stripped
    except:
        return None


def get_file_magic_bytes(filetype:str):
    match filetype:
        case "exe" | "dll" | "mui" |"sys"|"scr"|"cpl"|"ocx"|"ax"|"iec"|"ime"|"rs"|"tsp"|"fon"|"efi":
            return "4d5a" #dos executable
        case "none" | "axf" | "bin" | "elf" | "o" | "out" | "prx" | "puff" | "ko" | "mod" | "so":
            return "7F454C46" # linux executable
        case "pdf":
            return "255044462d"
        case "doc" | "xls" | "ppt" | "msi" | "msg":
            return "d0cf11e0a1b11ae1" # microsoft COM compound file binary format
        case "tar":
            return "7573746172003030" # could also be: 75 73 74 61 72 20 20 00 time will tell if thats needed
        case "zip" | "aar" | "apk" | "docx" | "epub" | "ipa" | "jar" | "kmz" | "maff" | "msix" | "odp" | "ods" | "odt" | "pk3" | "pk4" | "pptx" | "usdz" | "vsdx" | "xlsx" | "xpi" | "whl":
            return "504b0304" # could also be a empty archive: "50 4B 05 06" or a spanned archive "50 4B 07 08" not sure thats actually needed.
    print("Unimplemented retrieval of the given filetype.")
    exit()

def main():
    parser = argparse.ArgumentParser(description="Parse a hex dump in a file, file path and the expected filetype.")
    parser.add_argument("-hexdump", type=str, help="Hex dump (exported from request which contains file raw content) - file")
    parser.add_argument("-output", type=str, help="Path to the file (directory + filename (without filetype -> other argument)")
    parser.add_argument("-filetype", type=str, help="The filetype expected to be found. is gonna be used to find Header of payload")


    args = parser.parse_args()
    expected_file_type = args.filetype
    try:
        with open(args.hexdump, "r", encoding="utf-8") as f:
            file_content = f.read()
            hexdump = file_content
        print("File content successfully loaded.")

        # Parse hex dump
        hex_data = parse_hexdump(hexdump)

        # get start of the actual important data:
        magic_bytes = get_file_magic_bytes(expected_file_type)
        pos = hex_data.find(magic_bytes)
        interesting_data = hex_data[pos:]

        # convert hex data to bin data
        bin_data = binascii.unhexlify(interesting_data)

        file_and_filepath = args.output + "." + args.filetype
        with open (file_and_filepath, "wb") as file:
            file.write(bin_data)

        (print(f"file saved: {file_and_filepath}"))

    except FileNotFoundError:
        print(f"Error: The file '{args.hexdump}' was not found.")
    except Exception as e:
        print(f"Error reading file: {e}")

if __name__ == "__main__":
    main()