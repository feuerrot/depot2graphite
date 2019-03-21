#!/usr/bin/env python3
import graphitesend
import logging
import json
from fints.client import FinTS3PinTanClient

config = json.load(open("config", "r"))

def get_graphite(config):
	connection = config["graphite"]
	graphite = graphitesend.init(
		prefix=connection["prefix"],
		system_name="",
		graphite_server=connection["server"],
		graphite_port=connection["port"]
	)
	return graphite

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

def send_holding(graphite, holding):
	def fmt(h, n):
		return "{}.{}".format(h.ISIN, n)

	graphite.send(fmt(holding, "pieces"), holding.pieces)
	graphite.send(fmt(holding, "acquisitionprice"), holding.acquisitionprice)
	graphite.send(fmt(holding, "total_value"), holding.total_value)
	graphite.send(fmt(holding, "market_value"), holding.market_value)

def send_holdings(graphite, holdings):
	for holding in holdings:
		send_holding(graphite, holding)

def main(config):
	c = get_client(config)
	g = get_graphite(config)
	h = get_holdings(c)
	print_holdings(h)
	send_holdings(g, h)

if __name__ == "__main__":
	main(config)
