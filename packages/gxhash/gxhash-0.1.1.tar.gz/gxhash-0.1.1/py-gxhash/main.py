import asyncio
from asyncio import gather, get_running_loop, run, wrap_future
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
from pathlib import Path
from tempfile import TemporaryFile
from time import perf_counter_ns

from gxhash import GxHash32, GxHash64, GxHash128


class Global:
    collected = 0
    begin = False
    end = False


async def collect():
    while True:
        if Global.begin:
            Global.collected += 1

        elif Global.end:
            break

        await asyncio.sleep(0.1)


"""
bytes method
566.181921 ms
Total time: 2595.227745 ms
Global.collected=6

file method
964.431177 ms
Total time: 964.486867 ms
Global.collected=10

tempfile method
634.271684 ms
Total time: 2517.245562 ms
collected=7
"""


# async def gxhash():
#     thread_pool = ThreadPoolExecutor()
#     loop = get_running_loop()
#     load_time = perf_counter_ns()

#     with Path("gentoo_root.img").open("rb") as img:
#         file = img.read()
#         print("Hello, world!")

#         Global.begin = True
#         start = perf_counter_ns()
#         # result = await loop.run_in_executor(None, gxhash128_nogil, file, 1234)
#         result = await wrap_future(
#             thread_pool.submit(gxhash128_test, file, 1234), loop=loop
#         )
#         # result = await gxhash128_async(img, 1234)
#         print(f"{(perf_counter_ns() - start) / 1_000_000} ms")
#         Global.end = True

#     print(f"Total time: {(perf_counter_ns() - load_time) / 1_000_000} ms")
#     print(f"{result=}")
#     print(f"{Global.collected=}")


# async def gxhash():
#     with Path("gentoo_root.img").open("rb") as img:
#         print("Hello, world!")

#         load_time = perf_counter_ns()
#         # tfile = TemporaryFile()
#         # tfile.write(file)
#         # tfile.seek(0)
#         Global.begin = True
#         start = perf_counter_ns()
#         result = await gxhash128_async(img, 1234)
#         print(f"{(perf_counter_ns() - start) / 1_000_000} ms")
#         Global.end = True

#     print(f"Total time: {(perf_counter_ns() - load_time) / 1_000_000} ms")
#     print(f"{result=}")
#     print(f"{Global.collected=}")


async def main():
    try:
        input_bytes = bytes([42] * 10000000)
        seed = 1234
        file = TemporaryFile()
        event_loop = get_running_loop()
        file.write(input_bytes)
        file.seek(0)
        gxhash128 = GxHash128(seed=seed)

        start = perf_counter_ns()
        thread_pool = ThreadPoolExecutor()
        futures = [gxhash128.hash(input_bytes) for _ in range(1)]
        print(f"{(perf_counter_ns() - start) / 1_000_000} ms")

        tempfiles = [TemporaryFile() for _ in range(1)]
        for tfile in tempfiles:
            tfile.write(input_bytes)
            tfile.seek(0)

        start = perf_counter_ns()
        hash128_async = [gxhash128.hash_file(tfile) for tfile in tempfiles]
        print(f"{(perf_counter_ns() - start) / 1_000_000} ms")

        # await asyncio.gather(gxhash(), collect())

    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    run(main())


async def main():
    seed = 1234
    input_bytes = bytes([42] * 1000)
    file = TemporaryFile()
    file.write(input_bytes)
    file.seek(0)
    gxhash32 = GxHash32(seed=seed)
    gxhash64 = GxHash64(seed=seed)
    gxhash128 = GxHash128(seed=seed)

    hash32 = gxhash32.hash(input_bytes)
    hash32_nogil = gxhash32.hash_nogil(input_bytes)
    hash32_file = gxhash32.hash_file(file)
    file.seek(0)
    hash32_file_async = await gxhash32.hash_file_async(file)
    assert hash32 == hash32_nogil == hash32_file == hash32_file_async

    hash64 = gxhash64.hash(input_bytes)
    hash64_nogil = gxhash64.hash_nogil(input_bytes)
    hash64_file = gxhash64.hash_file(file)
    file.seek(0)
    hash64_file_async = await gxhash64.hash_file_async(file)
    assert hash64 == hash64_nogil == hash64_file == hash64_file_async

    hash128 = gxhash128.hash(input_bytes)
    hash128_nogil = gxhash128.hash_nogil(input_bytes)
    hash128_file = gxhash128.hash_file(file)
    file.seek(0)
    hash128_file_async = await gxhash128.hash_file_async(file)
    assert hash128 == hash128_nogil == hash128_file == hash128_file_async
