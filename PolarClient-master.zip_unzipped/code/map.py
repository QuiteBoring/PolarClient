import os
import hashlib

def md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            normalized_line = line.replace('\r', '').replace('\n', '').replace(' ', '')
            hash_md5.update(normalized_line.encode('utf-8'))
    return hash_md5.hexdigest()

def compare_first_10_lines(file1, file2):
    with open(file1, "r", encoding="utf-8", errors="ignore") as f1, open(file2, "r", encoding="utf-8", errors="ignore") as f2:
        lines1 = [next(f1, '').strip() for _ in range(10)]
        lines2 = [next(f2, '').strip() for _ in range(10)]
    return lines1 == lines2

def compare_and_override(src_dir, new_dir):
    matched_files = set()
    for root, _, files in os.walk(src_dir):
        for file_name in files:
            src_file_path = os.path.join(root, file_name)
            src_file_md5 = md5(src_file_path)
            match_found = False

            for new_root, _, new_files in os.walk(new_dir):
                for new_file_name in new_files:
                    new_file_path = os.path.join(new_root, new_file_name)
                    new_file_md5 = md5(new_file_path)
                    if new_file_md5 == src_file_md5:
                        os.remove(new_file_path)
                        print(f"Overridden and deleted: {new_file_path}")
                        match_found = True
                        matched_files.add(src_file_path)
                        break
                if match_found:
                    break

            if not match_found:
                for new_root, _, new_files in os.walk(new_dir):
                    for new_file_name in new_files:
                        new_file_path = os.path.join(new_root, new_file_name)
                        if compare_first_10_lines(src_file_path, new_file_path):
                            print(f"Match found by first 10 lines: {new_file_path}")
                            match_found = True
                            matched_files.add(src_file_path)
                            break
                    if match_found:
                        break

            if not match_found:
                print(f"No match found for: {src_file_path}")

if __name__ == "__main__":
    src_directory = "src"
    new_directory = "new"

    compare_and_override(src_directory, new_directory)
