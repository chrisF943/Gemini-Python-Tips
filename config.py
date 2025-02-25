SSL_PROVIDER_HOSTS = {
    "gmail": "smtp.gmail.com",
    "aol": "smtp.aol.com",
    "att": "smtp.att.net",
    "verizon": "smtp.verizon.net",
}

TLS_PROVIDER_HOSTS = {
    "outlook": "smtp-mail.outlook.com",
    "yahoo": "smtp.mail.yahoo.com",
    "icloud": "smtp.mail.me.com"
}

PROVIDER_PORTS = {
    "ssl": 465,
    "tls": 587
}

CHOSEN_PROVIDER = ""

# To see available models, refer to: https://ai.google.dev/gemini-api/docs/models/gemini
# Please keep in mind the rate limit for the model you choose,
# which can be found here: https://ai.google.dev/gemini-api/docs/rate-limits
# Rate limits depend on the tier of your account
CHOSEN_MODEL = ""

SAVE_LOGS = False
