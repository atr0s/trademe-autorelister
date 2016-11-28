#!/usr/bin/python
from trademe import *
import creds


a = TrademeApiConnection('https://api.tmsandbox.co.nz/v1',creds.oauthcreds)
t = MyTradeMe(a)

print "Items currently on sale:",len(t.sellingItems())
print "Items under offer:",len(t.unsoldItems('ItemsIHaveOffered'))

for item in t.unsoldItems('ItemsICanRelist',{'deleted':'false','photo_size':'Thumbnail'}):
  if item.BidderAndWatchers > 0 and item.PendingOffer == False:
    if item.offer(item.StartPrice,1):
      print "Offering item '%s (%i)' for $%.2f for 1 day" % (item.Title,item.ListingId,item.StartPrice)
    else:
      r = item.quickRelist()
      print "Relisting item '%s' new listing id is %i" % (item.Title,r.ListingId)
  else:
    r = item.quickRelist()
    if r != False:
      print "Relisting item '%s' new listing id is %i" % (item.Title,r.ListingId)
    else:
      print "Something went wrong relisting %s" % (item.ListingId)
     
