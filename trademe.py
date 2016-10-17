#!/usr/bin/python
import requests
import json
import sys
from requests_oauthlib import OAuth1

class TrademeApiConnection:
  def __init__(self,apiUrl,oAuthCredentials,cache=True):
      self.apiUrl=apiUrl
      self.auth=OAuth1(**oAuthCredentials)
      self.headers = { 'Content-Type': 'application/json' }

  def get(self,apiPath):
    url = self.apiUrl + apiPath
    r = requests.get(url,auth=self.auth,headers=self.headers)
    return False if r.status_code != 200 else r.json()
    
  def post(self,apiPath,postData):  
    url = self.apiUrl + apiPath
    r = requests.post(url,data=postData,auth=self.auth,headers=self.headers)
    return False if r.status_code != 200 else r.json()
      

class TrademeItem(object):
  canOffer = False
  PendingOffer = False
  def __init__(self,apiConnection,itemId):
    self.apiConnection = apiConnection
    self.BidderAndWatchers = 0
    item = self.apiConnection.get("/Listings/%s.json" % (itemId))
    for key in item:      
      setattr(self,key,item[key])
    
    self.BidderAndWatchersList = self.fixedOfferMembers()

  def fixedOfferMembers(self):
      r = self.apiConnection.get("/FixedPriceOffers/%s/Members/All.json" % (self.ListingId))
      return list(member for member in r['Watchers']) if self.BidderAndWatchers > 0 else []

  def offer(self,price,offerDuration=1):
    postdata = {
     'ListingId': self.ListingId,
     'Price': price,
     'Duration': offerDuration,
     'MemberIds': list(Watcher['MemberId'] for Watcher in self.BidderAndWatchersList) 
    }
    r = self.apiConnection.post("/FixedPriceOffers/MakeOffer.json",json.dumps(postdata))
    return r if r == False else len(postdata['MemberIds']) 

  def quickRelist(self):
    postdata = {
      'ListingId': self.ListingId,
      'ReturnListingDetails': True
    }
    r = self.apiConnection.post("/Selling/Relist.json",json.dumps(postdata))
    return r if r == False else TrademeItem(self.apiConnection,r['ListingId']) 

class MyTradeMe:

  def __init__(self,apiConnection):
    self.apiConnection=apiConnection

    
  def unsoldItems(self,searchFilter="Last45Days"):
    items = []
    r = self.apiConnection.get('/MyTradeMe/UnsoldItems/%s.json?deleted=false&photo_size=Thumbnail' % (searchFilter))
    items = list(TrademeItem(self.apiConnection,item['ListingId']) for item in r['List']) 
    return items 
  def sellingItems(self,searchFilter="All"):
    items = []
    r = self.apiConnection.get("/MyTradeMe/SellingItems/%s.json" % (searchFilter))
    items = list(TrademeItem(self.apiConnection,item['ListingId']) for item in r['List'])
    return items 

