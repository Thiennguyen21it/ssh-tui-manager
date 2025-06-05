# SSH TUI Manager

A terminal-based user interface (TUI) for managing SSH connections, inspired by tools like lazygit.

## Features

- Manage a list of SSH hosts with details (hostname, username, port, etc.)
- Organize hosts into groups for better management
- Quick connect to any saved host with keyboard shortcuts
- Add, edit, and delete hosts directly from the interface
- Navigate using keyboard shortcuts or mouse
- Modern and intuitive terminal UI

## Installation

### Requirements

- Python 3.8+
- Required Python packages (see requirements.txt)

### Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/Thiennguyen21it/ssh-tui-manager.git
   cd ssh-tui-manager
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python main.py
   ```

## Usage

### Keyboard Shortcuts

- `q`: Quit the application
- `a`: Add a new host
- `e`: Edit the selected host
- `d`: Delete the selected host
- `c`: Connect to the selected host
- `f`: Filter hosts by group
- `r`: Refresh the host list
- `s`: Open SCP menu (file transfer)

### Managing Hosts

#### Adding a Host

1. Press `a` or click the "Add Host" button
2. Fill in the required fields:
   - Alias: A unique identifier for the host
   - Hostname: The IP address or domain name
   - Username: SSH username
   - Port: SSH port (default: 22)
   - Group (optional): Group name for organization
   - Description (optional): Additional information
   - Key Path (optional): Path to SSH private key file
3. Click "Save" to add the host

#### Editing a Host

1. Select a host from the list
2. Press `e` or click the "Edit Host" button
3. Modify the host details
4. Click "Save" to update the host

#### Deleting a Host

1. Select a host from the list
2. Press `d` or click the "Delete Host" button
3. Confirm the deletion

### Connecting to a Host

1. Select a host from the list
2. Press `c` or click the "Connect" button
3. The application will exit and open an SSH connection in your terminal

### Filtering Hosts by Group

1. Press `f` to focus the group filter dropdown
2. Select a group to filter the host list
3. Select "All" to show all hosts

## Configuration

Host data is stored in JSON format in the `config/ssh_hosts.json` file. You can manually edit this file if needed, but it's recommended to use the application interface.

## Development

### Project Structure

```
ssh-tui-manager/
├── src/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── ssh_client.py       # Logic for SSH connections and SCP operations
│   │   └── host_manager.py     # Host data management (load, save, edit hosts)
│   ├── tui/
│   │   ├── __init__.py
│   │   ├── interface.py        # TUI interface logic (commands, navigation)
│   │   └── dialogs.py          # Dialog screens for adding/editing hosts
│   └── utils/
│       ├── __init__.py
│       └── helpers.py          # Utility functions (input validation, etc.)
├── config/
│   └── ssh_hosts.json          # Stored host data (groups, hosts, aliases, etc.)
├── tests/
│   ├── __init__.py
│   ├── test_ssh_client.py      # Unit tests for SSH connections
│   ├── test_host_manager.py    # Unit tests for host management
│   └── test_interface.py       # Unit tests for TUI interactions
├── docs/
│   ├── README.md               # Project overview, setup, and usage
│   ├── CHANGELOG.md            # Version history and changes
│   └── CONTRIBUTING.md         # Guidelines for contributors
├── main.py                     # Entry point for the application
├── requirements.txt            # Project dependencies
└── .gitignore                  # Git ignore file
```

### Running Tests

```bash
pytest
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to contribute to this project.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
