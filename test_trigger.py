import requests

URL = "http://127.0.0.1:8000/incoming-lead"

test_cases = [
    {"full_name": "John Doe",        "contact_number": "555-1234",        "goal": "weight loss"},
    {"full_name": "Maria Garcia",    "contact_number": "(555) 987-6543",   "goal": "muscle gain"},
    {"full_name": "Ali",             "contact_number": "555.000.1111",     "goal": "flexibility"},
    {"full_name": "Jean-Luc Picard", "contact_number": "555-0042",         "goal": "cardio"},
    {"full_name": "",                "contact_number": "555-9999",         "goal": "stress relief"},
    {"full_name": "Bruce Lee",       "contact_number": "",                 "goal": "martial arts"},
    {"full_name": "  Anna Smith  ",  "contact_number": "  555-3210  ",     "goal": "  yoga  "},
]

for i, payload in enumerate(test_cases, 1):
    try:
        response = requests.post(URL, json=payload)
        print(f"[Test {i}] {response.status_code} | {response.json()} | Input: {payload}")
    except Exception as e:
        print(f"[Test {i}] ERROR: {e}")
