# Taking Stock
**Category:** Web
**Difficulty:** Medium/Hard
**Author:** todo#7331

_After taking one unit of AI at uni I'm now a pro. My linear regression model is amazing at predicting the stock market. I'm so proud of it I'm even offering it as a service. Can't wait to get that VC money!_

## Description
The application allows users to use AI models in order to predict the future stock prices of a
given stock. The application also exposes functionality to upload profile pictures.

A series of bugs (detailed in the writeup section) are leveraged in order to gain remote code execution and cat
a flag file.

## Writeup
_A solve script can be found in solve/solve.py_

1. We notice that the /profile-picture/uuid leaks the location where profile pictures are stored (namely /tmp)
2. Can can retrieve our uuid either by hitting the profile endpoint and noticing what uuid is specified in the profile-picture img or by decoding our session id.
3. We can then upload malicious files as our profile picture as only the file extension of the uploaded file is checked
4. We notice there is a directory traversal on model selection. I.e. sending a request to predict prices for the stock `../../../../../../../etc/passwd` results in errors.
5. We can then upload a malicious joblib serialized model as our profile picture and load it with the path traversal vulnerability
6. This can lead to RCE.
7. At this point there are a variety of ways to exfiltrate the data. For example, one could pipe the result of the command back into their profile picture and request it from there.

## Running
Running `docker-compose up` should be enough to build the challenge and deploy it on port 3000.

All models have been built locally and pushed. The models are very small so this is not a issue. If models need to be rebuilt this can be done with `./build.sh`.
