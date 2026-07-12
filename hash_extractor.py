#!/usr/bin/env python3
import hashlib
import pytsk3
import csv

def calculate_hash(fs_info, inode_num):
    try:
        file_obj = fs_info.open_meta(inode_num)
        file_size = file_obj.info.meta.size
        content = file_obj.read_random(0, file_size)
        return hashlib.sha256(content).hexdigest()
    except Exception as e:
        return f"Error: {e}"

def extract_hashes(image_path="my-test.dd", output_csv="outputs/tsk_hashes.csv", offset=0):
    img = pytsk3.Img_Info(image_path)
    fs = pytsk3.FS_Info(img, offset=int(offset))

    print(f"Analyzing: {image_path}\n")
    print("SHA-256 hashes:\n")

    results = []
    root = fs.open_dir(path="/")
    for entry in root:
        filename = entry.info.name.name.decode('utf-8')
        if filename in [".", ".."]:
            continue

        if entry.info.meta and entry.info.meta.type == pytsk3.TSK_FS_META_TYPE_REG:
            file_hash = calculate_hash(fs, entry.info.meta.addr)
            print(f"{filename}: {file_hash}")
            results.append({'filename': filename, 'sha256': file_hash})

    with open(output_csv, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['filename', 'sha256'])
        writer.writeheader()
        writer.writerows(results)

    print(f"\n✅ Saved {len(results)} hashes to {output_csv}")
    return results

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        output_csv = sys.argv[2] if len(sys.argv) > 2 else "outputs/tsk_hashes.csv"
        offset = int(sys.argv[3]) if len(sys.argv) > 3 else 0
        extract_hashes(image_path, output_csv, offset)
    else:
        extract_hashes()
