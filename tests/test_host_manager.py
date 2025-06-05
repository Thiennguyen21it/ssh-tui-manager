import os
import pytest
import tempfile
import json
from src.core.host_manager import HostManager, SSHHost

class TestHostManager:
    @pytest.fixture
    def temp_config_dir(self):
        """Create a temporary config directory for testing."""
        with tempfile.TemporaryDirectory() as temp_dir:
            yield temp_dir

    @pytest.fixture
    def host_manager(self, temp_config_dir):
        """Create a host manager with a temporary config directory."""
        return HostManager(config_dir=temp_config_dir)

    def test_add_host(self, host_manager):
        """Test adding a host."""
        host = SSHHost(
            host="example.com",
            user="testuser",
            port=22,
            alias="test",
            description="Test host",
            group="test-group"
        )
        host_manager.add_host(host)
        
        # Check that the host was added
        assert "test" in host_manager.hosts
        assert host_manager.hosts["test"].host == "example.com"
        assert host_manager.hosts["test"].user == "testuser"

    def test_delete_host(self, host_manager):
        """Test deleting a host."""
        # Add a host first
        host = SSHHost(
            host="example.com",
            user="testuser",
            port=22,
            alias="test",
            description="Test host",
            group="test-group"
        )
        host_manager.add_host(host)
        
        # Delete the host
        host_manager.delete_host("test")
        
        # Check that the host was deleted
        assert "test" not in host_manager.hosts

    def test_update_host(self, host_manager):
        """Test updating a host."""
        # Add a host first
        host = SSHHost(
            host="example.com",
            user="testuser",
            port=22,
            alias="test",
            description="Test host",
            group="test-group"
        )
        host_manager.add_host(host)
        
        # Update the host
        updated_host = SSHHost(
            host="updated.com",
            user="updateduser",
            port=2222,
            alias="test",
            description="Updated host",
            group="updated-group"
        )
        host_manager.update_host("test", updated_host)
        
        # Check that the host was updated
        assert host_manager.hosts["test"].host == "updated.com"
        assert host_manager.hosts["test"].user == "updateduser"
        assert host_manager.hosts["test"].port == 2222

    def test_get_groups(self, host_manager):
        """Test getting groups."""
        # Add hosts with different groups
        host1 = SSHHost(
            host="example1.com",
            user="user1",
            alias="test1",
            group="group1"
        )
        host2 = SSHHost(
            host="example2.com",
            user="user2",
            alias="test2",
            group="group2"
        )
        host3 = SSHHost(
            host="example3.com",
            user="user3",
            alias="test3",
            group="group1"
        )
        
        host_manager.add_host(host1)
        host_manager.add_host(host2)
        host_manager.add_host(host3)
        
        # Get groups
        groups = host_manager.get_groups()
        
        # Check that the groups were returned
        assert len(groups) == 2
        assert "group1" in groups
        assert "group2" in groups

    def test_get_hosts_by_group(self, host_manager):
        """Test getting hosts by group."""
        # Add hosts with different groups
        host1 = SSHHost(
            host="example1.com",
            user="user1",
            alias="test1",
            group="group1"
        )
        host2 = SSHHost(
            host="example2.com",
            user="user2",
            alias="test2",
            group="group2"
        )
        host3 = SSHHost(
            host="example3.com",
            user="user3",
            alias="test3",
            group="group1"
        )
        
        host_manager.add_host(host1)
        host_manager.add_host(host2)
        host_manager.add_host(host3)
        
        # Get hosts by group
        group1_hosts = host_manager.get_hosts_by_group("group1")
        group2_hosts = host_manager.get_hosts_by_group("group2")
        
        # Check that the hosts were returned
        assert len(group1_hosts) == 2
        assert len(group2_hosts) == 1
        
        # Check that the hosts are in the correct groups
        for host in group1_hosts:
            assert host.group == "group1"
        
        for host in group2_hosts:
            assert host.group == "group2" 