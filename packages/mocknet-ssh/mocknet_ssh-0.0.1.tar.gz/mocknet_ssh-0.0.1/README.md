# MockNet SSH Server

The **MockNet SSH Server** is a Python-based tool designed to simulate SSH servers for various network devices. It supports multiple vendors and operating systems (OS), such as Cisco IOS, Cisco NX-OS, Cisco ASA, Palo Alto PAN-OS, and Fortinet. This tool is useful for testing automation scripts, training, or simulating network environments without requiring real hardware.

---

## Motivation

I was struggling to set up a lab with various network devices to test my code. I needed a simple SSH-based mock solution to test my code in GitHub Actions, providing consistent responses.

I came across a few projects with similar goals, but they were outdated, lacked active maintenance, or did not fully meet my requirements.

I wanted to avoid running containers or manually defining every command and its output. Instead, I decided to use the command outputs from the [Network to Code templates repository](https://github.com/networktocode/ntc-templates/tree/master), which are used for testing their parsers.

I also wanted to leverage `asyncssh` to support multiple concurrent tests against a single instance without performance issues. Setting up an SSH server with `asyncssh` is straightforward, and I wanted this project to be a Python module that I could easily import for testing on my local machine or in a GitHub runner.

---

## Features

- Simulates SSH servers for multiple vendors/OS.
- Dynamically loads command outputs from raw files.
- Supports vendor-specific commands and modes (e.g., `exec`, `enable`, `config`).
- Easily extensible to add new vendors/OS.
- Centralized logging for debugging and monitoring.

---

---

## Limitations

While the MockNet SSH Server is a powerful tool for simulating network devices, it has some limitations that users should be aware of:

1. **Show Commands Only**:
   - This tool is designed primarily for `show` commands. It does not support actual configuration changes or persistent state. Commands like `conf t` or `set` will not modify any internal state or configuration apart from the simulated mode that may change the prompt.

2. **File-Based Command Mapping**:
   - The server relies on raw command outputs stored in files. The name of the file must match the exact command (with spaces replaced by underscores). For example:
     - The command `show version` must correspond to a file named `show_version.txt` or `show_version.raw`.
     - This can be tricky for commands with dynamic parameters, such as `show bgp neighbor <IP>`. Each variation (e.g., `show bgp neighbor 192.168.1.1`) would require a separate file.

     For a command like `show bgp neighbor 192.168.1.1`, you would need to create a file named:

     ```bash
     cisco_ios_show_bgp_neighbor_192.168.1.1.txt
     ```
     
     If you have multiple neighbors, you would need to create separate files for each:
     ```bash
     cisco_ios_show_bgp_neighbor_192.168.1.1.txt
     cisco_ios_show_bgp_neighbor_192.168.1.2.txt
     cisco_ios_show_bgp_neighbor_10.0.0.1.txt
     ```
     This can become tedious for commands with many variations.

     The testfiles from the NTC templates sometimes have more that one filee per command. Then the filename contains a numbering at the end. In that case the command would be similar. A file `cisco_ios_show_version3.raw` woudl become the command `show version3`.



3. **No Dynamic Responses**:
   - The server provides static responses based on the content of the files. It does not dynamically generate responses based on the current state or input parameters.

4. **Limited Vendor-Specific Features**:
   - While the server supports vendor-specific commands and modes (e.g., `exec`, `enable`, `config`), it does not fully emulate the behavior of real devices. Advanced features like error handling, validation, or interactive prompts may not be implemented.

5. **No Persistent State**:
   - The server does not maintain a persistent state across sessions. For example, entering configuration mode (`conf t`) does not actually modify any settings or affect subsequent commands.

6. **Static Command Outputs**:
   - Commands always return the same output, as defined in the corresponding file. This may not reflect the dynamic nature of real devices, where outputs can change based on the device's state.

7. **File Management Overhead**:
   - Managing the raw command output files can be cumbersome, especially for commands with many variations or parameters. Users must ensure that the filenames are accurate and match the expected command format.

8. **No Authentication Beyond Username/Password**:
   - The server only supports basic username/password authentication. Advanced authentication mechanisms like public key authentication are not implemented.

9. **Not a Full Replacement for Real Devices**:
   - This tool is intended for testing and simulation purposes only. It is not a full replacement for real network devices and should not be used for production-grade testing of advanced features.


---

By understanding these limitations, you can better determine how to use the MockNet SSH Server effectively for your testing and simulation needs.


---


## Installation

1. Clone the repository:
   ```bash
   pip install mocknet_ssh
   ```

2. Run the server for a test if the installation was successful:
   ```bash
   python -m mocknet_ssh --platform cisco_ios
   ```

---

## Usage

### Starting the MockNet SSH Server

To start the server, use the `start_mock_server` function from `mocknet_ssh`. Specify the platform, username, password, and port.

Example:
```python
from mocknet_ssh.api import start_mock_server

# Start a Cisco IOS mock server
start_mock_server(platform="cisco_ios", username="testadmin", password="1234", port=9999)
```

### Connecting to the Server

Use an SSH client to connect to the server:
```bash
ssh testadmin@127.0.0.1 -p 9999
```

Enter the password (`1234` in this example) to log in.

---

## Supported Platforms

The following platforms are supported out of the box:

- **Cisco IOS**
- **Cisco NX-OS**
- **Cisco ASA**
- **Palo Alto PAN-OS**
- **Fortinet**

Each platform has its own handler and supports vendor-specific commands.

---

## Examples

### Cisco IOS Example

1. Start the Cisco IOS mock server:
   ```python
   start_mock_server(platform="cisco_ios", username="testadmin", password="1234", port=9999)
   ```

2. Connect to the server:
   ```bash
   ssh testadmin@127.0.0.1 -p 9999
   ```

3. Example commands:
   - `enable`: Enter enable mode.
   - `conf t`: Enter configuration mode.
   - `show version`: Display version information.
   - `exit`: Exit the current mode or session.

---


## Logging

The server uses centralized logging for debugging and monitoring. Logs are written to the console by default.

Example log output:
```
2025-03-30 12:00:00 [INFO] Creating SSH listener on 127.0.0.1, port 9999
2025-03-30 12:00:01 [INFO] 🚀 SSH mock server running on 127.0.0.1:9999
2025-03-30 12:00:05 [INFO] 📡 SSH session channel opened
2025-03-30 12:00:10 [INFO] 🔧 Command received: show version
```

---

## Contributing

Contributions are welcome! If you'd like to add new features or fix bugs, please submit a pull request.
If you would like to add new vendors see instructions below.

## Adding a New Vendor/OS

To add support for a new vendor/OS, follow these steps:

### 1. Create a New Handler

1. Create a new Python file in the `mocknet_ssh/handlers` directory. For example:
   ```bash
   touch mocknet_ssh/handlers/new_vendor.py
   ```

2. Implement a handler class by extending `asyncssh.SSHServerSession`. Use the existing handlers (e.g., `CiscoIOSHandler`) as a reference.

Example:
```python
import asyncssh
from pathlib import Path
from typing import Dict

class NewVendorHandler(asyncssh.SSHServerSession):
    def __init__(self) -> None:
        self._chan = None
        self._buffer = ""
        self.mode = "exec"
        self.dynamic_commands: Dict[str, Path] = {}

    def connection_made(self, chan: asyncssh.SSHServerChannel) -> None:
        self._chan = chan
        self._chan.write("Welcome to New Vendor OS\n")

    def data_received(self, data: str, datatype: asyncssh.DataType) -> None:
        # Handle incoming commands
        pass
```

### 2. Add Raw Command Outputs

1. Create a directory for the new vendor's command outputs:
   ```bash
   mkdir -p mocknet_ssh/handlers/command_output/new_vendor
   ```

2. Copy raw command outputs from the real device into this directory. Use filenames that match the commands, replacing spaces with underscores (`_`).

Example:
- `show_version.txt` for the `show version` command.
- `show_running_config.txt` for the `show running-config` command.

### 3. Register the Handler

1. Open `mocknet_ssh/api.py`.
2. Add the new handler to the `PLATFORM_HANDLERS` dictionary:
   ```python
   from mocknet_ssh.handlers.new_vendor import NewVendorHandler

   PLATFORM_HANDLERS: dict[str, Type[asyncssh.SSHServerSession]] = {
       "new_vendor": NewVendorHandler,
       # Other platforms...
   }
   ```

### 4. Test the New Vendor

1. Start the server for the new vendor:
   ```python
   start_mock_server(platform="new_vendor", username="admin", password="password", port=9999)
   ```

2. Connect to the server and test the commands.
---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
