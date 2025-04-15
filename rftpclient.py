import ftplib


def cmd_connect(hostname, username, password):
    """Connect to the FTP server."""
    try:
        ftp = ftplib.FTP(hostname)
        ftp.login(user=username, passwd=password)
        print(f"Connected to {hostname} as {username}.")
        return ftp
    except ftplib.all_errors as e:
        print(f"Failed to connect: {e}")
        return None

def cmd_disconnect(ftp):
    """Disconnect from the FTP server."""
    if ftp:
        ftp.quit()
        print("Disconnected from the server.")
    else:
        print("No active connection to disconnect.")


if __name__ == "__main__":
    cmd_map = {
        "connect": cmd_connect,
        "disconnect": cmd_disconnect,
    }

    running = True
    while running:
        command = input("Enter command (connect/disconnect): ").strip().lower()
        if command in cmd_map:
            if command == "connect":
                hostname = input("Enter hostname: ")
                username = input("Enter username: ")
                password = input("Enter password: ")
                ftp = cmd_map[command](hostname, username, password)
            elif command == "disconnect":
                running = False
                cmd_map[command](ftp)
        else:
            print("Unknown command. Please try again.")