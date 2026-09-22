import requests
from dataclasses import dataclass, field
import time

# response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd")
# currency = response.json()
# print(currency)

@dataclass
class Currency:
    id1: int
    name: str | int
    symbol: str | int
    price: float
    price_history: list = field(default_factory=list)
    
    def __str__(self):
        return f"{self.name}: {self.price_history}\n" f"Change: ${currency.get_price_change():.2f}"
    
    def __post_init__(self):
        if not self.price_history:
            self.price_history.append(self.price)
    
    def add_price(self, new_price):
        # add a new price to history
        self.price = new_price
        self.price_history.append(new_price)
    
    def get_price_change(self):
        # calculate price change from first to last
        if len(self.price_history) < 2:
            return 0
        return self.price_history[-1] - self.price_history[0]

def fetch_currency(endpoint_url: str = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1"):
    try:
        response = requests.get(endpoint_url, timeout=10)
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching currencies: {e}")
        return []

def create_currency_objects(data_currency):
    currency_objects = []
    for currency in data_currency:
        currency_obj = Currency(
            id1=currency['id'],
            name=currency['name'],
            symbol=currency['symbol'],
            price=currency['current_price']
        )
        currency_objects.append(currency_obj)
    return currency_objects

def save_currency_to_file(currency_objects):
    with open("currency.txt", "w", encoding="utf-8") as file:
        for currency in currency_objects:
            file.write(f"{currency.id1},{currency.name},{currency.symbol},{currency.price}\n")

currency_data = fetch_currency()
currency_objects = create_currency_objects(currency_data)
save_currency_to_file(currency_objects)  # save

print("Fetched initial prices. Waiting 5 seconds...\n")
time.sleep(5)  # wait 10 seconds

currency_objects[0].add_price(85300)  # bitcoin goes up
currency_objects[1].add_price(2720)   # ethereum goes down

for currency in currency_objects[:2]:
    print(currency)
