from textual.app import App, ComposeResult
from textual.containers import Container, Vertical
from textual.widgets import Header, Footer, DataTable, Button, Input, Select
from textual.binding import Binding
from textual.reactive import reactive
from typing import Optional
from ..core.host_manager import HostManager, SSHHost
from ..core.ssh_client import SSHClient

class SSHManagerApp(App):
    CSS = """
    Screen {
        align: center middle;
    }

    #host-table {
        width: 100%;
        height: 100%;
        border: solid green;
    }

    #action-buttons {
        width: 100%;
        height: auto;
        dock: bottom;
    }

    Button {
        width: auto;
        margin: 1;
    }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("a", "add_host", "Add Host"),
        Binding("d", "delete_host", "Delete Host"),
        Binding("e", "edit_host", "Edit Host"),
        Binding("c", "connect", "Connect"),
        Binding("g", "group_filter", "Filter by Group"),
    ]

    def __init__(self):
        super().__init__()
        self.host_manager = HostManager()
        self.ssh_client = SSHClient()
        self.selected_host: Optional[SSHHost] = None

    def compose(self) -> ComposeResult:
        yield Header()
        with Container():
            yield DataTable(id="host-table")
            with Vertical(id="action-buttons"):
                yield Button("Add Host", id="add-btn")
                yield Button("Edit Host", id="edit-btn")
                yield Button("Delete Host", id="delete-btn")
                yield Button("Connect", id="connect-btn")
                yield Select(id="group-filter")
        yield Footer()

    def on_mount(self) -> None:
        self.title = "SSH Host Manager"
        self.sub_title = "Manage your SSH connections"
        
        # Initialize the data table
        table = self.query_one("#host-table")
        table.add_columns("Alias", "Host", "User", "Port", "Group", "Description")
        self.refresh_host_table()

        # Initialize group filter
        group_filter = self.query_one("#group-filter")
        groups = ["All"] + self.host_manager.get_groups()
        group_filter.options = [(group, group) for group in groups]

    def refresh_host_table(self, group: Optional[str] = None) -> None:
        """Refresh the host table with current data."""
        table = self.query_one("#host-table")
        table.clear()
        
        hosts = (
            self.host_manager.get_hosts_by_group(group)
            if group and group != "All"
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

    def action_add_host(self) -> None:
        """Add a new host."""
        # TODO: Implement add host dialog
        pass

    def action_edit_host(self) -> None:
        """Edit the selected host."""
        # TODO: Implement edit host dialog
        pass

    def action_delete_host(self) -> None:
        """Delete the selected host."""
        # TODO: Implement delete host confirmation
        pass

    def action_connect(self) -> None:
        """Connect to the selected host."""
        # TODO: Implement SSH connection
        pass

    def action_group_filter(self) -> None:
        """Filter hosts by group."""
        # TODO: Implement group filtering
        pass

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        """Handle row selection in the data table."""
        row = event.row
        if row:
            alias = row[0]
            self.selected_host = self.host_manager.get_host(alias)

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

    def on_select_changed(self, event: Select.Changed) -> None:
        """Handle group filter selection changes."""
        self.refresh_host_table(event.value) 