#!/usr/bin/python
import requests
import json
import sys
from requests_oauthlib import OAuth1
import urllib

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
      if 'Watchers' in r:
          return list(member for member in r['Watchers']) if self.BidderAndWatchers > 0 else []
      else:
          return []

  def offer(self,price,offerDuration=1):
    postdata = {
     'ListingId': self.ListingId,
     'Price': price,
     'Duration': offerDuration,
     'MemberIds': list(Watcher['MemberId'] for Watcher in self.BidderAndWatchersList) 
    }
    r = self.apiConnection.post("/FixedPriceOffers/MakeOffer.json",json.dumps(postdata))
    return False if r['Success'] == False else len(postdata['MemberIds']) 

  def quickRelist(self):
    postdata = {
      'ListingId': self.ListingId,
      'ReturnListingDetails': True
    }
    r = self.apiConnection.post("/Selling/Relist.json",json.dumps(postdata))
    if not r['Success']:
      return False
    return r if r == False else TrademeItem(self.apiConnection,r['ListingId']) 

class MyTradeMe:

  def __init__(self,apiConnection):
    self.apiConnection=apiConnection

  def unsoldItems(self,searchFilter="Last45Days",qs={'deleted':'false','photo_size':'Thumbnail'}):
    items = []
    queryString = urllib.urlencode(qs)
    r = self.apiConnection.get('/MyTradeMe/UnsoldItems/%s.json?%s' % (searchFilter,queryString))
    items = list(TrademeItem(self.apiConnection,item['ListingId']) for item in r['List']) 
    return items 

  def sellingItems(self,searchFilter="All",qs={}):
    items = []
    queryString = urllib.urlencode(qs)
    r = self.apiConnection.get("/MyTradeMe/SellingItems/%s.json?%s" % (searchFilter,queryString))
    items = list(TrademeItem(self.apiConnection,item['ListingId']) for item in r['List'])
    return items 

  def soldItems(self,searchFilter="Last45Days",qs={}):
    items = []
    queryString = urllib.urlencode(qs)
    r = self.apiConnection.get("/MyTradeMe/SellingItems/%s.json?%s" % (searchFilter,queryString))
    items = list(TrademeItem(self.apiConnection,item['ListingId']) for item in r['List'])
    return items 
