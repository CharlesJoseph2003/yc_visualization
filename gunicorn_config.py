"""
Gunicorn configuration file for the YC Visualization application.
"""
import multiprocessing

# Binding
bind = "0.0.0.0:8050"  # Same port as in app.py for consistency

# Worker processes
workers = 1  # Recommended formula for worker processes
worker_class = "gevent"  # Use gevent for better async handling with Dash
worker_connections = 1  # Maximum number of simultaneous clients

# Timeout
timeout = 120  # Seconds before a worker is killed and restarted

# Server mechanics
daemon = False  # Don't daemonize the main process
pidfile = "gunicorn.pid"  # File to store the process ID
user = None  # User to run as
group = None  # Group to run as
umask = 0  # File mode creation mask
tmp_upload_dir = None  # Directory to store temporary uploads

# Logging
errorlog = "-"  # Standard error output
accesslog = "-"  # Standard output
loglevel = "info"  # Log level

# Process naming
proc_name = "yc_visualization"  # Process name

# Server hooks
def on_starting(server):
    """
    Called just before the master process is initialized.
    """
    pass

def on_exit(server):
    """
    Called just before exiting.
    """
    pass
