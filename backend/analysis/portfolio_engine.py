class PortfolioEngine:
    def __init__(self, portfolio):
        self.portfolio = portfolio

    def calculate_total_value(self):
        total_value = sum(asset['value'] for asset in self.portfolio)
        return total_value

    def calculate_return_on_investment(self):
        initial_investment = sum(asset['initial_value'] for asset in self.portfolio)
        current_value = self.calculate_total_value()
        roi = (current_value - initial_investment) / initial_investment * 100 if initial_investment > 0 else 0
        return roi

    def get_asset_allocation(self):
        total_value = self.calculate_total_value()
        allocation = {asset['name']: (asset['value'] / total_value) * 100 for asset in self.portfolio} if total_value > 0 else {}
        return allocation

    def generate_report(self):
        report = {
            'total_value': self.calculate_total_value(),
            'roi': self.calculate_return_on_investment(),
            'allocation': self.get_asset_allocation(),
        }
        return report