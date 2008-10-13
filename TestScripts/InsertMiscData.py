import memcache

mc = memcache.Client(['127.0.0.1:11211'], debug=0)
result = mc.set("Test_Key_1", "Test_Key_1_Value")
print "Set: Test_Key_1 - ", result

result = mc.set("Test_Key_2", "Test_Key_2_Value")
print "Set: Test_Key_2 - ", result

result = mc.set("Test_Key_3", "Test_Key_3_Value")
print "Set: Test_Key_3 - ", result

result = mc.set("Test_Key_4", "Test_Key_4_Value")
print "Set: Test_Key_4 - ", result

result = mc.set("Test_Key_5", "Test_Key_5_Value")
print "Set: Test_Key_5 - ", result

result = mc.set("Test_Key_6", "Test_Key_6_Value")
print "Set: Test_Key_6 - ", result

result = mc.set("Test_Key_7", "Test_Key_7_Value")
print "Set: Test_Key_7 - ", result

result = mc.set("Test_Key_8", "Test_Key_8_Value")
print "Set: Test_Key_8 - ", result