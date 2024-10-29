import multiprocessing

# Binding
bind = "0.0.0.0:8000"

# Worker Processes
workers = 3  # Simpler than multiprocessing calculation for stability
worker_class = 'sync'
worker_connections = 1000

# Timeout
timeout = 120  # Increased timeout for better stability
keepalive = 5

# Logging
accesslog = "logs/gunicorn-access.log"
errorlog = "logs/gunicorn-error.log"
loglevel = "debug"  # Set to debug to see more information

# Performance Tuning
max_requests = 1000
max_requests_jitter = 50
graceful_timeout = 30
forwarded_allow_ips = '*'

# SSL Configuration (if you're handling SSL at this level)
# keyfile = "/path/to/keyfile"
# certfile = "/path/to/certfile"

# Process Naming
proc_name = 'cryptomock-api'

# Security
limit_request_line = 4096
limit_request_fields = 100
limit_request_field_size = 8190