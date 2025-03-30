#!/usr/bin/env python3
import subprocess
import sys
import os
from pathlib import Path

def check_pip():
    """Check if pip is installed and accessible"""
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        return False

def install_beets():
    """Install beets and its dependencies"""
    print("[>] Installing beets and dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "beets", "pylast", "requests", "discogs-client"], check=True)
        print("[+] Beets installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[!] Error installing beets: {e}")
        return False

def create_alias():
    """Create shell alias for beets"""
    shell_rc = Path.home() / ".zshrc" if os.path.exists(Path.home() / ".zshrc") else Path.home() / ".bashrc"
    beets_path = subprocess.run([sys.executable, "-m", "pip", "show", "beets"], capture_output=True, text=True).stdout
    site_packages = [line.split(": ")[1] for line in beets_path.splitlines() if "Location" in line][0]
    beet_script = Path(site_packages) / "beets" / "scripts" / "beet"
    
    alias_line = f'\nalias beet="{sys.executable} {beet_script}"\n'
    
    print(f"[>] Adding beets alias to {shell_rc}")
    with open(shell_rc, "a") as f:
        f.write(alias_line)
    print("[+] Added beets alias. Please restart your terminal or run:")
    print(f"    source {shell_rc}")

def main():
    if not check_pip():
        print("[!] pip is not installed. Please install pip first.")
        sys.exit(1)
    
    if install_beets():
        create_alias()
        print("\n[+] Setup complete! You can now use beets by:")
        print("1. Restarting your terminal")
        print("2. Running 'beet' commands")
        print("\nExample usage:")
        print("  beet import /path/to/music")
    else:
        print("[!] Setup failed. Please check the error messages above.")

if __name__ == "__main__":
    main()
