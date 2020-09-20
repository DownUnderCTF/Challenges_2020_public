# WRITEUP

---

In the challenge the user is given a simulated capture of a suspect's pc files. Among the directories are miscellaneous files. However there are 2 primary directories of importance, one called `badFiles` and another secret directory called `.config`.

The primary folder is `badfiles`, as Indicated by the name, this is where the suspect is keeping the evidence. The evidence resides within a JPEG file, in order for the player to retrieve it, they have to use `steghide`, find the password, and extract the flag.

However, the JPEG file that holds the evidence, is hidden among 200 other JPEG images. This therefore forces the player to use bash scripting to process all the files. Every other JPEG image that does not contain the flag, Is embedded using the pass phrase: `password`, has another message embedded within, that simply says "Here's a tip, try harder". If the player uses a tool like stegcracker to try and brute force files, the only files that will extracted are the dummy files due to this weak password.

In order to find the password that will differentiate the correct JPEG from the others, the player has to venture into the `.config` directory. Within this is a PNG file → `Reminder.png` and a directory called `secret`. Within the `secret` directory, are 40 subdirectories, Each of which contains 40 `.txt` files. Each of these text files has a random base 64 encoded string. However there is one base 64 encoded string that when decoded reveals the password for the JPEG image embedded with the evidence in the `badfiles` directory.

This is where `reminder.png` comes in. When viewed, this image will show a partial string of the base 64 encoded password for the JPEG image holding the evidence. However, the suspect has used counter forensics to modify the header Hex values so that it cannot be viewed. Using the file command will show that the image seems to be a zip file. This means that the header of the file is identical to that of a `.zip` file. However the extension is left as `.png`. 

Thus inspection of the Hex header values such as using a tool like `xxd` will show the improper header. The player must realise this is meant to be a `.png` file, and thus use a program like `Hxd` Or any preferred hex value file editor to change the values back. Once changed back, the player will be able to view the `.png` file.

The player must realise that the tool like `grep` can be used to filter through the strings in text files. Using the recursive option `grep -r`, they can search the entire secret directory and obtain the base 64 encoded string for the password. The base 64 encoded string they are looking for is:

```bash
CjEyMzRJc0FTZWN1cmVQYXNzd29yZA==
```

when decoded, becomes

```bash
 1234IsASecurePassword
```

At this point, the player has all the need to complete their batch script. Then they simply have to use their bash script to iterate over every file in the `badfiles` directory Using the steghide tool in extraction mode, and the password as the parameter. Once extracted, they simply have to view the file and they will have the flag!

```bash
Flag: DUCTF{m0r3_th4n_M33ts_th3_ey3}
```