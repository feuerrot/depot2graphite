#!/usr/bin/env python3
import logging
import json
from fints.client import FinTS3PinTanClient

config = json.load(open("config", "r"))

def get_client(config):
	login = config["fints"]
	client = FinTS3PinTanClient(
		login["blz"],
		login["user"],
		login["pin"],
		login["url"]
	)
	return client

def get_holdings(client):
	accounts = client.get_sepa_accounts()
	holdings = []
	for account in accounts:
		for holding in client.get_holdings(account):
			holdings.append(holding)

	return holdings

def print_holdings(holdings):
	for holding in sorted(holdings):
		print("{}: {: >7.2f}\t{: >7.2f}\t{: >7.2f}\t{: >7.2f}\t{}".format(
			holding.ISIN,
			holding.pieces,
			holding.acquisitionprice * holding.pieces,
			holding.total_value,
			(holding.total_value / (holding.acquisitionprice * holding.pieces) - 1)*100,
			holding.name
		))

def main(config):
	c = get_client(config)
	h = get_holdings(c)
	print_holdings(h)

if __name__ == "__main__":
	main(config)
