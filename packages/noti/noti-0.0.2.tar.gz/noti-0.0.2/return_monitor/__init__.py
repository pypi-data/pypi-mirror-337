#!/usr/bin/env python3
import subprocess
import sys
import os
from PIL import Image, ImageDraw
import pystray
import threading
import time
import argparse
import shutil
import shlex

global_icon_ref = None
current_status_successful = None

def create_circle_icon(color, size=(64, 64)):
    image = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    padding = size[0] // 8
    draw.ellipse(
        (padding, padding, size[0] - padding -1, size[1] - padding -1),
        fill=color
    )
    return image

def run_command(args):
    print(f"Executing: {' '.join(args.command)}")
    try:
        result = subprocess.run(args.command, capture_output=True, check=False, text=True, timeout=30)
        print(f"Command finished with exit code: {result.returncode}")
        if result.returncode == 0:
            print(f"Success Output:\n{result.stdout.strip()}")
        else:
            print(f"Error Output:\n{result.stderr.strip()}", file=sys.stderr)
        return result.returncode == 0, result.stdout.strip() if result.returncode == 0 else result.stderr.strip()
    except FileNotFoundError:
        error_msg = f"Error: Command not found: {args.command[0]}"
        print(error_msg, file=sys.stderr)
        return False, error_msg
    except subprocess.TimeoutExpired:
        error_msg = f"Error: Command timed out after 30 seconds: {' '.join(args.command)}"
        print(error_msg, file=sys.stderr)
        return False, error_msg
    except Exception as e:
        error_msg = f"Error executing command: {e}"
        print(error_msg, file=sys.stderr)
        return False, error_msg

def update_icon_status(args, icon):
    global current_status_successful
    is_success, output_message = run_command(args)

    if is_success == current_status_successful:
        print("Status unchanged.")
        return

    current_status_successful = is_success
    icon.icon = create_circle_icon('green' if is_success else 'red')
    icon.title = f"ReturnMonitor: {'Success' if is_success else 'Failed'}"

    short_output = (output_message[:70] + '...') if len(output_message) > 70 else output_message
    tooltip_message = f"{'Success' if is_success else 'Failed'}\n{short_output.strip()}"
    if hasattr(icon, 'tooltip'): # pystray >= 0.19.1
         icon.tooltip = tooltip_message
    else: # older pystray
         icon.title = tooltip_message # Fallback for older pystray

    print(f"Icon updated to: {'Success (Green)' if is_success else 'Failure (Red)'}")
    # Optionally show a notification (works better on some systems than others)
    # try:
    #    icon.notify("Status Updated", tooltip_message)
    # except Exception as e:
    #    print(f"Could not send notification: {e}")


def periodic_check(args, icon):
    while True:
        update_icon_status(args, icon)
        # Check icon.visible again before sleeping in case Quit was selected
        if icon.visible:
            time.sleep(args.interval)

def exit_action(icon, item):
    print("Exiting...")
    icon.stop()

def run_check_now(icon, item):
    print("Manual check triggered.")
    # Run in a separate thread to avoid blocking the UI
    threading.Thread(target=update_icon_status, args=(icon,), daemon=True).start()

def setup_and_run_tray(args):
    global global_icon_ref
    global current_status_successful

    initial_success, initial_output = run_command(args)
    current_status_successful = initial_success

    icon_image = create_circle_icon('green' if initial_success else 'red')
    short_initial_output = (initial_output[:70] + '...') if len(initial_output) > 70 else initial_output
    initial_tooltip = f"{'Success' if initial_success else 'Failed'}\n{short_initial_output.strip()}"

    menu = pystray.Menu(
        pystray.MenuItem('Check Now', run_check_now),
        pystray.MenuItem('Quit', exit_action)
    )

    icon = pystray.Icon(
        "ReturnMonitor",
        icon_image,
        initial_tooltip,
        menu=menu
    )
    global_icon_ref = icon

    print(f"Displaying initial {'Success' if initial_success else 'Failure'} icon in system tray.")
    print(f"Will check status every {args.interval} seconds.")
    print("Right-click the icon for options.")

    check_thread = threading.Thread(target=periodic_check, args=(args, icon), daemon=True)
    check_thread.start()
    icon.run()

def main():
    parser = argparse.ArgumentParser(
        description="Run a command and show its status in the system tray.",
        usage="return-monitor [--interval SECONDS] -- command [args ...]"
    )
    
    parser.add_argument("command", nargs="+", help="The command to run and monitor.")
    parser.add_argument("--interval", type=int, default=30, help="Interval in seconds between checks.")
    parser.add_argument("--install", action="store_true", help="Install the script.")

    args = parser.parse_args()

    if not args.install:
        setup_and_run_tray(args)
    else:
        # Get the full path to the monitor executable
        monitor_path = shutil.which('return-monitor')
        if monitor_path is None:
            print("Error: 'return-monitor' executable not found in PATH.")
            print("Please activate the virtual environment and run 'return-monitor --install'.")
            sys.exit(1)
        
        # Construct the command string with proper quoting
        command_str = " ".join(shlex.quote(arg) for arg in args.command)
        
        # Construct the Exec line
        exec_line = f"{shlex.quote(monitor_path)} --interval {args.interval} -- {command_str}"
        
        # Expand the user's home directory and ensure the directory exists
        autostart_dir = os.path.expanduser("~/.config/autostart")
        os.makedirs(autostart_dir, exist_ok=True)
        
        # Write the .desktop file
        with open(os.path.join(autostart_dir, "return-monitor.desktop"), "w") as f:
            f.write(f"""[Desktop Entry]
Type=Application
Name=ReturnMonitor
Exec={exec_line}
Terminal=false
Categories=Utility;
X-GNOME-Autostart-enabled=true
""")
        print("Installed autostart entry.")

if __name__ == "__main__":
    main()
    print(f"ReturnMonitor has exited.")

