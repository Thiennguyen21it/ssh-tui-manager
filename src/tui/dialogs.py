from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label, Select
from textual.validation import Validator

from ..core.host_manager import SSHHost
from ..utils.helpers import (
    validate_hostname, 
    validate_port, 
    validate_username, 
    validate_key_path,
    expand_path
)

class HostFormScreen(ModalScreen):
    """Base screen for adding or editing a host."""
    
    CSS = """
    HostFormScreen {
        align: center middle;
    }
    
    #dialog {
        width: 60;
        height: auto;
        border: thick $accent;
        padding: 1 2;
        background: $surface;
    }
    
    #form {
        height: auto;
        width: 100%;
    }
    
    .form-row {
        height: 3;
        margin-bottom: 1;
        width: 100%;
        layout: horizontal;
    }
    
    .form-row Label {
        width: 15;
        padding-top: 1;
    }
    
    .form-row Input, .form-row Select {
        width: 1fr;
    }
    
    #buttons {
        width: 100%;
        height: 3;
        align: center middle;
    }
    
    #buttons Button {
        margin: 0 1;
    }
    """
    
    def __init__(self, host: SSHHost = None):
        """Initialize the form screen.
        
        Args:
            host: Optional host to edit. If None, a new host will be created.
        """
        super().__init__()
        self.host = host
        self.editing = host is not None
        self.original_alias = host.alias if host else None
    
    def compose(self) -> ComposeResult:
        """Compose the form screen."""
        with Container(id="dialog"):
            yield Label(
                "Edit Host" if self.editing else "Add Host",
                id="title"
            )
            
            with Vertical(id="form"):
                with Container(classes="form-row"):
                    yield Label("Alias:")
                    yield Input(
                        id="alias",
                        value=self.host.alias if self.host else "",
                        placeholder="Unique identifier for this host"
                    )
                
                with Container(classes="form-row"):
                    yield Label("Hostname:")
                    yield Input(
                        id="hostname",
                        value=self.host.host if self.host else "",
                        placeholder="IP address or hostname"
                    )
                
                with Container(classes="form-row"):
                    yield Label("Username:")
                    yield Input(
                        id="username",
                        value=self.host.user if self.host else "",
                        placeholder="SSH username"
                    )
                
                with Container(classes="form-row"):
                    yield Label("Port:")
                    yield Input(
                        id="port",
                        value=str(self.host.port) if self.host else "22",
                        placeholder="SSH port (default: 22)"
                    )
                
                with Container(classes="form-row"):
                    yield Label("Group:")
                    yield Input(
                        id="group",
                        value=self.host.group if self.host else "",
                        placeholder="Optional group for organizing hosts"
                    )
                
                with Container(classes="form-row"):
                    yield Label("Description:")
                    yield Input(
                        id="description",
                        value=self.host.description if self.host else "",
                        placeholder="Optional description"
                    )
                
                with Container(classes="form-row"):
                    yield Label("Key Path:")
                    yield Input(
                        id="key_path",
                        value=self.host.key_path if self.host else "",
                        placeholder="Path to SSH key file (optional)"
                    )
            
            with Container(id="buttons"):
                yield Button("Save", id="save")
                yield Button("Cancel", id="cancel")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "cancel":
            self.dismiss(None)
        elif event.button.id == "save":
            self._save_host()
    
    def _save_host(self) -> None:
        """Validate and save the host."""
        # Get form values
        alias = self.query_one("#alias").value
        hostname = self.query_one("#hostname").value
        username = self.query_one("#username").value
        port_str = self.query_one("#port").value
        group = self.query_one("#group").value or None
        description = self.query_one("#description").value or None
        key_path = self.query_one("#key_path").value or None
        
        # Validate inputs
        valid, errors = self._validate_inputs(alias, hostname, username, port_str, key_path)
        
        if not valid:
            # TODO: Show validation errors
            return
        
        # Create or update host
        host = SSHHost(
            host=hostname,
            user=username,
            port=int(port_str),
            alias=alias,
            description=description,
            group=group,
            key_path=expand_path(key_path) if key_path else None
        )
        
        # Return the host and original alias if editing
        if self.editing:
            self.dismiss((host, self.original_alias))
        else:
            self.dismiss(host)
    
    def _validate_inputs(self, alias, hostname, username, port_str, key_path):
        """Validate form inputs."""
        errors = []
        
        # Validate required fields
        if not alias:
            errors.append("Alias is required")
        
        # Validate hostname
        valid, error = validate_hostname(hostname)
        if not valid:
            errors.append(error)
        
        # Validate username
        valid, error = validate_username(username)
        if not valid:
            errors.append(error)
        
        # Validate port
        valid, error = validate_port(port_str)
        if not valid:
            errors.append(error)
        
        # Validate key path if provided
        if key_path:
            expanded_path = expand_path(key_path)
            valid, error = validate_key_path(expanded_path)
            if not valid:
                errors.append(error)
        
        return len(errors) == 0, errors

class DeleteConfirmationScreen(ModalScreen):
    """Screen for confirming host deletion."""
    
    CSS = """
    DeleteConfirmationScreen {
        align: center middle;
    }
    
    #dialog {
        width: 40;
        height: auto;
        border: thick $error;
        padding: 1 2;
        background: $surface;
    }
    
    #buttons {
        width: 100%;
        height: 3;
        align: center middle;
        margin-top: 1;
    }
    
    #buttons Button {
        margin: 0 1;
    }
    
    #delete-btn {
        background: $error;
    }
    """
    
    def __init__(self, host_alias: str):
        """Initialize the confirmation screen.
        
        Args:
            host_alias: The alias of the host to delete.
        """
        super().__init__()
        self.host_alias = host_alias
    
    def compose(self) -> ComposeResult:
        """Compose the confirmation screen."""
        with Container(id="dialog"):
            yield Label(f"Delete host '{self.host_alias}'?")
            yield Label("This action cannot be undone.")
            
            with Container(id="buttons"):
                yield Button("Delete", id="delete-btn")
                yield Button("Cancel", id="cancel-btn")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "cancel-btn":
            self.dismiss(False)
        elif event.button.id == "delete-btn":
            self.dismiss(True) 