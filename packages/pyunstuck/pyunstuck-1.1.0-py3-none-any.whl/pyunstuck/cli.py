"""
PyUnstuck - Python Script Debugging and Interruption Tool
A debugging tool that helps you analyze and attempt to terminate frozen Python scripts.

@Version: 1.1.0
@Platform: Windows (primary) / Linux / MacOS
@Python: >= 3.11

Key improvements in this version:
1. Clear disclaimers on Python thread killing limitations.
2. Optional detection for potential lock cycles in pure Python code.
3. More explicit warnings when force-kill fails.
"""

import sys
import threading
import runpy
import time
import ctypes
import os

import keyboard
import signal
import io

# =====================================================
# 1) Output capture (so we can show script output in real-time)
# =====================================================

class OutputCapture:
    """
    Thread-safe stdout capture utility
    """
    def __init__(self):
        self.output = []
        self._lock = threading.Lock()

    def write(self, text):
        with self._lock:
            self.output.append(text)
            sys.__stdout__.write(text)

    def flush(self):
        sys.__stdout__.flush()

    def get_recent_output(self, lines=50):
        with self._lock:
            # Return the last 'lines' lines worth of text
            # (Here we approximate by last 50 appended entries, might be incomplete lines)
            return ''.join(self.output[-lines:])

# Create a global output capture
output_capture = OutputCapture()

# =====================================================
# 2) Utility: Ask user for script path & set environment
# =====================================================

def ask_script_path():
    """
    Prompt for the target script path from user input and return absolute path
    """
    script_path = input("Enter the script path to monitor: ").strip()
    if not script_path:
        print("Script path cannot be empty!")
        sys.exit(1)

    # Convert to absolute path
    script_path = os.path.abspath(script_path)
    if not os.path.exists(script_path):
        print(f"Script path does not exist: {script_path}")
        sys.exit(1)
    return script_path

def setup_script_environment(script_path):
    """
    Setup script runtime environment
    - Add script directory to Python path
    - Change working directory to script directory
    """
    script_dir = os.path.dirname(os.path.abspath(script_path))

    # Add to Python path if not already present
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)

    # Change working directory
    original_dir = os.getcwd()
    os.chdir(script_dir)

    return original_dir

# =====================================================
# 3) Running script in a background thread
# =====================================================

def run_script_in_thread(script_path):
    """
    Execute target script in a new thread
    """
    original_dir = setup_script_environment(script_path)
    try:
        # Redirect stdout to our capture
        sys.stdout = output_capture
        runpy.run_path(script_path, run_name="__main__")
    finally:
        # Restore stdout and directory
        sys.stdout = sys.__stdout__
        os.chdir(original_dir)

# =====================================================
# 4) Stack trace analysis
# =====================================================

def get_file_context(filename, lineno, context_lines=2):
    """
    Get code context around specified line number
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        start = max(0, lineno - context_lines - 1)
        end = min(len(lines), lineno + context_lines)

        context = []
        for i in range(start, end):
            line_num = i + 1
            prefix = '  > ' if line_num == lineno else '    '
            if line_num == lineno:
                # Highlight current line
                context.append(
                    f"\033[1;90m{prefix}{line_num:4d}|\033[0m \033[48;2;100;181;246m\033[38;2;227;242;253m{lines[i].rstrip()}\033[0m"
                )
            else:
                context.append(
                    f"\033[1;90m{prefix}{line_num:4d}|\033[0m {lines[i].rstrip()}"
                )
        return '\n'.join(context)
    except:
        return None

def print_stack(thread_id):
    """
    Print call stack of specified thread (accurate to line number),
    using Rust compiler-like format, and show source code context
    """
    frames_map = sys._current_frames()
    if thread_id not in frames_map:
        print("\033[1;31merror\033[0m: Thread stack not found, thread may have exited.")
        return

    stack = frames_map[thread_id]
    print("\n\033[1;34m╔═══ Stack Trace Captured (thread_id = {}) ═══╗\033[0m".format(thread_id))
    frame_count = 0

    while stack:
        frame = stack
        code = frame.f_code
        lineno = frame.f_lineno
        filename = code.co_filename
        funcname = code.co_name

        # Add frame number
        frame_prefix = f"\033[1;36m{frame_count:>2}\033[0m: "
        location = f"\033[1;33m{filename}:{lineno}\033[0m"
        func_info = f"\033[1;32m{funcname}\033[0m"

        print(f"\n{frame_prefix}at {location}")
        print(f"     \033[1;90m└─\033[0m in {func_info}")

        # Show local variables
        if frame.f_locals:
            print("     \033[1;90m└─\033[0m Local Variables:")
            for key, value in frame.f_locals.items():
                if not key.startswith('__'):
                    try:
                        val_str = str(value)
                        if len(val_str) > 50:  # Truncate very long values
                            val_str = val_str[:47] + "..."
                        print(f"       \033[1;90m|\033[0m \033[1;35m{key}\033[0m = {val_str}")
                    except:
                        print(f"       \033[1;90m|\033[0m \033[1;35m{key}\033[0m = <unable to display>")

        # Show source code context if possible
        if os.path.exists(filename) and filename.endswith('.py'):
            print("     \033[1;90m└─\033[0m Source Context:")
            context = get_file_context(filename, lineno)
            if context:
                print("       \033[1;90m|\033[0m")
                for line in context.split('\n'):
                    print(f"       \033[1;90m|\033[0m {line}")
                print("       \033[1;90m|\033[0m")

        frame_count += 1
        stack = stack.f_back

    print("\033[1;34m╚════════════════════════════════════╝\033[0m\n")

# =====================================================
# 5) (Optional) Attempt to detect lock ownership & cycle
# =====================================================

def detect_potential_lock_cycle():
    """
    Attempt to detect potential lock cycles among pure Python threads using
    standard 'threading.Lock' or 'threading.RLock' objects. This is a best-effort
    approach and will NOT detect C-level locks or third-party extension locks.

    Method:
      1) For each alive thread, gather info: which lock is it currently waiting to acquire (if any),
         and which locks it currently owns (if it's an RLock with an _owner attr, etc.).
      2) Build a wait-for graph:
         - Node: a thread or lock object
         - Edge: T1 -> L if T1 is waiting on L
                 L -> T2 if L is owned by T2
      3) Check if there's a cycle in this directed graph.

    Caveats:
      - 'threading.Lock' in Python doesn't have a public "owner" field. 'RLock' has an '_owner',
        but it's not official API and may break in future Python versions.
      - If a lock is stuck in C extension or a custom object, we won't detect it.
      - This is purely experimental and for demonstration.
    """
    import threading

    # Grab snapshots of frames
    frames_map = sys._current_frames()
    alive_threads = []
    for t in threading.enumerate():
        if t.is_alive():
            alive_threads.append(t)

    # Data structures
    waiting_map = {}  # thread_id -> lock obj that this thread might be waiting for
    owned_map = {}    # thread_id -> set of locks that are currently owned by this thread
    lock_held_by = {} # lock_obj -> thread_id (which thread might own it)

    for t in alive_threads:
        # Initialize sets
        owned_map[t.ident] = set()
        waiting_map[t.ident] = None

    # Heuristics: parse each thread's top frame for something like lock.acquire()
    # For RLock, check lock._owner to see if it matches t.ident
    import traceback

    for t in alive_threads:
        f = frames_map.get(t.ident)
        while f:
            # Inspect function name
            code = f.f_code
            if code.co_name in ("acquire", "_acquire_restore"):
                # Possibly waiting on a lock
                # Try to see if 'self' in locals is a lock
                possible_lock = f.f_locals.get('self')
                if possible_lock and ('threading' in str(type(possible_lock))):
                    waiting_map[t.ident] = possible_lock
            # Inspect local variables to see if there's an RLock we own
            for varname, varvalue in f.f_locals.items():
                # Check if it's a standard RLock
                if 'RLock' in str(type(varvalue)):
                    # RLock in cpython might have an _owner internal attribute
                    # If it's the same as t.ident, we consider it "owned"
                    owner = getattr(varvalue, '_owner', None)
                    if owner == t.ident:
                        owned_map[t.ident].add(varvalue)

            f = f.f_back

    # Now build a graph: we have thread nodes & lock nodes
    # Edges:
    # 1) T -> L if T is waiting on L
    # 2) L -> T if L is owned by T
    # We'll store them as adjacency list
    graph = {}

    def add_edge(a, b):
        graph.setdefault(a, set()).add(b)

    # Fill edges
    for t in alive_threads:
        tid = t.ident
        lock_waiting = waiting_map[tid]
        if lock_waiting:
            add_edge(('thread', tid), ('lock', id(lock_waiting)))
        for lock_obj in owned_map[tid]:
            # lock -> thread is "lock owned by thread"
            add_edge(('lock', id(lock_obj)), ('thread', tid))

    # We do a simple DFS to see if there's a cycle
    visited = set()
    stack = set()

    def dfs(node):
        if node in stack:
            return True  # found cycle
        if node in visited:
            return False
        visited.add(node)
        stack.add(node)
        for nxt in graph.get(node, []):
            if dfs(nxt):
                return True
        stack.remove(node)
        return False

    # Check for cycle
    for node in graph:
        if dfs(node):
            print("\033[1;31m[DETECT]\033[0m Potential lock cycle detected among Python threads/locks!")
            print("    This is a best-effort guess. Some locks may be C-level or untracked.")
            print("    Recommend manual inspection or reorganizing concurrency design.\n")
            return

    print("\033[1;34m[INFO]\033[0m No obvious Python-level lock cycle found (or not detectable).")

# =====================================================
# 6) Force-terminate attempt
# =====================================================

def kill_thread(thread, exc_type=SystemExit):
    """
    Force terminate target thread by raising specified exception using ctypes.
    NOTE: This approach has major limitations:
      - In Python, there's no real 'kill thread' from outside.
      - This just injects an exception; if the thread is stuck at C level or
        ignoring exceptions (like holding a low-level lock), it won't help.
      - Could lead to corrupted interpreter state if the thread was in the middle
        of critical operation.
    """
    if not thread or not thread.is_alive():
        print("Thread is not alive or invalid.")
        return

    tid = thread.native_id  # use target thread's native_id
    if not tid:
        print("Unable to get thread ID (native_id = None).")
        return

    # Attempt to raise an exception in the target thread
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
        ctypes.c_ulong(tid),
        ctypes.py_object(exc_type)
    )
    if res == 0:
        print("Force termination failed: Thread ID not found.")
    elif res > 1:
        # If return value > 1, something went wrong, need to call again to recover
        ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_ulong(tid), None)
        print("Force termination error: Multiple threads affected, recovered.")

# =====================================================
# 7) Handling debug interrupt (Ctrl+Shift+C)
# =====================================================

def handle_debug_interrupt(worker):
    """
    Handle debug interrupt (Ctrl+Shift+C):
    - Print stack trace
    - Offer user menu: continue, gentle kill, force kill, check lock cycle, or exit
    - Return True if user wants to continue, False if user wants to stop monitoring
    """
    print("\n\033[1;33m[WARN]\033[0m Debug interrupt (Ctrl+Shift+C) detected, analyzing target script's stack...")
    print_stack(worker.ident)

    while True:
        choice = input(
            "\n\033[1;33m[PROMPT]\033[0m Options:\n"
            "1. Continue execution\n"
            "2. Try gentle termination (KeyboardInterrupt)\n"
            "3. Force kill thread (SystemExit / SystemError)\n"
            "4. (Optional) Attempt lock-cycle detection\n"
            "5. Exit pyunstuck (Emergency exit the entire process)\n"
            "Choice (1/2/3/4/5): "
        ).strip()

        if choice == '1':
            print("\033[1;32m[INFO]\033[0m Continuing script execution...\n")
            return True

        elif choice == '2':
            print("\033[1;31m[ALERT]\033[0m Attempting to terminate thread gently with KeyboardInterrupt...")
            kill_thread(worker, KeyboardInterrupt)
            time.sleep(1)
            if not worker.is_alive():
                print("\033[1;32m[SUCCESS]\033[0m Thread terminated successfully.\n")
                return False
            print("\033[1;31m[WARN]\033[0m Gentle termination failed. Thread is still alive.\n")
            return True

        elif choice == '3':
            print("\033[1;31m[ALERT]\033[0m Force killing thread (multiple attempts)...")
            for exc in [SystemExit, SystemError, Exception]:
                kill_thread(worker, exc)
                time.sleep(0.5)
                if not worker.is_alive():
                    print("\033[1;32m[SUCCESS]\033[0m Thread terminated successfully.\n")
                    return False
            print("\033[1;31m[ERROR]\033[0m All force-kill attempts failed.\n"
                  "The thread may be stuck in a C extension or holding a fatal lock. "
                  "Consider terminating the entire Python process.\n")
            return True

        elif choice == '4':
            print("\n\033[1;34m[INFO]\033[0m Attempting to detect Python-level lock cycles...\n")
            detect_potential_lock_cycle()
            print("")
            # Return to the same prompt cycle
            continue

        elif choice == '5':
            print("\033[1;31m[ALERT]\033[0m Emergency exit initiated. Terminating pyunstuck (and entire Python process)...")
            os._exit(1)  # Force exit the entire process

        else:
            print("\033[1;31m[ERROR]\033[0m Invalid choice, please try again.")

# =====================================================
# 8) Main loop
# =====================================================

def main():
    script_path = ask_script_path()

    # Start target script in child thread
    worker = threading.Thread(target=run_script_in_thread, args=(script_path,))
    worker.daemon = True  # Ensure child thread exits when main program exits
    worker.start()

    print(f"\033[1;34m[INFO]\033[0m Script started in child thread (thread_id = {worker.ident})")
    print("\033[1;34m[INFO]\033[0m Press Ctrl+C for normal interrupt, Ctrl+Shift+C for stack analysis")

    # Setup keyboard hook for Ctrl+Shift+C
    keyboard.add_hotkey('ctrl+shift+c', lambda: None)  # Just register the hotkey

    while True:
        try:
            while worker.is_alive():
                # Poll for 'ctrl+shift+c'
                if keyboard.is_pressed('ctrl+shift+c'):
                    # Open debug interrupt menu
                    if not handle_debug_interrupt(worker):
                        # If user chooses not to continue, break out of loop
                        break
                time.sleep(0.1)
            if not worker.is_alive():
                break
        except KeyboardInterrupt:
            # Just pass Ctrl+C to child thread and continue monitoring
            print("\n\033[1;33m[INFO]\033[0m Ctrl+C detected, passing to target script via KeyboardInterrupt...")
            kill_thread(worker, KeyboardInterrupt)
            continue

    keyboard.unhook_all()
    print("\033[1;34m[INFO]\033[0m Main script ended. Goodbye.")

if __name__ == "__main__":
    main()
