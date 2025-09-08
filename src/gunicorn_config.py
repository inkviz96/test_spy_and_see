import multiprocessing

bind = "0.0.0.0:80"
worker_class = "uvicorn.workers.UvicornWorker"

#######################################################
# Change only loglevel                                #
#######################################################
accesslog = "-"
errorlog = "-"
loglevel = "info"
capture_output = True
enable_stdio_inheritance = True

#######################################################
#######################################################
# Don't touch. This important for prevent DDOS attack #
#######################################################
limit_request_line = 4094
limit_request_fields = 200
limit_request_field_size = 8190
secure_scheme_headers = {
    "X-FORWARDED-PROTO": "https",
}
forwarded_allow_ips = "*"

timeout = 600
#######################################################
max_requests = 15000
max_requests_jitter = 3
workers = multiprocessing.cpu_count() * 2 + 1

cores = multiprocessing.cpu_count()
workers_per_core = float(2)
default_web_concurrency = workers_per_core * cores
use_max_workers = 15
web_concurrency = 5
