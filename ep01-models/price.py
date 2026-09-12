from config import RATE_IN, RATE_OUT, BUDGET_PER_TICKET


class BudgetExceeded(Exception):
    pass


def log_cost(ticket_id, cost):
    print(f"{ticket_id}\tcost={cost:.6f}")


def price(resp, ticket_id):
    u = resp.usage
    cost = (u.input_tokens * RATE_IN
            + u.output_tokens * RATE_OUT)
    log_cost(ticket_id, cost)
    if cost > BUDGET_PER_TICKET:
        raise BudgetExceeded(ticket_id)
    return cost
