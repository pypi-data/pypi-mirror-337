#!/usr/bin/env python3
"""
Command line entry point specifically for Claude Desktop integration.

This script is designed to be the target of the command in claude_desktop_config.json.
It sets up a basic Frida MCP server with STDIO transport for Claude to communicate with.
"""

import sys
import frida
from mcp.server.fastmcp import FastMCP, Context
from typing import Dict, List, Optional, Any, Union
import threading
import time

# Create the MCP server
mcp = FastMCP("Frida")

# Global dictionary to store scripts and their messages
# This allows us to retrieve messages from scripts after they've been created
_scripts = {}
_script_messages = {}
_message_locks = {}


@mcp.tool()
def list_processes() -> list:
    """List all processes running on the system."""
    device = frida.get_local_device()
    processes = device.enumerate_processes()
    return [{"pid": proc.pid, "name": proc.name} for proc in processes]


@mcp.tool()
def enumerate_processes() -> List[Dict[str, Any]]:
    """List all processes running on the system.
    
    Returns:
        A list of process information dictionaries containing:
        - pid: Process ID
        - name: Process name
    """
    device = frida.get_local_device()
    processes = device.enumerate_processes()
    return [{"pid": process.pid, "name": process.name} for process in processes]


@mcp.tool()
def enumerate_devices() -> List[Dict[str, Any]]:
    """List all devices connected to the system.
    
    Returns:
        A list of device information dictionaries containing:
        - id: Device ID
        - name: Device name
        - type: Device type
    """
    devices = frida.enumerate_devices()
    return [
        {
            "id": device.id,
            "name": device.name,
            "type": device.type,
        }
        for device in devices
    ]


@mcp.tool()
def get_device(device_id: str) -> Dict[str, Any]:
    """Get a device by its ID.
    
    Args:
        device_id: The ID of the device to get
        
    Returns:
        Information about the device
    """
    try:
        device = frida.get_device(device_id)
        return {
            "id": device.id,
            "name": device.name,
            "type": device.type,
        }
    except frida.InvalidArgumentError:
        raise ValueError(f"Device with ID {device_id} not found")


@mcp.tool()
def get_usb_device() -> Dict[str, Any]:
    """Get the USB device connected to the system.
    
    Returns:
        Information about the USB device
    """
    try:
        device = frida.get_usb_device()
        return {
            "id": device.id,
            "name": device.name,
            "type": device.type,
        }
    except frida.InvalidArgumentError:
        raise ValueError("No USB device found")


@mcp.tool()
def get_process_by_name(name: str) -> dict:
    """Find a process by name."""
    device = frida.get_local_device()
    for proc in device.enumerate_processes():
        if name.lower() in proc.name.lower():
            return {"pid": proc.pid, "name": proc.name, "found": True}
    return {"found": False, "error": f"Process '{name}' not found"}


@mcp.tool()
def attach_to_process(pid: int) -> dict:
    """Attach to a process by ID."""
    try:
        device = frida.get_local_device()
        session = device.attach(pid)
        return {
            "pid": pid,
            "success": True,
            "is_detached": False  # New session is not detached
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


# @mcp.tool()
# async def create_script(process_id: int, script_code: str, ctx: Context) -> Dict[str, Any]:
#     """Create and load a Frida script in the target process.
    
#     Args:
#         process_id: The ID of the process to attach to
#         script_code: The JavaScript code to inject
        
#     Returns:
#         Information about the created script
#     """
#     try:
#         # Attach to process
#         device = frida.get_local_device()
#         session = device.attach(process_id)
        
#         # Create script
#         script = session.create_script(script_code)
        
#         # Generate a unique script ID
#         script_id = f"script_{process_id}_{int(time.time())}"
        
#         # Store the script for later retrieval
#         _scripts[script_id] = script
#         _script_messages[script_id] = []
#         _message_locks[script_id] = threading.Lock()
        
#         # Set up message handler
#         def on_message(message, data):
#             with _message_locks[script_id]:
#                 message_type = message["type"]
#                 if message_type == "send":
#                     _script_messages[script_id].append({"payload": message["payload"]})
#                 elif message_type == "error":
#                     _script_messages[script_id].append({"error": message["description"]})
        
#         script.on("message", on_message)
        
#         # Load script
#         script.load()
        
#         return {
#             "status": "success",
#             "process_id": process_id,
#             "script_id": script_id,
#             "messages": _script_messages[script_id].copy()  # Return initial messages
#         }
    
#     except Exception as e:
#         return {
#             "status": "error",
#             "error": str(e)
#         }


# @mcp.tool()
# async def load_script_from_file(process_id: int, script_path: str, ctx: Context) -> Dict[str, Any]:
#     """Load a Frida script from a file in the target process.
    
#     Args:
#         process_id: The ID of the process to attach to
#         script_path: Path to the JavaScript file to load
        
#     Returns:
#         Information about the loaded script
#     """
#     try:
#         # Read the script file
#         try:
#             # Use the context to read the file as a resource if available
#             script_code, _ = await ctx.read_resource(f"file://{script_path}")
#         except:
#             # Fallback to standard file read if context read fails
#             with open(script_path, "r") as f:
#                 script_code = f.read()
        
#         # Now create the script using the existing tool
#         result = await create_script(process_id, script_code, ctx)
#         return result
    
#     except Exception as e:
#         return {
#             "status": "error",
#             "error": str(e)
#         }


@mcp.tool()
def create_simple_hook(pid: int, hook_type: str = "memory") -> dict:
    """Create a simple hook for a process."""
    script_code = ""
    
    if hook_type == "memory":
        script_code = """
        console.log("[*] Memory allocation hooks loaded");
        
        // Hook malloc on iOS/macOS
        Interceptor.attach(Module.findExportByName(null, 'malloc'), {
            onEnter: function(args) {
                const size = args[0].toInt32();
                if (size > 1024 * 1024) {  // Log allocations larger than 1MB
                    console.log(`[+] malloc(${size} bytes) called`);
                }
            }
        });
        
        send({type: 'status', message: 'Memory hooks installed'});
        """
    elif hook_type == "file":
        script_code = """
        console.log("[*] File operation hooks loaded");
        
        Interceptor.attach(Module.findExportByName(null, 'open'), {
            onEnter: function(args) {
                var path = args[0].readUtf8String();
                console.log(`[+] open(${path})`);
                this.path = path;
            },
            onLeave: function(retval) {
                console.log(`[+] open(${this.path}) returned: ${retval}`);
            }
        });
        
        send({type: 'status', message: 'File hooks installed'});
        """
    elif hook_type == "network":
        script_code = """
        console.log("[*] Network hooks loaded");
        
        Interceptor.attach(Module.findExportByName(null, 'connect'), {
            onEnter: function(args) {
                console.log(`[+] connect() called`);
            },
            onLeave: function(retval) {
                console.log(`[+] connect() returned: ${retval}`);
            }
        });
        
        send({type: 'status', message: 'Network hooks installed'});
        """
    else:
        return {"success": False, "error": f"Unknown hook type: {hook_type}"}
    
    try:
        device = frida.get_local_device()
        session = device.attach(pid)
        script = session.create_script(script_code)
        
        messages = []
        
        def on_message(message, data):
            messages.append(message)
        
        script.on("message", on_message)
        script.load()
        
        return {
            "success": True,
            "process_id": pid,
            "hook_type": hook_type,
            "messages": messages
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@mcp.tool()
def spawn_process(program: str, args: Optional[List[str]] = None, 
               device_id: Optional[str] = None) -> Dict[str, Any]:
    """Spawn a program.
    
    Args:
        program: The program to spawn
        args: Optional arguments for the program
        device_id: Optional device ID
        
    Returns:
        Information about the spawned process
    """
    try:
        if device_id:
            device = frida.get_device(device_id)
        else:
            device = frida.get_local_device()
            
        pid = device.spawn(program, args=args or [])
        
        return {"pid": pid}
    except Exception as e:
        raise ValueError(f"Failed to spawn {program}: {str(e)}")


@mcp.tool()
def resume_process(pid: int, device_id: Optional[str] = None) -> Dict[str, Any]:
    """Resume a process by ID.
    
    Args:
        pid: The ID of the process to resume
        device_id: Optional device ID
        
    Returns:
        Status information
    """
    try:
        if device_id:
            device = frida.get_device(device_id)
        else:
            device = frida.get_local_device()
            
        device.resume(pid)
        
        return {"success": True, "pid": pid}
    except Exception as e:
        raise ValueError(f"Failed to resume process {pid}: {str(e)}")


@mcp.tool()
def kill_process(pid: int, device_id: Optional[str] = None) -> Dict[str, Any]:
    """Kill a process by ID.
    
    Args:
        pid: The ID of the process to kill
        device_id: Optional device ID
        
    Returns:
        Status information
    """
    try:
        if device_id:
            device = frida.get_device(device_id)
        else:
            device = frida.get_local_device()
            
        device.kill(pid)
        
        return {"success": True, "pid": pid}
    except Exception as e:
        raise ValueError(f"Failed to kill process {pid}: {str(e)}")


@mcp.resource("frida://version")
def get_version() -> str:
    """Get the Frida version."""
    return frida.__version__


@mcp.resource("frida://processes")
def get_processes_resource() -> str:
    """Get a list of all processes as a readable string."""
    device = frida.get_local_device()
    processes = device.enumerate_processes()
    return "\n".join([f"PID: {p.pid}, Name: {p.name}" for p in processes])


@mcp.resource("frida://devices")
def get_devices_resource() -> str:
    """Get a list of all devices as a readable string."""
    devices = frida.enumerate_devices()
    return "\n".join([f"ID: {d.id}, Name: {d.name}, Type: {d.type}" for d in devices])


@mcp.resource("frida://example/hook")
def get_example_hook() -> str:
    """Get an example Frida hook script."""
    return """
    // Example Frida hook script
    
    // Hook file operations
    Interceptor.attach(Module.findExportByName(null, 'open'), {
        onEnter: function(args) {
            var path = args[0].readUtf8String();
            console.log(`[+] open(${path})`);
            this.path = path;
        },
        onLeave: function(retval) {
            console.log(`[+] open(${this.path}) returned: ${retval}`);
        }
    });
    
    // Hook network operations
    Interceptor.attach(Module.findExportByName(null, 'connect'), {
        onEnter: function(args) {
            // This is simplified - in reality you'd need to parse the sockaddr structure
            console.log(`[+] connect() called`);
        },
        onLeave: function(retval) {
            console.log(`[+] connect() returned: ${retval}`);
        }
    });
    
    // Send a message to Python
    send({type: 'status', message: 'Hooks installed'});
    """


@mcp.prompt()
def analyze_app_prompt(app_name: str) -> str:
    """Create a prompt to help analyze an application."""
    return f"""I want to analyze the {app_name} application using Frida.
Please help me create a strategy to:

1. Find the process
2. Identify key functions to hook
3. Monitor sensitive operations
4. Detect security vulnerabilities

What approach would you recommend for analyzing {app_name}?"""


@mcp.prompt()
def inject_script_prompt(process_id: int) -> str:
    """Create a prompt to help inject a script into a process."""
    return f"""I want to inject a Frida script into process {process_id}.
Please help me write a script to:
1. Hook common functions
2. Log interesting information
3. Manipulate program behavior if needed

What Frida script would you recommend?"""


@mcp.prompt()
def analyze_process_prompt(process_id: int) -> str:
    """Create a prompt to analyze a process."""
    return f"""I want to analyze process {process_id} using Frida.
Please guide me through:
1. Attaching to the process
2. Identifying interesting functions to hook
3. Finding important data structures
4. Creating effective instrumentation

What approach would you recommend?"""


# @mcp.tool()
# def get_script_messages(script_id: str) -> Dict[str, Any]:
#     """Get all messages from a script.
    
#     Args:
#         script_id: The ID of the script to get messages from
        
#     Returns:
#         A dictionary containing the messages from the script
#     """
#     if script_id not in _script_messages:
#         raise ValueError(f"Script with ID {script_id} not found")
    
#     with _message_locks[script_id]:
#         messages = _script_messages[script_id].copy()
    
#     return {
#         "script_id": script_id,
#         "message_count": len(messages),
#         "messages": messages
#     }


# @mcp.tool()
# def get_active_scripts() -> List[Dict[str, Any]]:
#     """Get a list of all active scripts.
    
#     Returns:
#         A list of dictionaries containing information about active scripts
#     """
#     result = []
    
#     for script_id, script in _scripts.items():
#         # Check if the script is still loaded
#         try:
#             is_destroyed = script.is_destroyed
#         except Exception:
#             is_destroyed = True
        
#         if not is_destroyed:
#             with _message_locks[script_id]:
#                 message_count = len(_script_messages[script_id])
            
#             result.append({
#                 "script_id": script_id,
#                 "message_count": message_count
#             })
    
#     return result


# @mcp.tool()
# def send_to_script(script_id: str, message: Any) -> Dict[str, Any]:
#     """Send a message to a script.
    
#     Args:
#         script_id: The ID of the script to send the message to
#         message: The message to send
        
#     Returns:
#         Status information
#     """
#     if script_id not in _scripts:
#         raise ValueError(f"Script with ID {script_id} not found")
    
#     script = _scripts[script_id]
    
#     try:
#         script.post(message)
#         return {
#             "success": True,
#             "script_id": script_id
#         }
#     except Exception as e:
#         return {
#             "success": False,
#             "script_id": script_id,
#             "error": str(e)
#         }


# @mcp.tool()
# def unload_script(script_id: str) -> Dict[str, Any]:
#     """Unload a script.
    
#     Args:
#         script_id: The ID of the script to unload
        
#     Returns:
#         Status information
#     """
#     if script_id not in _scripts:
#         raise ValueError(f"Script with ID {script_id} not found")
    
#     script = _scripts[script_id]
    
#     try:
#         script.unload()
#         return {
#             "success": True,
#             "script_id": script_id
#         }
#     except Exception as e:
#         return {
#             "success": False,
#             "script_id": script_id,
#             "error": str(e)
#         }


# @mcp.resource("frida://script/example")
# def get_example_script_with_communication() -> str:
#     """Get an example Frida script with two-way communication."""
#     return """
#     // Example Frida script with communication
    
#     // Listen for messages from Python
#     recv('ping', function(message) {
#         console.log('Received ping from Python');
#         send({type: 'pong', message: 'Hello from Frida!'});
#     });
    
#     // Hook file operations and send results back
#     Interceptor.attach(Module.findExportByName(null, 'open'), {
#         onEnter: function(args) {
#             var path = args[0].readUtf8String();
#             send({type: 'file_access', path: path, operation: 'open'});
#         }
#     });
    
#     // Send initial message
#     send({type: 'status', message: 'Script loaded and waiting for commands'});
#     """


@mcp.tool()
def create_interactive_session(process_id: int) -> Dict[str, Any]:
    """Create an interactive REPL-like session with a process.
    
    This returns a session ID that can be used with execute_in_session to run commands.
    
    Args:
        process_id: The ID of the process to attach to
        
    Returns:
        Information about the created session
    """
    try:
        # Attach to process
        device = frida.get_local_device()
        session = device.attach(process_id)
        
        # Generate a unique session ID
        session_id = f"session_{process_id}_{int(time.time())}"
        
        # Store the session
        _scripts[session_id] = session
        _script_messages[session_id] = []
        _message_locks[session_id] = threading.Lock()
        
        return {
            "status": "success",
            "process_id": process_id,
            "session_id": session_id,
            "message": f"Interactive session created for process {process_id}. Use execute_in_session to run JavaScript commands."
        }
    
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }


@mcp.tool()
def execute_in_session(session_id: str, javascript_code: str) -> Dict[str, Any]:
    """Execute JavaScript code in an interactive session.
    
    Args:
        session_id: The ID of the session to execute in
        javascript_code: The JavaScript code to execute
        
    Returns:
        The result of the execution
    """
    if session_id not in _scripts:
        raise ValueError(f"Session with ID {session_id} not found")
    
    session = _scripts[session_id]
    
    try:
        # For interactive use, we need to handle console.log output
        # and properly format the result
        
        # Wrap the code to capture console.log output and return values
        wrapped_code = f"""
        (function() {{
            // Capture console.log output
            var originalLog = console.log;
            var logs = [];
            
            console.log = function() {{
                var args = Array.prototype.slice.call(arguments);
                logs.push(args.map(function(arg) {{
                    return typeof arg === 'object' ? JSON.stringify(arg) : String(arg);
                }}).join(' '));
                originalLog.apply(console, arguments);
            }};
            
            // Execute the provided code
            var result;
            try {{
                result = eval({javascript_code!r});
            }} catch (e) {{
                send({{
                    type: 'error',
                    message: e.toString(),
                    stack: e.stack
                }});
                return;
            }}
            
            // Restore original console.log
            console.log = originalLog;
            
            // Send back the result and logs
            send({{
                type: 'result',
                result: result !== undefined ? result.toString() : 'undefined',
                logs: logs
            }});
        }})();
        """
        
        # Create a temporary script for this execution
        script = session.create_script(wrapped_code)
        
        # Store the results
        execution_results = []
        
        def on_message(message, data):
            if message["type"] == "send":
                execution_results.append(message["payload"])
            elif message["type"] == "error":
                execution_results.append({"error": message["description"]})
        
        script.on("message", on_message)
        
        # Load and wait for it to complete
        script.load()
        
        # Small wait to ensure messages are received
        time.sleep(0.1)
        
        # Format the result
        if execution_results:
            last_result = execution_results[-1]
            if "result" in last_result:
                result = {
                    "status": "success",
                    "result": last_result["result"],
                    "logs": last_result.get("logs", [])
                }
            elif "error" in last_result:
                result = {
                    "status": "error",
                    "error": last_result["error"],
                    "message": last_result.get("message", "")
                }
            else:
                result = {
                    "status": "success",
                    "raw_output": execution_results
                }
        else:
            result = {
                "status": "success",
                "result": "undefined",
                "logs": []
            }
        
        # Unload the temporary script
        script.unload()
        
        return result
    
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }


def main():
    """Run the CLI entry point for Claude Desktop integration."""
    # We deliberately don't process any arguments here - we just want basic STDIO mode
    # for Claude Desktop to talk to us
    mcp.run()


if __name__ == "__main__":
    main() 