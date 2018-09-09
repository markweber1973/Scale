import _readcount
import urllib2
import time
import datetime
from collections import deque
import picamera

urlOnlyString = "https://api.thingspeak.com/update?api_key="
apiKeyData = "8ZI7Q0MYFLNP9P3D"

sampleInterval  = 1
uploadInterval  = 15
previousCount   = 0
currentCount    = 0
weightThreshold = 5
sampleCounter   = 0
rawValues       = deque()
filterSize       = 5
nothingChangedValue = ""
birdIn          = 0
initialRun      = True
spikeCount      = 0
visits          = 0
camera = picamera.PiCamera()
secondsinbox    = 0
timeofenteringbox = datetime.datetime.now()

def createdAtString():
  return ("&created_at=" + datetime.datetime.now().isoformat() )

def countToWeigth(x):
  return ((x /100 )- 79445) * (145.2 / 2970)

def upload(x):
  fullUrl = urlOnlyString + apiKeyData + x
  print "Uploading: " + fullUrl
  try: urllib2.urlopen( fullUrl ).read()
  except:
    print "Upload failed"
    return False
  print "Upload succeeded "
  return True

def resultString(x, y, z, a, t):
  return ("&field1=" + str(countToWeigth(x)) + "&field2=" + str(y) + "&field3=" + str(z) + "&field4=" + str(a) + "&field5=" + str(t) + createdAtString())

def readFilteredValue():
  unfilteredValues = []
  for i in range (0, filterSize):   
    unfilteredValues.append(_readcount.readcount())
    time.sleep(0.1)  
  max = 0
  min = 999999999

  for value in unfilteredValues:   
    if (value > max ):
      max = value 
    if (value < min ):
      min = value 

  unfilteredValues.remove(max)
  unfilteredValues.remove(min)
  
  sum = 0
  for value in unfilteredValues:
    sum = sum + value
  avg = 0
  avg = sum / (filterSize-2) 
  print "readFilteredValue: " + str(avg)
  print "max: " + str(max)
  print "min: " + str(min)
  return avg


condition = 1
while condition :
  while (sampleCounter < uploadInterval):
    currentCount = readFilteredValue()
    weightDiff = countToWeigth(currentCount) - countToWeigth(previousCount)
    if (abs(weightDiff) > weightThreshold):      
      time.sleep(1)
      weightDiff = countToWeigth(readFilteredValue()) - countToWeigth(previousCount)
      if (abs(weightDiff) > weightThreshold):
        print "Dubbelcheck confirmed"
        if (weightDiff > 0):
          if (birdIn == 0):
            timeofenteringbox = datetime.datetime.now()
            visits = visits + 1
            camera.capture("visit" + str(visits) + "_" + datetime.datetime.now().isoformat() + ".jpg")
          birdIn = 1
        else:
          birdIn = 0
          secondsinbox = secondsinbox + (datetime.datetime.now() - timeofenteringbox).seconds
        rawValues.append(resultString(currentCount, birdIn, currentCount, visits, secondsinbox))
        previousCount = currentCount
        print "Change detected"
      else:
        nothingChangedValue = resultString(currentCount, birdIn, currentCount, visits, secondsinbox)
        print "No change detected"
    else:
      nothingChangedValue = resultString(currentCount, birdIn, currentCount, visits, secondsinbox)
      print "No change detected"

    sampleCounter = sampleCounter+1
    time.sleep(1)  

  previousCount = currentCount
  sampleCounter = 0
  initialRun = False

  if (len(rawValues) > 0):
    print "Changes detected: " + str(len(rawValues))
    leftEntry = rawValues.popleft()    
    print "Trying to upload: " + leftEntry    
    if upload(leftEntry):
      print "Upload change succeeded, nr of changes left to upload: " + str(len(rawValues))
    else:
      print "Failed to upload, putting it back: " + leftEntry
      rawValues.appendleft(leftEntry)

  else:
    if upload(nothingChangedValue):
      print "Uploaded nothingChangedValue"
    else:
      print "Queue nothingChangedValue"
      rawValues.appendleft(nothingChangedValue)
      print "Failed to upload 'nothing changed', putting it back: " + leftEntry
       


