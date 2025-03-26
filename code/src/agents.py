from dotenv import load_dotenv
load_dotenv()
from langchain_core.prompts import PromptTemplate
from langchain.chat_models import init_chat_model
from models import (
    DuplicateFlag,
    ClassificationResult,
    ExtractedFields,
    EmailState
)

request_types_dict = {
    "Adjustment": [],
    "AU Transfer": [],
    "Closing Notice": ["Reallocation Fees", "Amendment Fees", "Reallocation Principal"],
    "Commitment Change": ["Cashless Roll", "Decrease", "Increase"],
    "Fee Payment": ["Ongoing Fee", "Letter of Credit Fee"],
    "Money Movement - Inbound": ["Principal", "Interest", "Principal+Interest", "Principal+Interest+Fee"],
    "Money Movement - Outbound": ["Timebound", "Foreign Currency"]
}

config_fields_dict = {
    "Adjustment": ["deal_name", "adjustment_amount", "adjustment_reason", "effective_date"],
    "AU Transfer": ["account_number", "transfer_amount", "transfer_date", "recipient_name"],
    "Closing Notice": ["deal_name", "closing_date", "counterparty", "final_amount"],
    "Commitment Change": ["deal_name", "old_commitment", "new_commitment", "effective_date", "change_reason"],
    "Fee Payment": ["invoice_number", "fee_amount", "due_date", "payment_status"],
    "Money Movement - Inbound": ["sender_name", "amount_received", "transaction_date", "reference_number"],
    "Money Movement - Outbound": ["recipient_name", "amount_sent", "transaction_date", "payment_method"]
}


def duplicate_checker(state: EmailState):
    llm = init_chat_model(model="llama-3.3-70b-versatile", temperature=0, model_provider="groq")
    llm = llm.with_structured_output(DuplicateFlag)
    prompt = PromptTemplate(
        template="""Here is the email content: {email_content}""",
        input_variables=["email_content"],
    )
    chain = prompt | llm
    result = chain.invoke({"email_content": state.email_content})
    state.dup_reason = result.reason
    state.is_duplicate = result.flag
    return {"is_duplicate": result.flag, "dup_reason": result.reason}


def router(state: EmailState):
    return state.is_duplicate


def intent_identifier(state: EmailState):
    llm = init_chat_model(model="llama-3.3-70b-versatile", temperature=0, model_provider="groq")
    prompt = PromptTemplate(
        template="""You are an AI assistant analyzing service request emails received by the Commercial Bank Lending Service team. 
        Your task is to extract the core intent of the given email in a concise yet comprehensive manner. Focus on capturing the 
        main purpose of the email in a clear and professional way while preserving key details.
        Here is the email content: 

        {email_content} 

        Provide a well-formed sentence or short paragraph that accurately conveys the request or purpose of the email.""",
        input_variables=["email_content"],
    )
    chain = prompt | llm
    result = chain.invoke({"email_content": state.email_content})
    return {"email_intent": result.content}


def intent_clasifier(state: EmailState):
    llm = init_chat_model(model="llama-3.3-70b-versatile", temperature=0, model_provider="groq")
    llm = llm.with_structured_output(ClassificationResult)
    prompt = PromptTemplate(
        template="""You are an AI assistant that extracts request types and sub-request types from emails received by the Commercial Bank Lending Service team. 
        Given an email's intent and a dictionary of available request types and sub-types, identify the most relevant request types, assign appropriate sub-request types, and rank them in order of priority if multiple request types apply. 
        Use only request types and sub-types from the provided dictionary.

        ## Email Intent:
        {email_intent}
        
        ## Available Request Types and their Sub-Types:
        {request_types_dict}
        
        Now, extract the request details based on the given email intent.
        """,
        input_variables=["email_intent", "request_types_dict"],
    )

    chain = prompt | llm
    result = chain.invoke({"email_intent": state.email_intent, "request_types_dict": request_types_dict})
    return {"classification_result": result}


def fields_extractor(state: EmailState):
    fields_to_extract = []
    request_type_names = [request_type.name for request_type in state.classification_result.result]
    for name in request_type_names:
        fields_to_extract += config_fields_dict[name]

    llm = init_chat_model(model="llama-3.3-70b-versatile", temperature=0, model_provider="groq")
    llm = llm.with_structured_output(ExtractedFields)
    prompt = PromptTemplate(
        template="""You are an AI assistant that extracts values of fields provided from the email content. 
        Fields to be extracted is given in the form of a list. Extracted values must be returned in the form of a list.
        Extracted values should follow the same order as the fields given in the list.
        If value doesn't exist, populate with 'doesn't exist'.

        ## Email Content:
        {email_content}
        
        ## List of Fields to extract:
        {fields_to_extract}
        
        Now, extract the values of the fields based on the given email content.
        """,
        input_variables=["email_content", "fields_to_extract"],
    )

    chain = prompt | llm
    result = chain.invoke({"email_content": state.email_content, "fields_to_extract": fields_to_extract})
    print(fields_to_extract)
    print(result.extracted_values)
    extracted_fields = {k:v for k,v in zip(fields_to_extract, result.extracted_values)}
    return {"extracted_fields": extracted_fields}