import socket
import struct
import time

def traceroute(host, port=33434, max_hops=30):
    ttl = 1
    while ttl <= max_hops:
        # 用于发送UDP包的套接字
        send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.getprotobyname('udp'))
        send_socket.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl)

        # 创建原始套接字，用于接收ICMP包，在Windows上协议类型使用socket.IPPROTO_IP
        recv_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
        recv_socket.settimeout(3.0)

        target_ip = socket.gethostbyname(host)

        # 发送UDP包
        send_socket.sendto(b'', (target_ip, port))

        # 关闭发送套接字
        send_socket.close()

        # 等待ICMP响应
        try:
            data, curr_addr = recv_socket.recvfrom(512)
            curr_addr = curr_addr[0]
            print(f"Hop {ttl}: {curr_addr}")
        except socket.error:
            print(f"Hop {ttl}: *")
        finally:
            recv_socket.close()

        ttl += 1

if __name__ == '__main__':

    # 使用示例
    traceroute("www.baidu.com")