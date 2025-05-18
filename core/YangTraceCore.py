from scapy.all import *
from scapy.layers.inet import IP, ICMP
from core.iptoaddress import get_location
import time
import socket

def get_address(target_ip, ttl):
    pkt = IP(dst = target_ip, ttl = ttl) / ICMP()
    send_time = time.time()
    reply = sr1(pkt, verbose=0, timeout=2)
    if reply is None:
        result_list = [ttl, '*', '*', '*', '*', '*', '*']
    else:
        # 计算往返时间
        recv_time = time.time()
        elapsed_time = (recv_time - send_time) * 1000  # 转换为毫秒
        curr_addr = reply.src
        trace_object = get_location(curr_addr)
        # 尝试解析域名
        try:
            hostname = socket.gethostbyaddr(curr_addr)[0]
        except socket.herror:
            hostname = "未知"
        result_list = [ttl, curr_addr, round(elapsed_time, 3), trace_object.Nation + ' ' + trace_object.City, trace_object.Company]
        # 如果匹配了目标IP，结束追踪
    return result_list

def get_address_ceshi(target, max_ttl = 30):
    try:
        target_ip = socket.gethostbyname(target)
    except socket.gaierror:
        print(f"Could not resolve {target}")
        return
    for ttl in range(1, max_ttl + 1):
        result = get_address(target_ip, ttl)
        print(result)
        if result[1] == target_ip:
            break

if __name__ == '__main__':
    get_address_ceshi('www.baidu.com')


def traceroute(target, max_ttl=30):
    """实现路由追踪"""
    try:
        target_ip = socket.gethostbyname(target)
    except socket.gaierror:
        print(f"Could not resolve {target}")
        return

    the_result = []

    print(f"Traceroute to {target} ({target_ip}), {max_ttl} hops max")
    print(f"TTL\tIpAddress\tHostName\tNation\tCity\tCompany\tTime")

    for ttl in range(1, max_ttl + 1):
        # 发送的 IP 数据包
        pkt = IP(dst=target_ip, ttl=ttl)/ICMP()

        # 发送数据包并开始计时
        send_time = time.time()
        reply = sr1(pkt, verbose=0, timeout=2)

        if reply is None:
            print(f"{ttl}\t*\t*\t*\t*\t*\t*")

        else:
            # 计算往返时间
            recv_time = time.time()
            elapsed_time = (recv_time - send_time) * 1000  # 转换为毫秒

            curr_addr = reply.src
            trace_object = get_location(curr_addr)
            # 尝试解析域名
            try:
                hostname = socket.gethostbyaddr(curr_addr)[0]
            except socket.herror:
                hostname = "未知"
            print(f"{ttl}\t{curr_addr}\t{hostname}\t\t{trace_object.Nation}\t{trace_object.City}\t{trace_object.Company}\t{elapsed_time:.2f} ms")

            # 如果匹配了目标IP，结束追踪
            if curr_addr == target_ip:
                print(f"Arrive at\t{target} ({target_ip})")
                break

    return the_result
