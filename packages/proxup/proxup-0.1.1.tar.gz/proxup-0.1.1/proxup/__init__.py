try: 
    import amdl
except ImportError: 
    __import__('subprocess').check_call([__import__('sys').executable, "-m", "pip", "install", "amdl", "--break-system-packages"]); import amdl

amdl.add([
    'os',
    're',
    'random',
    'threading',
    'requests'
])

class __proxup__:
    project_root = os.path.dirname(os.path.abspath(__file__))
    proxies_dir = os.path.join(project_root, '..', 'proxies')

    os.makedirs(proxies_dir, exist_ok=True)

    proxies_file = os.path.join(proxies_dir, 'proxup-proxies.txt')

    if not os.path.exists(proxies_file):
        with open(proxies_file, 'w'):
            pass

def FetchProxies(url, custom_regex, proxieslog, lock):
    try:
        proxylist = requests.get(url, timeout=5).text
    except Exception:
        pass
    else:
        proxylist = proxylist.replace("null", "")
        custom_regex = custom_regex.replace("%ip%", "([0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3})")
        custom_regex = custom_regex.replace("%port%", "([0-9]{1,5})")
        new_proxies = [f"{proxy[0]}:{proxy[1]}" for proxy in re.findall(re.compile(custom_regex), proxylist)]

        with lock:
            proxieslog.extend(new_proxies)

def GetProxies():
    proxieslog = []
    lock = threading.Lock()

    proxysources = [
        ["http://spys.me/proxy.txt", "%ip%:%port% "],
        ["http://www.httptunnel.ge/ProxyListForFree.aspx", ' target="_new">%ip%:%port%</a>'],
        ["https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.json", '"ip":"%ip%","port":"%port%",'],
        ["https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list", '"host": "%ip%".*?"country": "(.*?){2}",.*?"port": %port%'],
        ["https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list.txt", "%ip%:%port% (.*?){2}-.-S \\+"],
        ["https://raw.githubusercontent.com/opsxcq/proxy-list/master/list.txt", '%ip%", "type": "http", "port": %port%'],
        ["https://www.sslproxies.org/", "<tr><td>%ip%<\\/td><td>%port%<\\/td><td>(.*?){2}<\\/td><td class='hm'>.*?<\\/td><td>.*?<\\/td><td class='hm'>.*?<\\/td><td class='hx'>(.*?)<\\/td><td class='hm'>.*?<\\/td><\\/tr>"],
        ["https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=6000&country=all&ssl=yes&anonymity=all", "%ip%:%port%"],
        ["https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt", "%ip%:%port%"],
        ["https://raw.githubusercontent.com/shiftytr/proxy-list/master/proxy.txt", "%ip%:%port%"],
        ["https://proxylist.icu/proxy/", "<td>%ip%:%port%</td><td>http<"],
        ["https://proxylist.icu/proxy/1", "<td>%ip%:%port%</td><td>http<"],
        ["https://proxylist.icu/proxy/2", "<td>%ip%:%port%</td><td>http<"],
        ["https://proxylist.icu/proxy/3", "<td>%ip%:%port%</td><td>http<"],
        ["https://proxylist.icu/proxy/4", "<td>%ip%:%port%</td><td>http<"],
        ["https://proxylist.icu/proxy/5", "<td>%ip%:%port%</td><td>http<"],
        ["https://www.hide-my-ip.com/proxylist.shtml", '"i":"%ip%","p":"%port%",'],
        ["https://raw.githubusercontent.com/scidam/proxy-list/master/proxy.json", '"ip": "%ip%",\n.*?"port": "%port%",'],
    ]


    threads = []

    for url, custom_regex in proxysources:
        t = threading.Thread(target=FetchProxies, args=(url, custom_regex, proxieslog, lock))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    proxies = list(set(proxieslog))

    with open(__proxup__.proxies_file, "w") as f:
        for proxy in proxies:
            for _ in range(random.randint(7, 10)):
                f.write(f"{proxy}\n")

def GetProxy():
    file = __proxup__.proxies_file

    if os.stat(file).st_size == 0:
        GetProxies()

    proxies = open(file).read().split("\n")
    proxy = proxies[0]

    with open(file, "r+") as fp:
        lines = fp.readlines()
        fp.seek(0)
        fp.truncate()
        fp.writelines(lines[1:])

    return {"http://": f"http://{proxy}", "https://": f"https://{proxy}"}