import multiprocessing
import sys,os 

PARENT_PATH=os.path.dirname( os.path.dirname(__file__) )

sys.path.append(PARENT_PATH)

from planting.settings import BIND_ADDR

bind=BIND_ADDR

workers=multiprocessing.cpu_count()*2+1
worker_class='eventlet'
backlog=1024
max_requests=1024
time_out=90
limit_request_line=1024
limit_request_fields=64
