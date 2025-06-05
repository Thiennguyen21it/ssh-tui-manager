import json
import os
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict

@dataclass
class SSHHost:
    host: str
    user: str
    port: int = 22
    alias: Optional[str] = None
    description: Optional[str] = None
    group: Optional[str] = None
    key_path: Optional[str] = None

class HostManager:
    def __init__(self, config_dir: str = "config"):
        self.config_dir = config_dir
        self.hosts_file = os.path.join(config_dir, "ssh_hosts.json")
        self._ensure_config_dir()
        self.hosts: Dict[str, SSHHost] = {}
        self.load_hosts()

    def _ensure_config_dir(self):
        """Ensure the config directory exists."""
        os.makedirs(self.config_dir, exist_ok=True)
        if not os.path.exists(self.hosts_file):
            self._save_hosts({})

    def load_hosts(self) -> None:
        """Load hosts from the JSON file."""
        try:
            with open(self.hosts_file, 'r') as f:
                data = json.load(f)
                self.hosts = {
                    alias: SSHHost(**host_data)
                    for alias, host_data in data.items()
                }
        except FileNotFoundError:
            self.hosts = {}
            self._save_hosts({})

    def _save_hosts(self, hosts: Dict[str, SSHHost]) -> None:
        """Save hosts to the JSON file."""
        with open(self.hosts_file, 'w') as f:
            json.dump(
                {alias: asdict(host) for alias, host in hosts.items()},
                f,
                indent=2
            )

    def add_host(self, host: SSHHost) -> None:
        """Add a new host."""
        if not host.alias:
            raise ValueError("Host alias is required")
        self.hosts[host.alias] = host
        self._save_hosts(self.hosts)

    def update_host(self, alias: str, host: SSHHost) -> None:
        """Update an existing host."""
        if alias not in self.hosts:
            raise KeyError(f"Host with alias '{alias}' not found")
        self.hosts[alias] = host
        self._save_hosts(self.hosts)

    def delete_host(self, alias: str) -> None:
        """Delete a host."""
        if alias not in self.hosts:
            raise KeyError(f"Host with alias '{alias}' not found")
        del self.hosts[alias]
        self._save_hosts(self.hosts)

    def get_host(self, alias: str) -> SSHHost:
        """Get a host by alias."""
        if alias not in self.hosts:
            raise KeyError(f"Host with alias '{alias}' not found")
        return self.hosts[alias]

    def get_all_hosts(self) -> List[SSHHost]:
        """Get all hosts."""
        return list(self.hosts.values())

    def get_hosts_by_group(self, group: str) -> List[SSHHost]:
        """Get all hosts in a specific group."""
        return [host for host in self.hosts.values() if host.group == group]

    def get_groups(self) -> List[str]:
        """Get all unique groups."""
        return list(set(host.group for host in self.hosts.values() if host.group)) 