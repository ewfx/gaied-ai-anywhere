from typing import Optional
from pydantic import BaseModel, Field

class DuplicateFlag(BaseModel):
    flag: bool = Field(
        ...,
        description="Indicates whether the email is a duplicate within the same thread. "
                    "A value of 'True' means the email is a reply or forward and does not initiate a new request. "
                    "'False' signifies the initial request email that starts the conversation."
    )
    reason: str = Field(
        ...,
        description="Explains why the email was flagged as a duplicate or not. "
                    "If 'flag' is True, reasons include 'Reply within the thread' or 'Forwarded email'. "
                    "If 'flag' is False, the reason should be 'Initial request email starting the thread'."
    )

class SubRequestType(BaseModel):
    name: str = Field(..., description="Name of the sub-request type associated with the main request type.")

class RequestType(BaseModel):
    name: str = Field(..., description="Name of the primary request type assigned to the email.")
    sub_types: list[SubRequestType] = Field(..., description="List of sub-request types under this request type.")

class ClassificationResult(BaseModel):
    result: list[RequestType] = Field(
        default_factory=list,  
        description="A list of request types assigned to the email, ordered by priority. Each request type contains its associated sub-request types."
    )
    confidence_score: int = Field(
        default=0,  
        description="Confidence level of the classification result, ranging from 0 (lowest) to 100 (highest)."
    )
    reason: Optional[str] = Field(
        default="No reason provided.",  
        description="Provides the reason behind the classification of the email."
    )

class ExtractedFields(BaseModel):
    extracted_values: list[str] = Field(
        default=[],
        description="List of key values extracted from the email"
    )

class EmailState(BaseModel):
    email_content: str
    email_intent: str = Field(default="Unknown")  
    is_duplicate: bool = Field(default=False)  
    dup_reason: str = Field(default="Not evaluated")
    classification_result: ClassificationResult = Field(default_factory=ClassificationResult)
    extracted_fields: dict = Field(default={})
    