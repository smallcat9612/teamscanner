from app.models import Task, Target, Result, db
from app.utils.scanner import parse_nmap_xml, get_http_title
from app.utils.bruteforce import BruteForcer
import subprocess

class Scanner:
    @staticmethod
    def scan_ports(target):
        """使用nmap扫描目标端口"""
        try:
            cmd = f"nmap -p 1-65535 -T4 -A -v -oX - {target.url}"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            return result.stdout
        except Exception as e:
            print(f"端口扫描失败: {e}")
            return None

    @staticmethod
    def parse_nmap_result(xml_output):
        """解析nmap XML输出"""
        return parse_nmap_xml(xml_output)

    @staticmethod
    def check_http_service(ip, port):
        """检查HTTP/HTTPS服务并获取标题"""
        # 先尝试HTTPS
        title = get_http_title(ip, port, is_https=True)
        if title is None:
            # 如果HTTPS失败，尝试HTTP
            title = get_http_title(ip, port, is_https=False)
        return title

    @staticmethod
    def brute_force(ip, port, service):
        """弱口令爆破"""
        result = BruteForcer.brute_force(ip, port, service)
        return result is not None  # 返回是否爆破成功

def process_task(task_id):
    """处理扫描任务"""
    task = Task.query.get(task_id)
    if not task:
        return
        
    task.status = 'running'
    db.session.commit()
    
    targets = Target.query.filter_by(task_id=task_id).all()
    for target in targets:
        try:
            # 1. 端口扫描
            nmap_result = Scanner.scan_ports(target)
            if not nmap_result:
                continue
                
            # 2. 解析结果并保存
            services = Scanner.parse_nmap_result(nmap_result)
            for service in services:
                result = Result(
                    target_id=target.id,
                    port=service['port'],
                    service=service['name'],
                    protocol=service['protocol']
                )
                
                # 3. 处理HTTP/HTTPS服务
                if service['protocol'] in ['http', 'https']:
                    title = Scanner.check_http_service(target.url, service['port'])
                    result.title = title
                
                # 4. 其他服务弱口令爆破
                else:
                    is_vulnerable = Scanner.brute_force(target.url, service['port'], service['name'])
                    result.is_vulnerable = is_vulnerable
                
                db.session.add(result)
            
            target.status = 'completed'
            db.session.commit()
            
        except Exception as e:
            target.status = 'failed'
            db.session.commit()
            continue
    
    task.status = 'completed'
    db.session.commit()
