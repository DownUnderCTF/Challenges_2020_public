# Writeup

You are given an image from the POV of a railcab, with the instruction to find the station shown in the image.

The first obviously identifiable object in the image is the train, when you zoom in on it you can kind of make out a logo.

If you put the image in a reverse image search engine (I recommend yandex here), and crop in on the train, similar trains will come up. If you click on one of the trains with the same logo and appearance that come up (https://rail.pictures/picture/7731), you'll discover that the train is a NSB Di 4 (or at least looks like one). 

Further research will reveal that this train only runs on a specific rail line in Norway, the Nordland Line.

Now you know which line you are on, you can start working on identifying the station.
The Nordland Line has 44 stations along its route from Trondheim to Bodø, so if you wanted you could just go through all the stations one by one until you located the one in the picture. However, we can make it easier on ourselves, by collecting information in the image to rule out some stops!

Identifying information:
- Red Building, two stories.
- Small red structure either a part of the red building or in front of it.
- Cream Building, one story.
- Two train lines.
- Small red structure near front of camera.
- Remote (no parking lots, or buildings visible other than the two noted).
- Up against mountains.
etc. etc.

Google maps unfortunately does not highlight railway maps and stations, however a useful tool I have found to do this is: https://www.openrailwaymap.org/

You can then follow along the train line, with each station highlighted in blue, ruling out each of them as you go along. Many of them are immediately obviously wrong without even zooming in due to location, and if not you can quickly zoom in to check and compare against the notes you have made earlier.

If you reach any stations that seem like a possibility then you can search them up in a search engine and get a better look.

Once you reach Dunderland Station, you can note it's remoteness, and upon zooming in that it has two train lines, with a structure on the left in the middle, and one on the right further back. Which all match the notes you took previously.

Searching up Dunderland Station in a search engine will reveal architecture very familiar to the picture, and if you drop yourself down nearby you can clearly see that this is the correct station. (If you want you can continue on and rule out all the others too).

*Alternatively Dunderland IS mentioned a couple of times on the Nordland Station wiki, so if you do it that way, you might luck out.

The flag is thus: DUCTF{dunderland}

Image in the challenge is a screencap from this video: https://www.youtube.com/watch?v=3rDjPLvOShM