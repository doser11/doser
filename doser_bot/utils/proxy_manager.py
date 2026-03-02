"""
Proxy Manager - Handle proxy rotation and validation
"""

import random
import requests
import socket
import socks
from typing import Optional, Dict, List
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class ProxyManager:
    """Manage and rotate proxies for Instagram account creation"""
    
    def __init__(self, proxy_file: Optional[str] = None):
        self.proxies: List[Dict] = []
        self.current_index = 0
        self.proxy_file = proxy_file
        self._load_proxies()
    
    def _load_proxies(self):
        """Load proxies from file or use default list"""
        if self.proxy_file and Path(self.proxy_file).exists():
            with open(self.proxy_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        self._parse_proxy(line)
        else:
            # Default empty list - user should add proxies
            logger.warning("No proxy file provided. Using direct connection.")
    
    def _parse_proxy(self, proxy_str: str):
        """Parse proxy string in format: type://user:pass@ip:port"""
        try:
            # Format: http://user:pass@ip:port or socks5://ip:port
            if '://' in proxy_str:
                proxy_type, rest = proxy_str.split('://', 1)
            else:
                proxy_type = 'http'
                rest = proxy_str
            
            if '@' in rest:
                auth, endpoint = rest.split('@', 1)
                username, password = auth.split(':', 1)
            else:
                endpoint = rest
                username = password = None
            
            ip, port = endpoint.split(':', 1)
            
            proxy_dict = {
                'type': proxy_type.lower(),
                'host': ip,
                'port': int(port),
                'username': username,
                'password': password,
                'url': proxy_str
            }
            self.proxies.append(proxy_dict)
            logger.info(f"Loaded proxy: {ip}:{port}")
            
        except Exception as e:
            logger.error(f"Failed to parse proxy '{proxy_str}': {e}")
    
    def get_next_proxy(self) -> Optional[Dict]:
        """Get next proxy in rotation"""
        if not self.proxies:
            return None
        
        proxy = self.proxies[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.proxies)
        return proxy
    
    def get_random_proxy(self) -> Optional[Dict]:
        """Get random proxy from list"""
        if not self.proxies:
            return None
        return random.choice(self.proxies)
    
    def test_proxy(self, proxy: Dict) -> bool:
        """Test if proxy is working"""
        try:
            proxy_url = proxy['url']
            proxies = {
                'http': proxy_url,
                'https': proxy_url
            }
            
            response = requests.get(
                'https://httpbin.org/ip',
                proxies=proxies,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"Proxy working. IP: {data.get('origin')}")
                return True
            return False
            
        except Exception as e:
            logger.error(f"Proxy test failed: {e}")
            return False
    
    def get_selenium_proxy(self, proxy: Dict) -> Dict:
        """Get proxy configuration for Selenium"""
        if not proxy:
            return {}
        
        proxy_type = proxy['type']
        host = proxy['host']
        port = proxy['port']
        
        selenium_proxy = {
            'proxyType': 'MANUAL',
        }
        
        if proxy_type in ['http', 'https']:
            selenium_proxy['httpProxy'] = f"{host}:{port}"
            selenium_proxy['sslProxy'] = f"{host}:{port}"
        elif proxy_type == 'socks4':
            selenium_proxy['socksProxy'] = f"{host}:{port}"
            selenium_proxy['socksVersion'] = 4
        elif proxy_type == 'socks5':
            selenium_proxy['socksProxy'] = f"{host}:{port}"
            selenium_proxy['socksVersion'] = 5
        
        if proxy.get('username') and proxy.get('password'):
            selenium_proxy['socksUsername'] = proxy['username']
            selenium_proxy['socksPassword'] = proxy['password']
        
        return selenium_proxy
    
    def apply_proxy_to_socket(self, proxy: Dict):
        """Apply SOCKS proxy to socket for requests"""
        if proxy and proxy['type'] in ['socks4', 'socks5']:
            sock_type = socks.SOCKS5 if proxy['type'] == 'socks5' else socks.SOCKS4
            socks.set_default_proxy(
                sock_type,
                proxy['host'],
                proxy['port'],
                username=proxy.get('username'),
                password=proxy.get('password')
            )
            socket.socket = socks.socksocket
    
    def get_proxy_count(self) -> int:
        """Get total number of loaded proxies"""
        return len(self.proxies)
    
    def add_proxy(self, proxy_str: str):
        """Add a new proxy to the list"""
        self._parse_proxy(proxy_str)
    
    def remove_proxy(self, index: int):
        """Remove proxy at index"""
        if 0 <= index < len(self.proxies):
            removed = self.proxies.pop(index)
            logger.info(f"Removed proxy: {removed['host']}:{removed['port']}")
