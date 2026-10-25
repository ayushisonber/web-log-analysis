import random
from datetime import datetime, timedelta

NUM_RECORDS = 500000

ips = [
    "192.168.1.10",
    "192.168.1.11",
    "192.168.1.12",
    "192.168.1.13",
    "192.168.1.14",
    "10.0.0.5",
    "10.0.0.6",
    "172.16.0.10"
]

urls = [
    "/",
    "/home",
    "/login",
    "/products",
    "/products/laptop",
    "/products/mobile",
    "/products/headphones",
    "/about",
    "/contact",
    "/cart",
    "/checkout",
    "/profile",
    "/search",
    "/api/products",
    "/api/users"
]

methods = ["GET", "GET", "GET", "GET", "POST"]

status_codes = [200, 200, 200, 200, 201, 301, 302, 400, 404, 500]

start_time = datetime(2026, 9, 1, 0, 0, 0)

with open("access.log", "w") as file:

    for i in range(NUM_RECORDS):

        ip = random.choice(ips)

        current_time = start_time + timedelta(
            seconds=random.randint(0, 30 * 24 * 60 * 60)
        )

        method = random.choice(methods)
        url = random.choice(urls)
        status = random.choice(status_codes)

        if status == 200:
            bytes_sent = random.randint(500, 50000)
        elif status == 404:
            bytes_sent = random.randint(100, 1000)
        else:
            bytes_sent = random.randint(100, 5000)

        timestamp = current_time.strftime("%d/%b/%Y:%H:%M:%S")

        log_line = (
            f'{ip} - - [{timestamp}] '
            f'"{method} {url} HTTP/1.1" '
            f'{status} {bytes_sent}\n'
        )

        file.write(log_line)

print("Dataset generated successfully!")
print("Total records:", NUM_RECORDS)
