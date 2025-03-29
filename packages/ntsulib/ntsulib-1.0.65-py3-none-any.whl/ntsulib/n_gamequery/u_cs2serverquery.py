import concurrent
import enum
import inspect
import json
import re
import socket
import time
from itertools import islice
import a2s
import requests

class NtsuQueryError(Exception):
    def __init__(self, msg):
        self.msg = msg
        self.line_number = inspect.currentframe().f_back.f_lineno
        super().__init__(self.msg)
    def __str__(self):
        return f"{self.msg} (line {self.line_number})"

class query_type(enum.Enum):
    SteamAPI = 0
    A2S = 1

class ntsu_valveQuery:
    class server_info:
        def __init__(
                self,
                server_ip: str,
                server_port: int,
                server_name: str = None,
                server_onlineplayer_count: int = None,
                server_maxplayer_count: int = None,
                server_mapname: str = None,
                game: str = None,
                timeout: int = None,
                querystatus: bool = False
        ):
            self.server_ip = server_ip
            self.server_port = server_port
            self.server_name = server_name
            self.server_transname = None
            self.server_onlineplayer_count = server_onlineplayer_count
            self.server_maxplayer_count = server_maxplayer_count
            self.server_mapname = server_mapname
            self.game = game
            self.timeout = timeout
            self.querystatus = querystatus
            self.specmode = False
        def is_error(self):
            return not self.querystatus
        def __str__(self):
            return str(
                'ip: ' + self.server_ip +
                ' port: ' + str(self.server_port) +
                ' name: ' + (self.server_name if self.server_name else 'N/A') +
                ' transname: ' + (self.server_transname if self.server_transname else 'N/A') +
                ' onlineplayer_count: ' + (
                    str(self.server_onlineplayer_count) if self.server_onlineplayer_count is not None else 'N/A') +
                ' maxplayer_count: ' + (
                    str(self.server_maxplayer_count) if self.server_maxplayer_count is not None else 'N/A') +
                ' mapname: ' + (self.server_mapname if self.server_mapname else 'N/A') +
                ' game: ' + (self.game if self.game else 'N/A') +
                ' timeout: ' + (str(self.timeout) if self.timeout is not None else 'N/A') +
                ' specmode: ' + str(self.specmode) +
                ' querystatus: ' + str(self.querystatus)
            )
    def __init__(self, timeout:float, encoding:str, steamwebapikey:str):
        self.timeout = timeout
        self.encoding = encoding
        requests.adapters.DEFAULT_RETRIES = 2
        requests.packages.urllib3.disable_warnings()
        self.header = {'Connection': 'close'}
        self.session = requests.session()
        self.steamwebapikey = steamwebapikey
    # 用于解析域名
    def resolve_domain_to_ip(self, domain):
        # 分离域名和端口
        if ':' in domain:
            domain, port = domain.split(':')
        else:
            port = None
        # 获取域名的 IP 地址
        ip = socket.gethostbyname(domain)
        if port:
            return f"{ip}:{port}"
        else:
            return ip
    def _a2s_toServerInfoClass(self, response_string:str, specmode = False) -> server_info:
        ip_port_pattern = re.compile(r"Server: \('([^']*)', (\d+)\)")
        ip_port_match = ip_port_pattern.search(response_string)
        if ip_port_match:
            ip = ip_port_match.group(1)
            port = int(ip_port_match.group(2))
        else:
            raise NtsuQueryError('查询的字符串有误')
        try:
            server_name_pattern = re.compile(r"server_name='(.*?)'")
            player_count_pattern = re.compile(r"player_count=(\d+)")
            max_players_pattern = re.compile(r"max_players=(\d+)")
            map_name_pattern = re.compile(r"map_name='(.*?)'")
            ping_pattern = re.compile(r"ping=([\d\.]+)")
            game_pattern = re.compile(r"game='(.*?)'")
            server_name = server_name_pattern.search(response_string).group(1)
            server_onlineplayer_count = player_count_pattern.search(response_string).group(1)
            server_maxplayer_count = max_players_pattern.search(response_string).group(1)
            origin_mapname = map_name_pattern.search(response_string).group(1)
            if specmode is False:
                server_mapname = origin_mapname
            else:
                server_mapname = self._query_mapmame(origin_mapname,0.7)
            game = game_pattern.search(response_string).group(1)
            timeout = ping_pattern.search(response_string).group(1)
            serverinfo = self.server_info(ip,
                                          port,
                                          server_name,
                                          server_onlineplayer_count,
                                          server_maxplayer_count,
                                          server_mapname,
                                          game,
                                          timeout,
                                          querystatus=True)
            serverinfo.specmode = specmode
            return serverinfo
        except:
            error_serverinfo = self.server_info(ip,port)
            return error_serverinfo
    def _a2s_query_server(self, server_address):
        try:
            server_info = a2s.info(address=server_address, timeout=self.timeout, encoding=self.encoding)
            return f"Server: {server_address}, Info: {server_info}"
        except Exception as e:
            #return f"Server: {server_address}, Error: {e}"
            # 重试次数
            retrytimes = 1
            while retrytimes > 0:
                retrytimes = retrytimes -1
                try:
                    server_info = a2s.info(address=server_address, timeout=self.timeout, encoding=self.encoding)
                    return f"Server: {server_address}, Info: {server_info}"
                except:
                    if retrytimes == 0:
                        return f"Server: {server_address}, Error: {e}"
                    else:
                        continue

    #解析并处理steamapi查询的结果
    def _steam_toServerInfoClass(self, response_string:str) -> server_info:
        ip_port_pattern = re.compile(r"Server: \('([^']*)', (\d+)\)")
        ip_port_match = ip_port_pattern.search(response_string)
        if ip_port_match:
            ip = ip_port_match.group(1)
            port = int(ip_port_match.group(2))
        else:
            raise NtsuQueryError('查询的字符串有误')
        try:
            # 提取后半段json
            match = re.search(r"Info: ({.*})$", response_string)
            if match:
                json_str = match.group(1)
                # 使用 eval 将字符串转换为 Python 字典
                info_data = eval(json_str)
                s_info = info_data['response']['servers'][0]
                # 清单
                r_address = s_info['addr']
                r_gameport = s_info['gameport']
                r_steamid = s_info['steamid']
                r_name = s_info['name']
                r_appid = s_info['appid']
                r_gamedir = s_info['gamedir']
                r_version = s_info['version']
                r_product = s_info['product']
                r_region = s_info['region']
                r_players = s_info['players']
                r_max_players = s_info['max_players']
                r_bots = s_info['bots']
                r_map = s_info['map']
                r_secure = s_info['secure']
                r_dedicated = s_info['dedicated']
                r_os = s_info['os']
                r_gametype = s_info['gametype']
                # r_product与timeout 和a2s查询不一致 需要做区分
                #print(r_address,r_gameport,r_steamid,r_name,r_appid,r_gamedir,r_version,r_product,r_region,r_players,r_max_players,r_bots,r_map,r_secure,r_dedicated,r_os,r_gametype,sep = "\n")
                serverinfo = self.server_info(ip,
                                              port,
                                              r_name,
                                              r_players,
                                              r_max_players,
                                              r_map,
                                              r_product,
                                              0,
                                              querystatus=True)
                # print('查询: ', ip_address, ":", port, "成功")
                return serverinfo
            # 如果正则表达式匹配不到json 可能是服务器没开启 或者网络问题
            else:
                # print('[SteamWebAPI] 查询: ', ip, ":", port, "失败, 可能是网络问题或服务器未开启")
                raise NtsuQueryError(msg='查询失败,没有匹配到符合的json数据')
        # 无法查询 域名 检测正则表达式与域名的匹配
        except:
            error_serverinfo = self.server_info(server_ip=ip, server_port=port)
            return error_serverinfo

    # threshold 代表相似度 0.7 则70%相同
    # self.map_list 在主文件内定义
    def _query_mapmame(self, name: str, threshold: float) -> str:
        best_match = name  # 默认返回原字符串
        best_similarity = 0  # 记录最高相似度
        target_len = len(name)

        for map_name in self.map_list:
            if len(map_name) != target_len:
                continue  # 长度不同，跳过

            # 计算匹配字符数量
            match_count = sum(1 for a, b in zip(map_name, name) if a == b)
            similarity = match_count / target_len  # 计算匹配度

            # 如果匹配度符合要求，且比当前最佳匹配更高，则更新
            if similarity >= threshold and similarity > best_similarity:
                best_match = map_name
                best_similarity = similarity

        return best_match  # 返回相似度最高的地图名（或原字符串）

    # 使用steamapi查询 并返回网页结果
    def _steam_query_server(self, server_address) -> str:
        u_ip = self.resolve_domain_to_ip(server_address[0])

        url = (
               f"https://api.steampowered.com/IGameServersService/GetServerList/v1/?"
               f"key={self.steamwebapikey}"
               f"&filter=\\appid\\730\\gameaddr\\{u_ip}:{server_address[1]}\\&limit=1"
        )

        try:
            req = self.session.get(url, headers=self.header, verify=False, timeout=5)
            req.close()
            datas = json.loads(req.text)
            return f"Server: {server_address}, Info: {datas}"
        except Exception as e:
            return f"Server: {server_address}, Error: {e}"

    def query_servers(self, addresses: list, q_type: query_type, specmode=False) -> list:
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:  # 限制并发数
            if q_type == query_type.SteamAPI:  # 0
                result = []
                for chunk in self._chunked_iterable(addresses, 2):  # 每次查询 2 个服务器
                    futures = {executor.submit(self._steam_query_server, address): address for address in chunk}
                    for future in concurrent.futures.as_completed(futures):
                        time.sleep(0.1)
                        result.append(self._steam_toServerInfoClass(future.result()))
                return result

            elif q_type == query_type.A2S and not specmode:  # 1
                result = []
                for chunk in self._chunked_iterable(addresses, 2):  # 每次查询 2 个服务器
                    futures = {executor.submit(self._a2s_query_server, address): address for address in chunk}
                    for future in concurrent.futures.as_completed(futures):
                        time.sleep(0.1)
                        result.append(self._a2s_toServerInfoClass(future.result()))
                return result

            elif q_type == query_type.A2S and specmode:  # 2
                # fys特殊匹配模式
                result = []
                for chunk in self._chunked_iterable(addresses, 2):  # 每次查询 2 个服务器
                    futures = {executor.submit(self._a2s_query_server, address): address for address in chunk}

                    for future in concurrent.futures.as_completed(futures):
                        time.sleep(0.1)
                        result.append(self._a2s_toServerInfoClass(future.result(), specmode=True))

                return result

            else:
                raise NtsuQueryError('query_type 传入错误')

    def _chunked_iterable(self, iterable, size):
        """ 将地址列表分块，每次返回 size 个  """
        it = iter(iterable)
        chunk = list(islice(it, size))
        while chunk:  # 只要 chunk 不为空，就继续迭代
            yield chunk
            chunk = list(islice(it, size))  # 继续获取下一组