import xml.etree.ElementTree as ET
import requests
from requests.exceptions import RequestException

def parse_nmap_xml(xml_string):
    """解析nmap XML输出"""
    try:
        root = ET.fromstring(xml_string)
        results = []
        
        for host in root.findall('host'):
            for port in host.findall('ports/port'):
                service = port.find('service')
                result = {
                    'port': int(port.get('portid')),
                    'protocol': port.get('protocol'),
                    'state': port.find('state').get('state'),
                    'name': service.get('name') if service is not None else 'unknown',
                    'product': service.get('product') if service is not None else '',
                    'version': service.get('version') if service is not None else ''
                }
                results.append(result)
        
        return results
    except Exception as e:
        print(f"解析nmap XML失败: {e}")
        return []

def get_http_title(url, port, is_https=False):
    """获取HTTP/HTTPS标题"""
    try:
        scheme = 'https' if is_https else 'http'
        full_url = f"{scheme}://{url}:{port}"
        response = requests.get(full_url, timeout=5, verify=False)
        if response.status_code == 200:
            # 从HTML中提取<title>标签内容
            start = response.text.find('<title>')
            end = response.text.find('</title>')
            if start != -1 and end != -1:
                return response.text[start+7:end]
        return None
    except RequestException as e:
        print(f"获取HTTP标题失败: {e}")
        return None
    except Exception as e:
        print(f"未知错误: {e}")
        return None
