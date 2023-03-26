import os
import hashlib
import subprocess

def generate_html(data):
    html_str = "<table>\n"
    html_str += "<tr><th>Level</th><th>Type</th><th>Name</th><th>Size (bytes)</th><th>CRC-32</th></tr>\n"
    for item in data:
        html_str += "<tr>"
        for field in item:
            html_str += "<td>" + str(field) + "</td>"
        html_str += "</tr>\n"
    html_str += "</table>"
    with open("output.html", "w") as f:
        f.write(html_str)
    print("HTML file generated successfully!")

def calculate_crc32(file_path):
    buf = open(file_path, 'rb').read()
    crc32 = hex(zlib.crc32(buf) & 0xffffffff)
    return crc32

def explore_directory(path, level=0):
    data = []
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            data.append([level, "directory", item, os.path.getsize(item_path), "N/A"])
            data += explore_directory(item_path, level + 1)
        else:
            data.append([level, "file", item, os.path.getsize(item_path), calculate_crc32(item_path)])
    return data

def install_zlib():
    try:
        import zlib
    except ImportError:
        subprocess.run(["pip", "install", "zlib"])
        import zlib

install_zlib()
directory = input("Enter the directory path: ")
data = explore_directory(directory)
generate_html(data)