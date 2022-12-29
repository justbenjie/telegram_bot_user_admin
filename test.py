import re
from bot.api_client.api_requests import api_requests

# phone_numbers = [
#     "+375 29 19 29 727",
#     "80291929727",
#     "+375448092233",
#     "3752949388234s",
#     "+37529302091t",
#     "+375441939228",
#     "",
#     "",
#     "",
# ]
# for phone in phone_numbers:
#     if re.match(r"^(\+375|80)(29|25|44|33)(\d{7})$", phone):
#         print(f"Found phone number: {phone}")
#     else:
#         print(f"Did not find phone number: {phone}")

response = api_requests.post(
    "/admins/",
    json={"user_id": 1},
)

print(response.status_code, response.json())
