import requests

def convert_currency(amount, from_currency, to_currency):
    try:
        base_url = "https://api.fxratesapi.com/convert"
        params = {
            "from": from_currency.upper(),
            "to": to_currency.upper(),
            "amount": amount,
            "format": "json"
        }

        response = requests.get(base_url, params=params)
        data = response.json()

        if response.status_code == 200 and data.get("success"):
            print(data)
            print(round(data["result"], 2))
            print(round(data["info"]["rate"], 4))
            return {
                "converted_amount": round(data["result"], 2),
                "exchange_rate": round(data["info"]["rate"], 2)
            }
        else:
            raise ValueError("Currency conversion failed or unsupported currency.")
    
    except Exception as e:
        raise Exception(f"Currency conversion error: {str(e)}")
