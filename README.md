# Custom Webhook Bridge

A lightweight Python API that acts as a custom middleware layer between incoming lead sources and third-party CRM platforms — a self-hosted alternative to tools like Zapier or Make.

---

## What It Does

When a lead form, external service, or automation tool sends a raw payload to this server, the bridge:

1. **Validates** the incoming data — rejects empty or whitespace-only fields with a clear error.
2. **Transforms** the payload — splits `full_name` into `first_name` / `last_name`, maps `contact_number` to `phone`, and strips accidental whitespace from all fields.
3. **Forwards** the clean, structured payload to a third-party destination (CRM, database, email tool, etc.).

No third-party automation platform needed. You own the logic.

---

## How It Works

```
Lead Form / External Service
        │
        ▼
POST /incoming-lead
        │
   [Validation]  ◄── rejects empty name or phone (422)
        │
  [Transformation]
   full_name      →  first_name + last_name
   contact_number →  phone
   all fields     →  whitespace stripped
        │
        ▼
  Outgoing Payload  →  CRM / Database / 3rd Party API
```

---

## Project Structure

```
custom-webhook-bridge/
├── server.py          # FastAPI application — validation, transformation, forwarding
├── test_trigger.py    # Test script — fires mock POST requests to verify the server
└── venv/              # Python virtual environment
```

---

## Incoming Payload Format

```json
{
    "full_name": "John Doe",
    "contact_number": "555-1234",
    "goal": "weight loss"
}
```

## Transformed Output

```json
{
    "first_name": "John",
    "last_name": "Doe",
    "phone": "555-1234",
    "goal": "weight loss"
}
```

---

## Validation Rules

| Field | Rule |
|---|---|
| `full_name` | Required, must not be empty or blank |
| `contact_number` | Required, must not be empty or blank |
| `goal` | Required |

Invalid requests receive a `422 Unprocessable Entity` response with a descriptive error message.

**Example rejection:**
```json
{
    "detail": [
        {
            "type": "value_error",
            "loc": ["body", "full_name"],
            "msg": "Value error, full_name must not be empty"
        }
    ]
}
```

---

## How to Run

**1. Activate the virtual environment:**
```bash
source venv/bin/activate
```

**2. Start the server:**
```bash
uvicorn server:app --reload
```

Server runs at `http://127.0.0.1:8000`.

**3. In a second terminal, fire the test requests:**
```bash
python test_trigger.py
```

---

## Requirements

- Python 3.x
- FastAPI
- Uvicorn
- Requests

Install all dependencies:
```bash
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn requests
```

---

## Customization

| What you want to change | Where to change it |
|---|---|
| Transformation logic | `receive_lead()` in `server.py` |
| Validation rules | `@field_validator` methods in `IncomingLead` |
| Forward to a real CRM | Replace the `print()` in `receive_lead()` with an HTTP call to your CRM's API |
| Add new fields | Extend the `IncomingLead` model in `server.py` |

---

## Use Case

Built for freelancers and businesses that need to:
- Accept leads from any form or service without relying on Zapier or Make
- Transform and normalize incoming data before it hits a CRM
- Own and control their integration logic with no monthly subscription cost
