# Robotssss
**Category:** Web
**Difficulty:** Medium
**Author:** donfran

## Flavourtext
Us robot devs use better templates than those stupid humans! https://chal.duc.tf:30106

## Description
The application has a forum with a few post written by some robots which contains helpful information that leads to the user discovering the admin's credentials.

Chaining multiple vulnerabilties (detailed in the writeup section) eventually leads to server side template injection which then uses a function to read the **fl4g.txt** file.

## Writeup

1. Create an account using the register function.
2. Read the two blog post given.
3. Check the source for both blog post and notice the <noscript> tags that contains some binary numbers.
4. Change the binary to ascii (UTF-8) and we find get some more information: the flag file is fl4g.txt and there is a path called /humen.txt.
5. Go to humen.txt and find 3 new paths.
6. Download the bender.jpeg image from /Bender and use exiftools to view the information.
7. Notice the "Artist" section has a base58 encoded string which is the real admin cred.
8. Login in as the admin.
9. We are taken to admin.php, which has an input field where we can type things and it "repeats" it back to us.
10. Try {{ 7*7 }} and we get 49. This means we got server side template injection for jinja2.
11. Dump the config for our flask by doing {{ config.items() }}.
12. In the config items, notice that the secret key is a hint on a function we can use.
13. Type {{ getFile("/fl4g.txt") }} to get the flag.

## Running
Running `docker-compose up` should be enough to build the challenge and deploy it on port 5000.

All models have been built locally and pushed. The models are very small so this is not a issue. If models need to be rebuilt this can be done with `./build.sh`.
