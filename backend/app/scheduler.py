import os
import json
import httpx
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from pymysqlpool.pool import Pool

# Pool fr Hintergrundjobs
pool = Pool(
    host=os.getenv("MYSQL_HOST", "mysql"),
    user=os.getenv("MYSQL_USER", "user"),
    password=os.getenv("MYSQL_PASSWORD", "password"),
    db=os.getenv("MYSQL_DATABASE", "testdb"),
    autocommit=True
)
pool.init()

CERT_API_URL = os.getenv("CERT_API_URL", "https://external-api.example.com/certs")  # extern!

def sync_certificates():
    response = httpx.get(CERT_API_URL, timeout=10)
    cert_list = response.json()
    cnx = pool.get_conn()
    with cnx.cursor() as cursor:
        for cert in cert_list:
            # Prepare/Convert types (Date, JSON etc.)
            valid_until = datetime.fromisoformat(cert["valid_until"].replace("Z", "+00:00"))
            chain_json = json.dumps(cert["chain"])
            cursor.execute(
                "REPLACE INTO certificates (id, issuer, cn, valid_until, status, certificate, chain, csr) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (
                    cert["id"], cert["issuer"], cert["cn"], valid_until, cert["status"],
                    cert["certificate"], chain_json, cert["csr"]
                )
            )
    pool.release(cnx)
    print("Certs synced.")

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(sync_certificates, "interval", minutes=30)
    scheduler.start()
