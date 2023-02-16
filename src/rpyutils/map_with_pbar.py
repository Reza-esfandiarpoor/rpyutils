import multiprocessing as mp
import time

from tqdm import tqdm as local_tqdm


def init_pool_processes(shared_value):
    global g_counter
    g_counter = shared_value


def pbar(total, counter_var):
    prev = 0
    pbar = local_tqdm(total=total)
    while True:
        new = counter_var.value
        pbar.update(new - prev)
        prev = new
        if prev == total:
            break
        time.sleep(0.5)
    pbar.close()


def worker(args):

    func, func_args = args

    if isinstance(func_args, dict):
        output = func(**func_args)
    else:
        output = func(*func_args)

    with g_counter.get_lock():
        g_counter.value += 1

    return output


def map_tqdm(func, args, pool_size=8):

    shared_counter = mp.Value("q", 0)

    args_with_func = [(func, arg_) for arg_ in args]

    p = mp.Process(target=pbar, args=(len(args_with_func), shared_counter))
    p.daemon = True
    p.start()

    with mp.Pool(
        processes=pool_size, initializer=init_pool_processes, initargs=(shared_counter,)
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
#     o = mp_map_tqdm(test_func, arg_list, pool_size=8)
#     print(len(o))
