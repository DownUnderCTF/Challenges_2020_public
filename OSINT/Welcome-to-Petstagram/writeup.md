# Writeup

> **Welcome to Petstagram**
>
> Who is Alexandros the cat exactly? And who is this mysterious "mum" he keeps talking about?
>
> Submit his mum's full name in lowercase and with underscores instead of spaces, as the flag.
>
>
> **Category:** OSINT
>
> **Difficulty level:** Beginner
>
> **Author:** dahlia
>

## Solution

In the challenge description and title, you are given three data points:
- Persons of Interest:
  - Alexandros the cat
  - Alexandros' "mum"
- A location to search:
  - Petstagram

The use of "Petstagram" gives a hint that we are looking for an Instagram account.

Searching "alexandrosthecat" or "alexandros the cat" on Instagram leads you to: [alexandrosthecat](https://www.instagram.com/alexandrosthecat/)\
Next, Alexandros' first follower is an account owned by "Emily Waters": [emwaters92](https://www.instagram.com/emwaters92/)

An examination of this Instagram account shows that it includes an image of Alexandros, and that the bio (description) on Emily's profile includes her email address: `emilytwaters92@gmail.com`\
Emily Waters also has a middle name, as indicated by the 't' in her email address, and it is needed for the flag which asks for her *full* name.

The description of the second post on Alexandros' profile contains a shortened link to a YouTube channel: `bit.ly/3h3e7A0`\
Searching up the username of the YouTube channel `gelato_elgato` using a username search site will show that it is also taken on twitter.

Visiting this twitter page [gelato_elgato](https://twitter.com/gelato_elgato) you can identify it is owned by Emily with the description "love gelato and my cat alexandros 🤩".\
The twitter account can further be confirmed as her account by searching for tweets mentioning her username, where a [tweet](https://twitter.com/lovejenn1fer/status/1303201839731453952?s=20) from an account @lovejenn1fer can be found: "Emily Waters this is your account, right?". If you hadn't discovered her first and last name at this point, this might be where you do so.

If you have not yet located her Instagram account before finding her twitter, a google dork with relevant information based on her twitter profile e.g. 'site:instagram.com "alexandros" "cat" "gelato"' with return her Instagram account.

Her name on twitter is "call me theresa", and in conjunction with the Gmail address emily ***t*** waters you can assume that *maybe* this is her middle name.\
Further confirmation of her middle name can be found by sending an email Emily at her Gmail address, where an out of office auto reply will include her full name:

> Hello,
>
> I will be out of the office from Sunday, September 6th onward.
>
> If you need immediate assistance during my absence, that sounds like a you problem. Otherwise, I will probably respond to your emails as soon as possible if I return.
>
> Kind Regards,
>
> Emily Theresa Waters.
>
> P.S. I recently made Alexandros an Instagram account. https://www.Instagram.com/alexandrosthecat/. Please go check it out and give a follow.

Full name: Emily Theresa Waters

Flag: `DUCTF{emily_theresa_waters}`
