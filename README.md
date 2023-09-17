# For all those that are conducting research on Aruba IoT devices.
You may have noticed some components are missing/referenced within the base Aruba filesystem that you extracted, more specifically, mentions of arubaos_core. 
This is because extraction tools such as binwalk is not always reliable, hence I have developed a script to (hopefully) help you extract arubaos' corefile archive.

# Usage example
aruba_extract.py -f <aruba_fimrware> -o outfile.7z
