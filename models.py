from uagents import Model

class LoanRequest(Model):
    name: str
    amount: float

class LoanResponse(Model):
    message: str

class ClientConfirmation(Model):
    confirmation: str
