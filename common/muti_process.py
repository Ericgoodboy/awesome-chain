import time
from concurrent.futures import ThreadPoolExecutor

import tqdm


def handel_process_list(data):
    run = 0
    all_count = len(data)
    with tqdm.tqdm(total=all_count, desc="处理进度") as pbar:
        while run < all_count:
            time.sleep(0.1)
            current_done = 0
            for i in data:
                if i.done():
                    current_done += 1
            if current_done != run:
                pbar.update(current_done - run)
                run = current_done


def issue_thread_task(func, args_list: list[tuple], max_workers=10):
    with ThreadPoolExecutor(max_workers=max_workers) as e:
        data = []
        for args in args_list:
            try:
                data.append(e.submit(func, *args))
            except Exception as ex:
                pass
        handel_process_list(data)
        return data
