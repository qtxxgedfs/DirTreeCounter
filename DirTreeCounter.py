"""
Purpose:
Traverse all subfolders of a parent directory, generate a directory structure diagram,
count the total number of folders and non-folder files,
and output the results to a txt file in the program's directory.
"""

import os
import sys
import argparse
from typing import Tuple

class TeeOutput:
    """
    A class to redirect output to both console and a file simultaneously.
    """
    def __init__(self, file_path):
        self.console = sys.stdout  # Save original console output
        self.file = open(file_path, 'w', encoding='utf-8')  # Open output file
    
    def write(self, message):
        """Write message to both console and file"""
        self.console.write(message)
        self.file.write(message)
    
    def flush(self):
        """Flush both outputs"""
        self.console.flush()
        self.file.flush()
    
    def close(self):
        """Close the file and restore original console output"""
        if self.file:
            self.file.close()
        sys.stdout = self.console

def print_directory_tree(
    root_dir: str,
    prefix: str = "",
    is_last: bool = True,
    folder_count: list = None,
    file_count: list = None
) -> None:
    """
    Recursively print directory tree structure.
    
    Args:
        root_dir: Current directory to process
        prefix: String used for formatting tree structure
        is_last: Whether current entry is the last in its parent directory
        folder_count: List to track total folder count (mutable object)
        file_count: List to track total file count (mutable object)
    """
    if folder_count is None:
        folder_count = [0]
    if file_count is None:
        file_count = [0]
    
    try:
        # Get and sort all entries, excluding hidden files/folders (starting with .)
        entries = sorted(os.listdir(root_dir))
        entries = [e for e in entries if not e.startswith('.')]
        
        # Separate entries into directories and files
        dirs = []
        files = []
        for entry in entries:
            entry_path = os.path.join(root_dir, entry)
            if os.path.isdir(entry_path):
                dirs.append(entry)
            elif os.path.isfile(entry_path):
                files.append(entry)
        
        # Update folder count
        folder_count[0] += len(dirs)
        
        # Combine directories and files for processing
        all_entries = []
        for d in dirs:
            all_entries.append((d, 'dir'))
        for f in files:
            all_entries.append((f, 'file'))
            file_count[0] += 1
        
        entries_count = len(all_entries)
        for idx, (entry, entry_type) in enumerate(all_entries):
            is_entry_last = idx == entries_count - 1
            
            # Determine prefix for child entries
            if is_last:
                current_prefix = prefix + "    "
            else:
                current_prefix = prefix + "│   "
            
            # Determine branch symbol and icon
            branch = "└── " if is_entry_last else "├── "
            icon = "📁 " if entry_type == 'dir' else "📄 "
            print(f"{prefix}{branch}{icon}{entry}")
            
            # Recursively process subdirectories
            if entry_type == 'dir':
                print_directory_tree(
                    os.path.join(root_dir, entry),
                    current_prefix,
                    is_entry_last,
                    folder_count,
                    file_count
                )
                
    except PermissionError:
        print(f"{prefix}└── ❌ [Permission denied]")
    except Exception as e:
        print(f"{prefix}└── ⚠️ [Error accessing: {str(e)}]")

def analyze_directory(root_path: str) -> Tuple[int, int]:
    """
    Analyze directory structure and count folders/files.
    
    Args:
        root_path: Root directory to analyze
        
    Returns:
        Tuple containing (folder_count, file_count)
        
    Raises:
        FileNotFoundError: If root_path does not exist
        NotADirectoryError: If root_path is not a directory
    """
    if not os.path.exists(root_path):
        raise FileNotFoundError(f"Directory does not exist: {root_path}")
    if not os.path.isdir(root_path):
        raise NotADirectoryError(f"Not a valid directory: {root_path}")
    
    folder_count = [0]
    file_count = [0]
    
    print(f"📂 Directory structure: {os.path.abspath(root_path)}")
    print("=" * 60)
    print_directory_tree(root_path, folder_count=folder_count, file_count=file_count)
    print("=" * 60)
    
    return folder_count[0], file_count[0]

def main(root_path):
    """Main function to coordinate directory analysis and output"""
    # Define output txt file path (in program's directory)
    output_file = os.path.join(os.path.dirname(__file__), "tree-count-directory-stats.txt")
    
    try:
        tee = TeeOutput(output_file)
        sys.stdout = tee  # Redirect output to both console and file
        
        folder_num, file_num = analyze_directory(root_path)
        
        print("📊 Statistics:")
        print(f"Total folders: {folder_num}")
        print(f"Total files: {file_num}")
        print(f"Total items: {folder_num + file_num}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    finally:
        if 'tee' in locals():
            sys.stdout = tee.console  # Restore original output
            tee.close()
            print(f"\n✅ Results saved to: {output_file}")

if __name__ == "__main__":
    # Parse command line arguments, default path is program's directory
    parser = argparse.ArgumentParser(description='Generate directory structure and count files')
    parser.add_argument('path', nargs='?', default=os.path.dirname(__file__), 
                        help='Directory path to analyze (default: program directory)')
    args = parser.parse_args()

    # Set your target directory path here
    args.path = r"D:\code\health-pdf-description-combine\pathway_description"
    main(args.path)
