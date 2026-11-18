# Imports
import argparse
import httpx
import random
import time
from datetime import datetime, timedelta
from multiprocessing import Process
import json

parser = argparse.ArgumentParser()
client = httpx.Client(http2=True, verify=False, follow_redirects=True)
parser.add_argument("-d", "--domain", help="Mandatory - root domain")
parser.add_argument("-t", "--time", help="Optional - Time to run traffic in minutes (default 30 m)")
parser.add_argument("-s", "--subdomain", help="Optional - define additional subdomains. Syntax: -s www,api,contact")
parser.add_argument("--tls", action='store_true', help="Run over HTTPS (default setting)")
parser.add_argument("--notls", action='store_false', help="Run requests over HTTP")
parser.set_defaults(tls=True)
args = parser.parse_args()

f = open("resources.json")
jsond = json.load(f)

top_browser_uas = list(jsond['user_agents']['top_browser_user_agents'].keys())
top_browser_ua_weights = list(jsond['user_agents']['top_browser_user_agents'].values())

uri_single = list(jsond['uris']['common_uris']['single'].keys())
uri_single_weights = list(jsond['uris']['common_uris']['single'].values())
uri_years = list(jsond['uris']['common_uris']['years'].keys())
uri_years_weights = list(jsond['uris']['common_uris']['years'].values())
uri_months = list(jsond['uris']['common_uris']['months'].keys())
uri_months_weights = list(jsond['uris']['common_uris']['months'].values())


class Traffic:

    def __init__(self, domain, time, subdomain):
        self.domain = domain
        self.time = time
        self.subdomain = subdomain

    def apex_traffic(self):
        weighted_uas = str(random.choices(top_browser_uas, weights=top_browser_ua_weights, k=1))[2:-2]
        while datetime.now() < self.time:
            response = client.get(
                url=f"https://{self.domain}{str(random.choices(uri_single, weights=uri_single_weights, k=1))[2:-2]}",
                headers={"User-Agent": f"{weighted_uas}", "referer": ""})
            print(f"apex traffic:\n {response.request.headers.get('user-agent')}\n {response.url}")
            time.sleep(random.randint(1, 5))

    def apex_traffic_second_stream(self):
        weighted_uas = str(random.choices(top_browser_uas, weights=top_browser_ua_weights, k=1))[2:-2]
        while datetime.now() < self.time:
            response = client.get(
                url=f"https://{self.domain}{str(random.choices(uri_single, weights=uri_single_weights, k=1))[2:-2]}",
                headers={"User-Agent": f"{weighted_uas}", "referer": ""})
            print(f"apex traffic stream two:\n {response.request.headers.get('user-agent')}\n {response.url}")
            time.sleep(random.randint(1, 5))

    def apex_traffic_third_stream(self):
        weighted_uas = str(random.choices(top_browser_uas, weights=top_browser_ua_weights, k=1))[2:-2]
        while datetime.now() < self.time:
            response = client.get(
                url=f"https://{self.domain}{str(random.choices(uri_single, weights=uri_single_weights, k=1))[2:-2]}",
                headers={"User-Agent": f"{weighted_uas}", "referer": ""})
            print(f"apex traffic stream two:\n {response.request.headers.get('user-agent')}\n {response.url}")
            time.sleep(random.randint(1, 5))

    def subdomain_traffic(self):
        weighted_uas = str(random.choices(top_browser_uas, weights=top_browser_ua_weights, k=1))[2:-2]
        values = args.subdomain.split(",")
        sub = random.choice(values)

        while datetime.now() < self.time:
            url = f"{sub}.{self.domain}"
            response = client.get(
                url=f"https://{url}{str(random.choices(uri_single, weights=uri_single_weights, k=1))[2:-2]}",
                headers={"User-Agent": f"{weighted_uas}", "referer": ""})
            time.sleep(random.randint(1, 5))
            print(f"apex traffic stream two:\n {response.request.headers.get('user-agent')}\n {response.url}")

    def subdomain_traffic_second_stream(self):
        weighted_uas = str(random.choices(top_browser_uas, weights=top_browser_ua_weights, k=1))[2:-2]
        values = args.subdomain.split(",")
        while datetime.now() < self.time:
            url = f"{random.choice(values)}.{self.domain}"
            response = client.get(
                url=f"https://{url}{str(random.choices(uri_single, weights=uri_single_weights, k=1))[2:-2]}",
                headers={"User-Agent": f"{weighted_uas}", "referer": ""})
            time.sleep(random.randint(1, 5))
            print(f"apex traffic stream two:\n {response.request.headers.get('user-agent')}\n {response.url}")


def run_in_parallel(fns):
    proc = []
    for fn in fns:
        p = Process(target=fn["name"])
        p.start()
        proc.append(p)
    for p in proc:
        p.join()


if __name__ == "__main__":
    current_time = datetime.now()

    if args.domain:
        domain = args.domain
        if not args.time:
            new_time = current_time + timedelta(minutes=30)
        else:
            new_time = current_time + timedelta(seconds=int(args.time))
        if not args.subdomain:
            subdomain = 0
            traffic_generator = Traffic(domain, new_time, subdomain)
            run_in_parallel(
                [{'name': traffic_generator.apex_traffic}, {'name': traffic_generator.apex_traffic_second_stream},
                 {'name': traffic_generator.apex_traffic_third_stream()}])
        else:
            subdomain = 1
            traffic_generator = Traffic(domain, new_time, subdomain)
            run_in_parallel([{'name': traffic_generator.apex_traffic}, {'name': traffic_generator.subdomain_traffic},
                             {'name': traffic_generator.apex_traffic_second_stream}])
    else:
        print("Specify the root domain with a -d or --domain flag")
