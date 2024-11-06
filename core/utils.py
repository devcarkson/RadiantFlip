import requests

# This function fetches live conversion rates from CoinGecko for multiple cryptocurrencies
def get_live_rate(payment_system):
    url = 'https://api.coingecko.com/api/v3/simple/price'
    params = {
        'ids': 'bitcoin,ethereum,tether',  # Add more as necessary
        'vs_currencies': 'usd'
    }
    response = requests.get(url, params=params)
    data = response.json()

    if payment_system == 'Bitcoin':  # Bitcoin
        return data['bitcoin']['usd']
    elif payment_system == 'Ethereum':  # Ethereum
        return data['ethereum']['usd']
    elif payment_system == 'Litecoin':  # Litecoin
        return data['tether']['usd']
    return 1
