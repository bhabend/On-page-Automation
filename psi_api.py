import requests
import os

def get_pagespeed_data(url):
    key = os.getenv("PSI_API_KEY")
    api_url = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&key={key}&strategy=mobile"
    try:
        res = requests.get(api_url)
        data = res.json()
        lighthouse = data.get("lighthouseResult", {})
        return {
            "Performance Score": lighthouse.get("categories", {}).get("performance", {}).get("score", 0) * 100,
            "FCP": lighthouse.get("audits", {}).get("first-contentful-paint", {}).get("displayValue", "N/A"),
            "LCP": lighthouse.get("audits", {}).get("largest-contentful-paint", {}).get("displayValue", "N/A"),
            "CLS": lighthouse.get("audits", {}).get("cumulative-layout-shift", {}).get("displayValue", "N/A"),
        }
    except Exception as e:
        print(f"PSI API error: {e}")
        return {"Performance Score": "Error", "FCP": "N/A", "LCP": "N/A", "CLS": "N/A"}
