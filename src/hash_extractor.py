#!/usr/bin/env python3
import pytsk3
import hashlib
import csv
import sys
import os

def extract_hashes(image_path, output_csv):
    img = pytsk3.Img_Info(image_path)
    
    # Try with offset (M57), then without (test image)
    try:
        fs = pytsk3.FS_Info(img, offset=63*512)
    except:
        fs = pytsk3.FS_Info(img)
    
    results = []
    
    def walk_directory(dir_path):
        """Recursively walk through all directories"""
        try:
            directory = fs.open_dir(path=dir_path)
            for file in directory:
                if file.info.meta is None:
                    continue
                
                # If it's a directory, walk into it
                if file.info.meta.type == pytsk3.TSK_FS_META_TYPE_DIR:
                    if file.info.name.name not in [b'.', b'..']:
                        sub_path = f"{dir_path}/{file.info.name.name.decode('utf-8')}"
                        walk_directory(sub_path)
                
                # If it's a regular file, get hash
                elif file.info.meta.type == pytsk3.TSK_FS_META_TYPE_REG:
                    try:
                        content = file.read_random(0, file.info.meta.size)
                        sha256_hash = hashlib.sha256(content).hexdigest()
                        filename = file.info.name.name.decode('utf-8')
                        full_path = f"{dir_path}/{filename}"
                        results.append({'filename': full_path, 'sha256': sha256_hash})
                    except:
                        pass
        except:
            pass
    
    # Start walking from root
    walk_directory("/")
    
    # Write to CSV
    with open(output_csv, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['filename', 'sha256'])
        writer.writeheader()
        writer.writerows(results)
    
    print(f"✅ Extracted {len(results)} files to {output_csv}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python hash_extractor.py <image_path> <output_csv>")
        sys.exit(1)
    extract_hashes(sys.argv[1], sys.argv[2])
