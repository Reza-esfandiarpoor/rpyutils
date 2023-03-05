import multiprocessing as mp
import os
import time

from tqdm import tqdm as local_tqdm


def init_pool_processes(args):
    global counter_list
    global counter_index
    counter_list = args["counter_list"]
    counter_index = args["index_queue"].get()


def pbar(total, counter_var_list, update_interval=0.5):
    prev = 0
    pbar = local_tqdm(total=total)
    while True:
        new = 0
        for counter_var in counter_var_list:
            counter_value = counter_var.value
            new += counter_value
        pbar.update(new - prev)
        prev = new
        if prev >= total:
            break
        time.sleep(update_interval)
    pbar.close()


def worker(args):
    func = args["func"]
    func_args = args["args"]

    if isinstance(func_args, dict):
        output = func(**func_args)
    else:
        output = func(*func_args)

    with counter_list[counter_index].get_lock():
        counter_list[counter_index].value += 1

    return output


def map_tqdm(func, args, pool_size=None, update_interval=0.5):
    if pool_size is None:
        pool_size = os.cpu_count()

    shared_counter_list = [mp.Value("q", 0) for _ in range(pool_size)]

    init_queue = mp.Queue()
    for sc in range(pool_size):
        init_queue.put(sc)

    args_with_func = [{"func": func, "args": arg_} for arg_ in args]

    p = mp.Process(
        target=pbar, args=(len(args_with_func), shared_counter_list, update_interval)
    )
    p.daemon = True
    p.start()

    with mp.Pool(
        processes=pool_size,
        initializer=init_pool_processes,
        initargs=({"index_queue": init_queue, "counter_list": shared_counter_list},),
    ) as pool:
        out_list = pool.map(worker, args_with_func)

    p.join()

    return out_list


# def test_func(arg):
#     time.sleep(0.5)
#     return arg
#
#
# if __name__ == "__main__":
#
#     arg_list = [(1,) for _ in range(80)]
#     o = map_tqdm(test_func, arg_list, pool_size=8)
#     print(len(o))
#
