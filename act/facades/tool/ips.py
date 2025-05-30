import socket
import string

from act.facades.Logx.Logx import logx


def get_host_ip(host:string):
    try:
        # 解析主机名
        ip = socket.gethostbyname(host)
        return ip
    except socket.gaierror:
        try:
            # 备选方案：获取默认网关作为宿主机 IP
            import subprocess
            result = subprocess.run(
                ["ip", "route", "show", "default"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                return result.stdout.split()[2]
            return None
        except Exception as e:
            logx.warning(f"获取默认网关失败: {e}")

    return "127.0.0.1"

if __name__ == "__main__":
    host_ip = get_host_ip("host.docker.internal")
    if host_ip:
        print(f"宿主机 IP: {host_ip}")
    else:
        print("无法解析 host.docker.internal")