def calculate_buy_and_hold(investment, prices):
    """
    Calculate the final value of a buy-and-hold investment strategy.

    Parameters:
    investment (float): The initial amount invested.
    prices (list): A list of prices over time.

    Returns:
    float: The final value of the investment.
    """
    if not prices:
        return investment

    # Buy at the first price
    initial_price = prices[0]
    shares_bought = investment / initial_price

    # Value at the last price
    final_price = prices[-1]
    final_value = shares_bought * final_price

    return final_value


def calculate_return_on_investment(investment, final_value):
    """
    Calculate the return on investment (ROI).

    Parameters:
    investment (float): The initial amount invested.
    final_value (float): The final value of the investment.

    Returns:
    float: The ROI as a percentage.
    """
    if investment == 0:
        return 0.0

    roi = ((final_value - investment) / investment) * 100
    return roi