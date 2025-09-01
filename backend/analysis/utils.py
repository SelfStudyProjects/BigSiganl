def calculate_average(data):
    if not data:
        return 0
    return sum(data) / len(data)

def format_currency(value):
    return "${:,.2f}".format(value)

def validate_portfolio_data(portfolio_data):
    required_fields = ['name', 'investments']
    for field in required_fields:
        if field not in portfolio_data:
            raise ValueError(f"Missing required field: {field}")
    return True

def generate_report(data):
    report = {
        "total_investments": sum(item['amount'] for item in data),
        "average_investment": calculate_average([item['amount'] for item in data]),
    }
    return report