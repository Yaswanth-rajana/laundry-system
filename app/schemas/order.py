from pydantic import BaseModel, field_validator
from typing import List, Optional

class Garment(BaseModel):
    type: str
    quantity: int
    
    @field_validator('type')
    def validate_garment_type(cls, v):
        allowed = ['Shirt', 'Pants', 'Saree']
        if v not in allowed:
            raise ValueError(f'Invalid garment. Allowed: {", ".join(allowed)}')
        return v
    
    @field_validator('quantity')
    def validate_quantity(cls, v):
        if v < 1:
            raise ValueError('Quantity must be at least 1')
        if v > 99:
            raise ValueError('Quantity cannot exceed 99')
        return v

class OrderCreate(BaseModel):
    customer_name: str
    phone: str
    garments: List[Garment]
    notes: Optional[str] = ""
    
    @field_validator('customer_name')
    def validate_name(cls, v):
        v = v.strip()
        if len(v) < 2:
            raise ValueError('Name must be at least 2 characters')
        return v
    
    @field_validator('phone')
    def validate_phone(cls, v):
        v = v.strip()
        if not v.isdigit() or len(v) != 10:
            raise ValueError('Phone must be 10 digits')
        return v
    
    @field_validator('garments')
    def validate_garments_not_empty(cls, v):
        if not v:
            raise ValueError('At least one garment required')
        return v

class StatusUpdate(BaseModel):
    status: str
    
    @field_validator('status')
    def validate_status(cls, v):
        allowed = ['RECEIVED', 'PROCESSING', 'READY', 'DELIVERED']
        if v not in allowed:
            raise ValueError(f'Invalid status. Allowed: {", ".join(allowed)}')
        return v
