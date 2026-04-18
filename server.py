from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator

app = FastAPI()


class IncomingLead(BaseModel):
    full_name: str
    contact_number: str
    goal: str

    @field_validator("full_name", "contact_number", "goal", mode="before")
    @classmethod
    def strip_whitespace(cls, v: str) -> str:
        return v.strip()

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, v: str) -> str:
        if not v:
            raise ValueError("full_name must not be empty")
        return v

    @field_validator("contact_number")
    @classmethod
    def validate_contact_number(cls, v: str) -> str:
        if not v:
            raise ValueError("contact_number must not be empty")
        return v


@app.post("/incoming-lead")
def receive_lead(lead: IncomingLead):
    name_parts = lead.full_name.split(" ", 1)
    first_name = name_parts[0]
    last_name = name_parts[1] if len(name_parts) > 1 else ""

    transformed = {
        "first_name": first_name,
        "last_name": last_name,
        "phone": lead.contact_number,
        "goal": lead.goal,
    }

    print("[Outgoing Payload]", transformed)

    return {"status": "success"}
