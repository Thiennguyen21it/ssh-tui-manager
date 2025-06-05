from textual.app import App, ComposeResult
from textual.containers import Container, Vertical
from textual.widgets import Header, Footer, DataTable, Button, Input, Select, Static
from textual.binding import Binding
from textual.reactive import reactive
from textual.screen import Screen
from textual import work
from typing import Optional, Dict, List, Any, Tuple
import subprocess
import os
import sys

from ..core.host_manager import HostManager, SSHHost
from ..core.ssh_client import SSHClient
from .dialogs import HostFormScreen, DeleteConfirmationScreen

class SSHManagerApp(App):
    CSS = """
    Screen {
        align: center middle;
    }

    #main-container {
        width: 100%;
        height: 100%;
        layout: grid;
        grid-size: 1 2;
        grid-rows: 1fr auto;
    }

    #host-table {
        width: 100%;
        height: 100%;
        border: solid green;
    }

    #action-bar {
        width: 100%;
        height: auto;
        layout: horizontal;
        background: $panel;
        padding: 1;
    }

    Button {
        width: auto;
        margin: 1;
    }

    #status-message {
        width: 100%;
        height: 1;
        dock: bottom;
        background: $surface;
        color: $text;
    }

    #group-filter {
        width: 20;
        margin: 1;
    }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("a", "add_host", "Add Host"),
        Binding("d", "delete_host", "Delete Host"),
        Binding("e", "edit_host", "Edit Host"),
        Binding("c", "connect", "Connect"),
        Binding("f", "group_filter", "Filter by Group"),
        Binding("r", "refresh", "Refresh"),
        Binding("s", "scp_menu", "SCP"),
    ]

    def __init__(self):
        super().__init__()
        self.host_manager = HostManager()
        self.ssh_client = SSHClient()
        self.selected_host: Optional[SSHHost] = None
        self.selected_group: Optional[str] = None
        self.status_message = ""

    def compose(self) -> ComposeResult:
        yield Header()
        with Container(id="main-container"):
            yield DataTable(id="host-table")
            with Container(id="action-bar"):
                # Initialize Select with default options
                yield Select([("all", "All Groups")], id="group-filter")
                yield Button("Add Host", id="add-btn", variant="primary")
                yield Button("Edit Host", id="edit-btn")
                yield Button("Delete Host", id="delete-btn", variant="error")
                yield Button("Connect", id="connect-btn", variant="success")
                yield Button("SCP", id="scp-btn")
        yield Static(id="status-message")
        yield Footer()

    def on_mount(self) -> None:
        self.title = "SSH Host Manager"
        self.sub_title = "Manage your SSH connections"
        
        # Initialize the data table
        table = self.query_one("#host-table")
        table.add_columns("Alias", "Host", "User", "Port", "Group", "Description")
        
        # Set initial group selection
        self.selected_group = "all"
        
        # Initialize group filter and refresh host table
        self.refresh_group_filter()
        self.refresh_host_table()
        
        # Update status message
        self.update_status("Ready")
        
        # Disable buttons initially since no host is selected
        self.update_button_states()

    def refresh_host_table(self) -> None:
        """Refresh the host table with current data."""
        table = self.query_one("#host-table")
        table.clear()
        
        hosts = (
            self.host_manager.get_hosts_by_group(self.selected_group)
            if self.selected_group and self.selected_group != "all"
            else self.host_manager.get_all_hosts()
        )
        
        for host in hosts:
            table.add_row(
                host.alias or "",
                host.host,
                host.user,
                str(host.port),
                host.group or "",
                host.description or ""
            )
            
        # Reset selected host
        self.selected_host = None
        
        # Update edit and delete buttons state
        self.update_button_states()

    def refresh_group_filter(self) -> None:
        """Refresh the group filter dropdown."""
        group_filter = self.query_one("#group-filter")
        
        # Get all unique groups
        groups = self.host_manager.get_groups()
        
        # Always include "All" option
        options = [("all", "All Groups")]
        
        # Add other groups if they exist
        if groups:
            options.extend([(group, group) for group in groups])
            
        # Set the options
        group_filter.options = options

    def update_button_states(self) -> None:
        """Update button states based on selection."""
        edit_btn = self.query_one("#edit-btn")
        delete_btn = self.query_one("#delete-btn")
        connect_btn = self.query_one("#connect-btn")
        scp_btn = self.query_one("#scp-btn")
        
        has_selection = self.selected_host is not None
        edit_btn.disabled = not has_selection
        delete_btn.disabled = not has_selection
        connect_btn.disabled = not has_selection
        scp_btn.disabled = not has_selection

    def update_status(self, message: str) -> None:
        """Update the status message."""
        status = self.query_one("#status-message")
        status.update(message)

    async def action_add_host(self) -> None:
        """Add a new host."""
        host_screen = HostFormScreen()
        result = await self.push_screen(host_screen)
        
        if result:
            try:
                self.host_manager.add_host(result)
                self.refresh_group_filter()  # Refresh groups first
                self.refresh_host_table()
                self.update_status(f"Host '{result.alias}' added successfully")
            except ValueError as e:
                self.update_status(f"Error: {str(e)}")

    async def action_edit_host(self) -> None:
        """Edit the selected host."""
        if not self.selected_host:
            self.update_status("No host selected")
            return
        
        host_screen = HostFormScreen(self.selected_host)
        result = await self.push_screen(host_screen)
        
        if result:
            host, original_alias = result
            try:
                self.host_manager.delete_host(original_alias)
                self.host_manager.add_host(host)
                self.refresh_group_filter()  # Refresh groups first
                self.refresh_host_table()
                self.update_status(f"Host '{host.alias}' updated successfully")
            except ValueError as e:
                self.update_status(f"Error: {str(e)}")

    async def action_delete_host(self) -> None:
        """Delete the selected host."""
        if not self.selected_host:
            self.update_status("No host selected")
            return
        
        confirm_screen = DeleteConfirmationScreen(self.selected_host.alias)
        confirmed = await self.push_screen(confirm_screen)
        
        if confirmed:
            try:
                alias = self.selected_host.alias
                self.host_manager.delete_host(alias)
                self.refresh_group_filter()  # Refresh groups first
                self.refresh_host_table()
                self.update_status(f"Host '{alias}' deleted successfully")
            except KeyError as e:
                self.update_status(f"Error: {str(e)}")

    def action_connect(self) -> None:
        """Connect to the selected host."""
        if not self.selected_host:
            self.update_status("No host selected")
            return
        
        host = self.selected_host
        self.update_status(f"Connecting to {host.host}...")
        
        # Build SSH command
        cmd = ["ssh"]
        
        # Add port if not default
        if host.port != 22:
            cmd.extend(["-p", str(host.port)])
        
        # Add key if provided
        if host.key_path:
            cmd.extend(["-i", host.key_path])
        
        # Add user@host
        cmd.append(f"{host.user}@{host.host}")
        
        # Exit the app and connect
        self.exit(lambda: self._connect_ssh(cmd))

    def _connect_ssh(self, cmd: List[str]) -> None:
        """Connect to SSH in the terminal."""
        try:
            # Clear the screen first
            if sys.platform == "win32":
                os.system("cls")
            else:
                os.system("clear")
                
            print(f"Connecting with command: {' '.join(cmd)}")
            subprocess.run(cmd)
        except Exception as e:
            print(f"Error connecting: {str(e)}")

    def action_group_filter(self) -> None:
        """Filter hosts by group."""
        group_filter = self.query_one("#group-filter")
        group_filter.focus()

    def action_refresh(self) -> None:
        """Refresh the host table."""
        self.host_manager.load_hosts()
        self.refresh_group_filter()  # Refresh groups first
        self.refresh_host_table()
        self.update_status("Refreshed host list")

    async def action_scp_menu(self) -> None:
        """Show SCP menu."""
        if not self.selected_host:
            self.update_status("No host selected")
            return
            
        # TODO: Implement SCP functionality
        self.update_status("SCP functionality not yet implemented")

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        """Handle row selection in the data table."""
        table = self.query_one("#host-table")
        if event.row_key is not None:
            row = table.get_row(event.row_key)
            alias = row[0]
            try:
                self.selected_host = self.host_manager.get_host(alias)
                self.update_status(f"Selected host: {alias}")
                self.update_button_states()
            except KeyError:
                self.update_status(f"Error: Host '{alias}' not found")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events."""
        button_id = event.button.id
        if button_id == "add-btn":
            self.action_add_host()
        elif button_id == "edit-btn":
            self.action_edit_host()
        elif button_id == "delete-btn":
            self.action_delete_host()
        elif button_id == "connect-btn":
            self.action_connect()
        elif button_id == "scp-btn":
            self.action_scp_menu()

    def on_select_changed(self, event: Select.Changed) -> None:
        """Handle group filter selection changes."""
        self.selected_group = event.value
        self.refresh_host_table() 