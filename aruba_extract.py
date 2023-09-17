#!/usr/bin/env python3
# For more details regarding 7z archive structure, please refer to: https://www.7-zip.org/recover.html

import sys
import argparse

signature_7z = b"\x37\x7a\xbc\xaf\x27\x1c"

def main(file, out):
	result = 0
	with open(file, "rb") as rf:
		n = 0
		block = rf.read(1) 
		print("Searching for 7z signature...")
		while block:
			#print(f"{n*16:08x}  {block}")
			if block[0] == signature_7z[0]:
				block = rf.read(len(signature_7z) - 1)
				if block == signature_7z[1:]:
					result += n
					print(f"[+] Found 7z signature at {hex(n)}!")
					break
				n += len(signature_7z) - 1
			else:
				n += 1
				block = rf.read(1)
		
		if result == 0:
			print("No 7z signature found.")
			
		else:		
			print(f"    Now parsing archive structure...")
			block = rf.read(26)
			format_version = block[:2]
			CRC = block[2:6]
			endHeader_offset = block[6:14]
			endHeader_size = block[14:22]
			endHeader_CRC = block[22:26]
			archive_length = int(endHeader_offset[::-1].hex().lstrip("0"),16) + endHeader_size[0] + 0x20
			
			
			print(f"    Archive file size: {archive_length}")	
			print(f"    Now extracting to {out}...")

			with open(out, "wb") as wf:
				try:
					wf.write(signature_7z)
					wf.write(block)
					wf.write(rf.read(archive_length - 32))
					print("[+] Extraction successful, good luck.")		
				except Exception as e:
					print(e)
					print("[-] Error writing extracted content.")
					
parser = argparse.ArgumentParser(description="Aruba corefiles extractor")
parser.add_argument("-f", "--file", help = "Your aruba firmware", required=True)
parser.add_argument("-o", "--out", help = "Output filename", required=True)
args = parser.parse_args()

if args.out[-3:] != ".7z":
	args.out = args.out + ".7z"

main(args.file, args.out)
