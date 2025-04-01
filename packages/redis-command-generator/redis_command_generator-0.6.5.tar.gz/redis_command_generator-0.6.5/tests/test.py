import redis_command_generator as cg

gen_runner = cg.GenRunner(hosts=("192.168.122.190:6379",), max_cmd_cnt=100000, pipe_every_x=1000, distributions='{"tsadd": 100, "tsrem": 0, "delete": 0}', verbose=True)
gen_runner.start()
gen_runner.join()