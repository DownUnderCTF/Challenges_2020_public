
const {Storage} = require('@google-cloud/storage');
const storage = new Storage();

exports.getListOfMemes = async (bucketName) => {
    let [files] = await storage.bucket(bucketName).getFiles();
    files = files.map(file => file.name)
    return files;
}

exports.getMeme = async (bucketName, objectName) => {
    await storage.bucket(bucketName).file(objectName).download(options);

}


exports.generateSignedURL = async (bucketName, objectName) => {
    const options = {
        version: 'v4', // defaults to 'v2' if missing.
        action: 'read',
        expires: Date.now() + 1000 * 60 * 60, // one hour
      };

      const [url] = await storage.bucket(bucketName).file(objectName).getSignedUrl(options);

      return url;
}