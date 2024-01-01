from django.shortcuts import render, redirect
from .models import Stock
from .forms import StockForm
from django.contrib import messages


def home(request):
	import requests
	import json

	if request.method =='POST':
		ticker = request.POST['ticker']
			
		api_request = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=" + ticker + "&apikey=ZH9G4KRDQ09KQ8QN")

		try:
			api = json.loads(api_request.content)
			metadata = api['Meta Data']
			time_series_data = api['Time Series (Daily)']
			latest_data = next(iter(time_series_data.values())) # Get the latest data point
			symbol = metadata['2. Symbol']
			open_price = "{:.2f}".format(float(latest_data['1. open']))
			high_price = "{:.2f}".format(float(latest_data['2. high']))
			low_price = "{:.2f}".format(float(latest_data['3. low']))
			close_price = "{:.2f}".format(float(latest_data['4. close']))
			volume = latest_data['5. volume']

			context = {
				'symbol': symbol,
				'open_price': open_price,
				'high_price': high_price,
				'low_price': low_price,
				'close_price': close_price,
				'volume': volume,
			}

			return render(request, 'home.html', context=context)

		except Exception as e:
			api = "Error..."
			
			return render(request, 'home.html', {'api': api})

	else:
		return render(request, 'home.html', {'ticker': "Enter a Ticker Symbol Above..."})

def about(request):
	return render(request, 'about.html', {})

def trending_tickers(request):
	return render(request, 'trending_tickers.html', {})

def add_stock(request):
	import requests
	import json

	if request.method =='POST':
		form = StockForm(request.POST or None)

		if form.is_valid():
			form.save()
			messages.success(request, ("Stock Has Been Added!"))
			return redirect('add_stock')


	# Inside the add_stock view function in views.py
# (Please replace this code within your existing view function)

	else:
	    ticker = Stock.objects.all()
	    output = []

	    for ticker_item in ticker:
	        api_request = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=" + str(ticker_item) + "&apikey=ZH9G4KRDQ09KQ8QN")
	        
	        try:
	            api = json.loads(api_request.content)
	            metadata = api['Meta Data']
	            time_series_data = api['Time Series (Daily)']
	            latest_data = next(iter(time_series_data.values()))  # Get the latest data point
	            symbol = metadata['2. Symbol']
	            open_price = "{:.2f}".format(float(latest_data['1. open']))
	            high_price = "{:.2f}".format(float(latest_data['2. high']))
	            low_price = "{:.2f}".format(float(latest_data['3. low']))
	            close_price = "{:.2f}".format(float(latest_data['4. close']))
	            volume = latest_data['5. volume']

	            # Check if all data is available before appending to output
	            if all([symbol, open_price, high_price, low_price, close_price, volume]):
	                context = {
	                    'symbol': symbol,
	                    'open_price': open_price,
	                    'high_price': high_price,
	                    'low_price': low_price,
	                    'close_price': close_price,
	                    'volume': volume,
	                }
	                output.append(context)
	        except Exception as e:
	            api = "Error..."

	    return render(request, 'add_stock.html', {'ticker': ticker, 'output': output})


def delete(request, stock_id):
	item = Stock.objects.get(pk=stock_id)
	item.delete()
	messages.success(request, ("Stock Has Been Deleted!"))
	return redirect(delete_stock)

def delete_stock(request):
	ticker = Stock.objects.all()
	return render(request, 'delete_stock.html', {'ticker': ticker})