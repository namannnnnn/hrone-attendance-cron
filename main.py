import requests
from datetime import datetime
import pytz

# Convert current UTC time to IST
ist = pytz.timezone('Asia/Kolkata')
now_ist = datetime.now(ist)
punch_time = now_ist.strftime('%Y-%m-%dT%H:%M')
# Step 1: Login and get access token
login_url = "https://gateway.app.hrone.cloud/oauth2/token"
login_payload = {
    "username": "naman.parmar@vinculumgroup.com",
    "password": "HRONE@vinnaman021000",
    "grant_type": "password",
    "loginType": "1",
    "companyDomainCode": "vinculum",
    "isUpdated": "0",
    "validSource": "Y",
    "deviceName": "Chrome-unknown"
}

session = requests.Session()

headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json, text/plain, */*",
    "origin": "https://app.hrone.cloud",
    "referer": "https://app.hrone.cloud/",
}

response = session.post(login_url, data=login_payload, headers=headers)

if response.status_code == 200 and "access_token" in response.json():
    access_token = response.json()["access_token"]
    print("✅ Login successful.")
    resp = requests.get('https://geo.brdtest.com/mygeo.json')
    print(resp.json())
    # Step 2: Get employee ID
    session.headers.update({
        "Authorization": f"Bearer {access_token}",
        "domaincode": "vinculum",
        "hrone-refresh-header": "true",
        "x-requested-with": "https://app.hrone.cloud",
        "Content-Type": "application/json"
    })

    user_detail_url = "https://app.hrone.cloud/api/LogOnUser/LogOnUserDetail"
    user_detail_resp = session.get(user_detail_url)

    if user_detail_resp.status_code == 200 and "employeeId" in user_detail_resp.json():
        employee_id = user_detail_resp.json()["employeeId"]
        print(f"👤 Employee ID: {employee_id}")

        # Step 3: Mark Attendance
        attendance_url = "https://app.hrone.cloud/api/timeoffice/mobile/checkin/Attendance/Request"

        current_time = datetime.now().strftime("%Y-%m-%dT%H:%M")

        attendance_payload = {
            "requestType": "A",
            "applyRequestSource": 10,
            "employeeId": employee_id,
            "latitude": "",
            "longitude": "",
            "geoAccuracy": "",
            "geoLocation": "",
            "punchTime": punch_time,
            "remarks": "",
            "uploadedPhotoOneName": "",
            "uploadedPhotoOnePath": "",
            "uploadedPhotoTwoName": "",
            "uploadedPhotoTwoPath": "",
            "attendanceSource": "W",
            "attendanceType": "Online"
        }

        attendance_resp = session.post(attendance_url, json=attendance_payload)

        if attendance_resp.status_code == 200:
            print("✅ Attendance marked successfully!")
            print(attendance_resp.json())
        else:
            print("❌ Failed to mark attendance.")
            print(attendance_resp.status_code, attendance_resp.text)
    else:
        print("❌ Failed to get employee ID.")
        print(user_detail_resp.status_code, user_detail_resp.text)
else:
    print("❌ Login failed.")
    print(response.status_code, response.text)
