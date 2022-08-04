import itertools
import json
import main
import time
import pandas as pd

static_json = {
    "tehhhhnhhhhhhst": "thheshhhhhhhhhhhhhhhhhhhhhhhhhhhhhhs"}

def runtime():
    blockchain = main.BlockchainDatabase()
    q = [''.join(p) for p in itertools.permutations('qwertyuiopasdfghjklzx', 4)]

    for i in q:
        main.append_method(i, static_json, main.privKey, blockchain)

    df = pd.DataFrame(main.time_arr, columns=['Append Time'])
    df.to_csv("append_time.csv", mode='a')

    print("a")

    for i in q:
        a = main.query_method(i, main.privKey, blockchain)

    df = pd.DataFrame(main.timeq_arr, columns=['Append Time'])
    df.to_csv("query_time.csv", mode='a')

    print("q")

    for i in q:
        main.update_method(i, static_json, main.privKey, blockchain)

    df = pd.DataFrame(main.timeu_arr, columns=['Append Time'])
    df.to_csv("update_time.csv", mode='a')

    print("u")

    for i in q:
        main.delete_method(i, blockchain)

    df = pd.DataFrame(main.timed_arr, columns=['Append Time'])
    df.to_csv("delete_time.csv", mode='a')

    print("d")


def throughput():
    blockchain = main.BlockchainDatabase()
    throughput_q = []
    throughput_a = []
    throughput_u = []
    throughput_d = []

    q = [''.join(p) for p in itertools.permutations('qwertyuiopasdfghjklzx', 4)]
    st = time.time()
    count = 0
    for i in q:
        main.append_method(i, static_json, main.privKey, blockchain)
        count += 1
        et = time.time()
        if et-st >= 1:
            throughput_a.append(count)
            count = 0
            st = time.time()
    throughput_a.append(count)
    df = pd.DataFrame(throughput_a, columns=['Number of operations'])
    df.to_csv("append_throughput.csv", mode='a')

    print("a")

    st = time.time()
    count = 0

    for i in q:
        a = main.query_method(i, main.privKey, blockchain)
        count += 1
        et = time.time()
        if et - st >= 1:
            throughput_q.append(count)
            count = 0
            st = time.time()
    throughput_q.append(count)
    df = pd.DataFrame(throughput_q, columns=['Number of operations'])
    df.to_csv("query_throughput.csv", mode='a')

    print("q")

    st = time.time()
    count = 0

    for i in q:
        main.update_method(i, static_json, main.privKey, blockchain)
        count += 1
        et = time.time()
        if et - st >= 1:
            throughput_u.append(count)
            count = 0
            st = time.time()
    throughput_u.append(count)
    df = pd.DataFrame(throughput_u, columns=['Number of operations'])
    df.to_csv("update_throughput.csv", mode='a')

    print("u")
    st = time.time()
    count = 0
    for i in q:
        main.delete_method(i, blockchain)
        count += 1
        et = time.time()
        if et - st >= 1:
            throughput_d.append(count)
            count = 0
            st = time.time()
    throughput_d.append(count)
    df = pd.DataFrame(throughput_d, columns=['Number of operations'])
    df.to_csv("delete_throughput.csv", mode='a')

    print("d")
