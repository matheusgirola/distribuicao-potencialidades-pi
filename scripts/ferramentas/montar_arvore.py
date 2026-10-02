from pathlib import Path

def print_tree(directory, indent=""):
    path = Path(directory)
    
    # Print the current directory name
    print(indent + f"📁 {path.name}/")
    
    # Update indentation for items inside this directory
    indent += "    "
    
    # Sort items so folders appear first, then files
    try:
        items = sorted(path.iterdir(), key=lambda x: (x.is_file(), x.name.lower()))
        for item in items:
            if item.is_dir():
                print_tree(item, indent)
            else:
                print(indent + f"📄 {item.name}")
    except PermissionError:
        print(indent + "⚠️ [Permission Denied]")

# Example Usage: Replace with your actual path
print_tree("./")
