import memcache

mc = memcache.Client(['127.0.0.1:11211','127.0.0.1:11212'], debug=0)

for i in range(1,100000):
    result = mc.set("Test_Key_"+ str(i), "Test_Key_"+ str(i) +"_Value")
    #print "Set: Test_Key_"+ str(i) +"- ", result