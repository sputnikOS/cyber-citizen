import psutil
import os

import gc

def clear_ram():
    """Force garbage collection to free up memory."""
    gc.collect()
    print("Garbage collection complete.")

def release_large_object(obj):
    """Delete a large object and clear memory."""
    del obj  # Remove the reference to the object
    gc.collect()  # Trigger garbage collection
    print("Large object cleared from memory.")

def memory_usage():
    """Check memory usage of the current process."""
    process = psutil.Process(os.getpid())
    mem = process.memory_info().rss / (1024 * 1024)  # Convert to MB
    print(process)
    print(f"Memory usage: {mem:.2f} MB")

# Example usage
memory_usage()
clear_ram()
