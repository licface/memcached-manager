import memcache

mc = memcache.Client(['127.0.0.1:11211'], debug=0)
result = mc.get("Test_Key_1")
print "Get: Test_Key_1 - ", result

result = mc.get("Test_Key_2")
print "Get: Test_Key_2 - ", result

result = mc.get("Test_Key_3")
print "Get: Test_Key_3 - ", result

result = mc.get("Test_Key_4")
print "Get: Test_Key_4 - ", result

result = mc.get("Test_Key_5")
print "Get: Test_Key_5 - ", result

result = mc.get("Test_Key_6")
print "Get: Test_Key_6 - ", result

result = mc.get("Test_Key_7")
print "Get: Test_Key_7 - ", result

result = mc.get("Test_Key_8")
print "Get: Test_Key_8 - ", result