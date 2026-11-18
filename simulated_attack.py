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

browser_uas = list(jsond['user_agents']['browser_user_agents'])
scanners = list(jsond['user_agents']['terminal_user_agents']['scanners'].keys())
misc_uas = list(jsond['user_agents']['terminal_user_agents']['misc'].keys())
non_browser_uas = scanners + misc_uas
all_uas = ['browser_uas', 'non_browser_uas']
all_uas_combined = non_browser_uas + browser_uas
weighted_uas = str(random.choices(all_uas, weights=[2, 1], k=1))[2:-2]

if weighted_uas == 'browser_uas':
    ua_choice = str(random.choice(browser_uas))
else:
    ua_choice = str(random.choice(non_browser_uas))

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

    def malicious_traffic_single_ua_single_uri(self):
        while datetime.now() < self.time:
            response = client.get(
                url=f"https://{self.domain}",
                headers={"User-Agent": f"{ua_choice}", "referer": ""})
            print(f"malicious_traffic_single_ua_single_ui traffic:\n {response.request.headers.get('user-agent')}\n {response.url}")

    def malicious_traffic_single_ua_random_uri(self):
        while datetime.now() < self.time:
            response = client.get(
                url=f"https://{self.domain}{str(random.choices(uri_single, weights=uri_single_weights, k=1))[2:-2]}",
                headers={"User-Agent": f"{ua_choice}", "referer": ""})
            print(f"malicious_traffic_single_ua_random_uri traffic:\n "
                  f"{response.request.headers.get('user-agent')}\n "
                  f"{response.url}")

    def malicious_traffic_random_ua_single_uri(self):
        while datetime.now() < self.time:
            response = client.get(
                url=f"https://{self.domain}",
                headers={"User-Agent": f"{str(random.choices(all_uas_combined, k=1))[2:-2]}", "referer": ""})
            print(f"malicious_traffic_random_ua_single_uri traffic:\n "
                  f"{response.request.headers.get('user-agent')}\n "
                  f"{response.url}")

    def malicious_traffic_random_ua_random_uri(self):
        while datetime.now() < self.time:
            response = client.get(
                url=f"https://{self.domain}{str(random.choices(uri_single, weights=uri_single_weights, k=1))[2:-2]}",
                headers={"User-Agent": f"{str(random.choices(all_uas_combined, k=1))[2:-2]}", "referer": ""})
            print(f"malicious_traffic_random_ua_random_uri traffic:\n "
                  f"{response.request.headers.get('user-agent')}\n "
                  f"{response.url}")

    # def subdomain_traffic(self):
    #     weighted_uas = str(random.choices(top_browser_uas, weights=top_browser_ua_weights, k=1))[2:-2]
    #     values = args.subdomain.split(",")
    #     sub = random.choice(values)

        # while datetime.now() < self.time:
        #     url = f"{sub}.{self.domain}"
        #     response = client.get(
        #         url=f"https://{self.domain}",
        #         headers={"User-Agent": f"{weighted_uas}", "referer": ""})
        #     print(f"apex traffic stream two:\n {response.request.headers.get('user-agent')}\n {response.url}")

    # def subdomain_traffic_second_stream(self):
    #     weighted_uas = str(random.choices(top_browser_uas, weights=top_browser_ua_weights, k=1))[2:-2]
    #     values = args.subdomain.split(",")
    #     while datetime.now() < self.time:
    #         url = f"{random.choice(values)}.{self.domain}"
    #         response = client.get(
    #             url=f"https://{self.domain}",
    #             headers={"User-Agent": f"{weighted_uas}", "referer": ""})
    #         print(f"apex traffic stream two:\n {response.request.headers.get('user-agent')}\n {response.url}")


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
            new_time = current_time + timedelta(minutes=3)
        else:
            new_time = current_time + timedelta(seconds=int(args.time))
        if not args.subdomain:
            subdomain = 0
            traffic_generator = Traffic(domain, new_time, subdomain)
            run_in_parallel([{'name': traffic_generator.malicious_traffic_single_ua_single_uri},
                             {'name': traffic_generator.malicious_traffic_single_ua_random_uri},
                             {'name': traffic_generator.malicious_traffic_random_ua_single_uri},
                             {'name': traffic_generator.malicious_traffic_random_ua_random_uri}
                             ])
        else:
            subdomain = 1
            traffic_generator = Traffic(domain, new_time, subdomain)
            run_in_parallel([{'name': traffic_generator.malicious_traffic_single_ua_single_uri},
                             {'name': traffic_generator.malicious_traffic_single_ua_random_uri},
                             {'name': traffic_generator.malicious_traffic_random_ua_single_uri},
                             {'name': traffic_generator.malicious_traffic_random_ua_random_uri}
                             ])
    else:
        print("Specify the root domain with a -d or --domain flag")
