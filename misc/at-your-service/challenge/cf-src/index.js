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