import re, json

def masking(number): 
    num_len = len(number)
    # prefix = re.split(r'(+?\d{2})(\d{4})', number)
    # prefix = re.findall(r'(\+?\d{2})', number)
    if num_len < 10 and num_len > 11:
        return 
    
    # if re.findall(r'')

    if number[0] == '+':
        if re.findall(r'\D',number[1:]):
            return
        prefix = number[:3]
    else:
        if re.findall(r'\D',number):
            return
        prefix = number[:2]
    
    subfix = number[-4:]
    # print(prefix)
    # print(subfix)
    return prefix+'*'*(num_len-len(prefix+subfix)) +subfix



if __name__ == "__main__":
    input_data = '''
    {
        "id": "8888",
        "content": {
            "timestamp": "2023-05-17T04:06:34.466Z",
            "tags": [
            ],
            "service": "aws",
            "attributes": {
                "datacontenttype": "application/json",
                "data": {
                    "messageStatus": "UNDELIVERED",
                    "to": "+658888888",
                    "display_phone_number": "6582410624",
                    "recipient_id": "6586734692",
                    "timestamp": "2023-05-17T04:06:22.659Z"
                },
                "id": "EZ2e1db131fc165d33378666f6e545c630",
                "type": "com.twilio.messaging.message.undelivered"
            }
        }
    }
    '''

    # Parse the input JSON data
    parsed_data = json.loads(input_data)

    # Mask phone numbers in the "data" section
    parsed_data["content"]["attributes"]["data"]["to"] = masking(parsed_data["content"]["attributes"]["data"]["to"])
    parsed_data["content"]["attributes"]["data"]["display_phone_number"] = masking(parsed_data["content"]["attributes"]["data"]["display_phone_number"])
    parsed_data["content"]["attributes"]["data"]["recipient_id"] = masking(parsed_data["content"]["attributes"]["data"]["recipient_id"])

    # Convert the modified data back to JSON format
    masked_data = json.dumps(parsed_data, indent=4)

    print(masked_data)
    # number = input()
    # masking_number = masking(number)
    # print(masking_number)