from colorama import Fore, Style, init
import os
import requests
import socket
import re

init(autoreset=True)

def display_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.BLUE + Style.BRIGHT + r"""
 _____         _                       _   _  _     ______
|  __ \       | |                     | | | || |    | ___ \
| |  \/  __ _ | |  __ _ __  __ _   _  | | | || |    | |_/ /
| | __  / _` || | / _` |\ \/ /| | | | | | | || |    |  __/
| |_\ \| (_| || || (_| | >  < | |_| | | |_| || |____| |
 \____/ \__,_||_| \__,_|/_/\_\ \__, |  \___/ \_____/\_|
                                __/ |
                               |___/
""" + Style.RESET_ALL)
    print(Fore.MAGENTA + Style.BRIGHT + "               Developer: GalaxyCloud")
    print(Fore.CYAN + Style.BRIGHT + "         Welcome to GalaxyCloud Tool v1.5\n" + Style.RESET_ALL)

def read_file_with_fallback(file_name="list.txt"):
    if not os.path.isfile(file_name):
        print(Fore.RED + f"[!] Không tìm thấy file '{file_name}'")
        return None
    with open(file_name, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

# Chức năng 1
def tim_dong_chua_tu_khoa(file_name="list.txt", keyword="admin"):
    lines = read_file_with_fallback(file_name)
    if lines is None: return
    result = [line for line in lines if keyword.lower() in line.lower()]
    with open("Ket_qua_tim_kiem.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(result))
    for line in result:
        print(Fore.YELLOW + "[MATCH] " + line)
    print(Fore.CYAN + f"[+] Đã lưu {len(result)} dòng chứa từ khóa vào 'Ket_qua_tim_kiem.txt'")

# Chức năng 2
def loc_bo_dong_admin(file_name="list.txt"):
    lines = read_file_with_fallback(file_name)
    if lines is None: return
    filtered = []
    for line in lines:
        if any(x in line.lower() for x in ["#admin", "@", "user=", "pass="]): continue
        if re.match(r'https?:\/\/[^\/]+@', line): continue
        filtered.append(line)
    with open("Danh_sach_sach.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(filtered))
    print(Fore.GREEN + f"[+] Đã lọc và lưu {len(filtered)} dòng sạch vào 'Danh_sach_sach.txt'")

# Chức năng 3
def lay_proxy():
    proxies = [
        "http://103.163.231.12:3128",
        "http://110.34.3.229:3128",
        "http://139.59.1.14:3128",
        "http://64.225.8.132:9981"
    ]
    with open("Danh_sach_proxy.txt", "w") as f:
        f.write("\n".join(proxies))
    for proxy in proxies:
        print(Fore.YELLOW + "[PROXY] " + proxy)
    print(Fore.CYAN + f"[+] Đã lưu danh sách proxy vào 'Danh_sach_proxy.txt'")

# Chức năng 4
def chuyen_domain_sang_ip(file_name="list.txt"):
    lines = read_file_with_fallback(file_name)
    if lines is None: return
    ket_qua = []
    for line in lines:
        try:
            domain = line.strip().replace("http://", "").replace("https://", "").split('/')[0]
            ip = socket.gethostbyname(domain)
            ket_qua.append(f"{domain} => {ip}")
            print(Fore.GREEN + f"[IP] {domain} => {ip}")
        except Exception:
            print(Fore.RED + f"[LỖI] Không thể chuyển {line}")
    with open("Danh_sach_IP.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(ket_qua))
    print(Fore.CYAN + f"[+] Đã lưu danh sách IP vào 'Danh_sach_IP.txt'")

# Chức năng 5
def is_valid_url(url):
    url = url.lower()
    if any(s in url for s in ['@', 'user=', 'pass=', '#admin']):
        return False
    if re.match(r'https?:\/\/[^\/]+@', url):
        return False
    return True

def check_website_alive(file_name="list.txt"):
    lines = read_file_with_fallback(file_name)
    if lines is None: return
    alive, dead = [], []

    for line in lines:
        url = line.strip()
        if not url: continue
        if not url.startswith("http"):
            url = "http://" + url
        if not is_valid_url(url):
            print(Fore.YELLOW + f"[SKIP] Bỏ qua dòng có thông tin đăng nhập: {url}")
            continue
        try:
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                print(Fore.GREEN + f"[200 OK] {url}")
                alive.append(url)
            else:
                print(Fore.YELLOW + f"[{r.status_code}] {url}")
        except:
            print(Fore.RED + f"[DOWN] {url}")
            dead.append(url)

    with open("Alive_Websites.txt", 'w') as f:
        f.write("\n".join(alive))
    if dead:
        with open("Dead_Websites.txt", 'w') as f:
            f.write("\n".join(dead))
    print(Fore.CYAN + f"[+] Live: {len(alive)} | Dead: {len(dead)}")

# Menu chính
def main_menu():
    while True:
        display_banner()
        print(Fore.YELLOW + Style.BRIGHT + """
[1] Tìm dòng chứa từ khóa
[2] Lọc bỏ dòng chứa #Admin hoặc thông tin đăng nhập
[3] Lấy proxy từ nhiều nguồn
[4] Chuyển domain sang IP
[5] Kiểm tra website còn hoạt động (HTTP 200)
[6] Thoát chương trình
""")
        lua_chon = input(Fore.GREEN + "Nhập lựa chọn (1-6): ").strip()

        if lua_chon == '1':
            keyword = input("Nhập từ khóa cần tìm: ")
            tim_dong_chua_tu_khoa("list.txt", keyword)
        elif lua_chon == '2':
            loc_bo_dong_admin("list.txt")
        elif lua_chon == '3':
            lay_proxy()
        elif lua_chon == '4':
            chuyen_domain_sang_ip("list.txt")
        elif lua_chon == '5':
            check_website_alive("list.txt")
        elif lua_chon == '6':
            print(Fore.MAGENTA + "[!] Thoát chương trình...")
            break
        else:
            print(Fore.RED + "[!] Lựa chọn không hợp lệ.")
        input(Fore.CYAN + "\n[Enter] để quay lại