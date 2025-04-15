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

def cmd_send(ftp, local_file, remote_file):
    """Send a file to the FTP server."""
    if ftp:
        try:
            with open(local_file, 'rb') as f:
                ftp.storbinary(f"STOR {remote_file}", f)
            print(f"Sent {local_file} to {remote_file}.")
        except FileNotFoundError:
            print(f"Local file {local_file} not found.")
        except ftplib.all_errors as e:
            print(f"Failed to send file: {e}")
    else:
        print("No active connection.")
        

def cmd_recv(ftp, remote_file, local_file):
    """Receive a file from the FTP server."""
    if ftp:
        try:
            with open(local_file, 'wb') as f:
                ftp.retrbinary(f"RETR {remote_file}", f.write)
            print(f"Received {remote_file} and saved as {local_file}.")
        except ftplib.all_errors as e:
            print(f"Failed to receive file: {e}")
    else:
        print("No active connection.")

def cmd_ls(ftp):
    """List files in the current directory."""
    if ftp:
        try:
            files = ftp.nlst()
            print("Files in current directory:")
            for file in files:
                print(file)
        except ftplib.all_errors as e:
            print(f"Failed to list files: {e}")
    else:
        print("No active connection.")

def cmd_cd(ftp, directory):
    """Change the current directory."""
    if ftp:
        try:
            ftp.cwd(directory)
            print(f"Changed directory to {directory}.")
        except ftplib.all_errors as e:
            print(f"Failed to change directory: {e}")
    else:
        print("No active connection.")

def cmd_mkdir(ftp, directory):
    """Create a new directory."""
    if ftp:
        try:
            ftp.mkd(directory)
            print(f"Created directory {directory}.")
        except ftplib.all_errors as e:
            print(f"Failed to create directory: {e}")
    else:
        print("No active connection.")

def cmd_rmdir(ftp, directory):
    """Remove a directory."""
    if ftp:
        try:
            ftp.rmd(directory)
            print(f"Removed directory {directory}.")
        except ftplib.all_errors as e:
            print(f"Failed to remove directory: {e}")
    else:
        print("No active connection.")


if __name__ == "__main__":
    cmd_map = {
        "connect": cmd_connect,
        "disconnect": cmd_disconnect,
        "ls": cmd_ls,
        "dir": cmd_ls,
        "exit": cmd_disconnect,
        "quit": cmd_disconnect,
        "send": cmd_send,
        "put": cmd_send,
        "recv": cmd_recv,
        "get": cmd_recv,
        "cd": cmd_cd,
        "mkdir": cmd_mkdir,
        "rmdir": cmd_rmdir,
    }

    running = True
    while running:
        command = input("rftpclient >> ").strip().lower()

        if command in cmd_map:
            if command == "connect":
                hostname = input("Enter hostname: ")
                username = input("Enter username: ")
                password = input("Enter password: ")
                ftp = cmd_map[command](hostname, username, password)
            elif command in ["ls", "dir"]:
                if ftp:
                    cmd_map[command](ftp)
                else:
                    print("No active connection.")
            elif command in ["exit", "quit"]:
                running = False
                cmd_map[command](ftp) # Disconnect before exiting
            elif command in ["send", "put"]:
                if ftp:
                    local_file = input("Enter local file path: ")
                    remote_file = input("Enter remote file name: ")
                    cmd_map[command](ftp, local_file, remote_file)
                else:
                    print("No active connection.")
            elif command in ["recv", "get"]:
                if ftp:
                    remote_file = input("Enter remote file name: ")
                    local_file = input("Enter local file path: ")
                    cmd_map[command](ftp, remote_file, local_file)
                else:
                    print("No active connection.")
            elif command in ["cd", "mkdir", "rmdir"]:
                if ftp:
                    directory = input("Enter directory path: ")
                    cmd_map[command](ftp, directory)
                else:
                    print("No active connection.")
            else:
                if ftp:
                    cmd_map[command](ftp)
                else:
                    print("No active connection.")
        else:
            print("Unknown command. Please try again.")