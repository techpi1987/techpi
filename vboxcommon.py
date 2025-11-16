import virtualbox
from virtualbox.library import MachineState
import time

# Constants
LONG_WAIT = "⏳ This might take a while..."

def get_vbox():
    """Get VirtualBox instance"""
    return virtualbox.VirtualBox()

def get_session():
    """Get VirtualBox session"""
    return virtualbox.Session()

def get_vm_uuid(vm_name):
    """Get VM UUID by name"""
    try:
        machine = get_vbox().find_machine(vm_name)
        return str(machine.id_)
    except:
        return None

def get_vm_state(vm_uuid):
    """Get VM state"""
    machine = get_vbox().find_machine(vm_uuid)
    return str(machine.state)

def ensure_vm_running(vm_uuid):
    """Ensure VM is running"""
    machine = get_vbox().find_machine(vm_uuid)
    if machine.state != MachineState.running:
        session = get_session()
        progress = machine.launch_vm_process(session, "gui", [])
        progress.wait_for_completion()
        session.unlock_machine()
        time.sleep(5)  # Give the VM some time to fully start

def control_guest(vm_uuid, username, password, commands, wait_stdout=False):
    """Control guest VM using VBox guest control"""
    machine = get_vbox().find_machine(vm_uuid)
    session = get_session()
    
    try:
        machine.lock_machine(session, virtualbox.library.LockType.shared)
        guest = session.console.guest
        
        # Wait for guest to be ready
        while not guest.additions_run_level:
            time.sleep(1)
            
        guest_session = guest.create_session(username, password)
        
        if commands[0] == "run":
            process = guest_session.process_create(
                commands[1],  # path
                commands[2:],  # arguments
                [],  # environment
                [virtualbox.library.ProcessCreateFlag.wait_for_process_start],
            )
            if wait_stdout:
                while True:
                    try:
                        stdout = process.read(1, 65536, 0)
                        if stdout:
                            print(stdout.decode(), end="")
                        else:
                            break
                    except:
                        break
            process.wait_for(0, 0)
            
        elif commands[0] == "copyto":
            guest_session.directory_create(commands[3], 0o755)  # Create target directory
            guest_session.file_copy_to_guest(commands[2], commands[3])
            
        elif commands[0] == "copyfrom":
            guest_session.file_copy_from_guest(commands[2], commands[3])
            
    finally:
        if 'guest_session' in locals():
            guest_session.close()
        session.unlock_machine()

def take_snapshot(vm_uuid, name, power_off=False, wait=False):
    """Take VM snapshot"""
    machine = get_vbox().find_machine(vm_uuid)
    if power_off and machine.state == MachineState.running:
        session = get_session()
        machine.lock_machine(session, virtualbox.library.LockType.shared)
        progress = session.console.power_down()
        progress.wait_for_completion()
        session.unlock_machine()
        
    machine.take_snapshot(name, f"Snapshot {name}", True)
    if wait:
        while machine.snapshot_count == 0 or machine.current_snapshot.name != name:
            time.sleep(1)

def restore_snapshot(vm_uuid, name):
    """Restore VM snapshot"""
    machine = get_vbox().find_machine(vm_uuid)
    snapshot = machine.find_snapshot(name)
    if snapshot:
        session = get_session()
        progress = machine.restore_snapshot(snapshot)
        progress.wait_for_completion()
        session.unlock_machine()
    else:
        raise RuntimeError(f"Snapshot {name} not found")

def export_vm(vm_uuid, name, description=""):
    """Export VM to OVA"""
    machine = get_vbox().find_machine(vm_uuid)
    appliance = get_vbox().create_appliance()
    machine.export_to(appliance, description)
    progress = appliance.write("output.ova", [], description)
    progress.wait_for_completion()

def set_network_to_hostonly(vm_uuid):
    """Set VM network adapter to host-only"""
    machine = get_vbox().find_machine(vm_uuid)
    adapter = machine.get_network_adapter(0)
    adapter.attachment_type = virtualbox.library.NetworkAttachmentType.host_only
    machine.save_settings()