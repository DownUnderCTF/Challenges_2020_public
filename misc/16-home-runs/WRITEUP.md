# 16 home runs
## Author: Crem

16 home runs is a basic base64 challenge. You need to first identify that the string provided is a base64 string. You can identify that is a base64 string by the equals sign at the end of the string.

Once, we identified that it is a base64 string. you can run the following command in a linux terminal and once executed will return the flag:
`echo 'RFVDVEZ7MTZfaDBtM19ydW41X20zNG41X3J1bm4xbjZfcDQ1N182NF9iNDUzNX0=' | base64 -d`

Alteratively, you can go to an online base64 decoder like CyberChef and it will also return the flag!