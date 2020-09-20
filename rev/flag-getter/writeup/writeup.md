The provided APK is a simple, but heavily obfuscated app that makes some requests to a server to get the flag. Static analysis and trying to deobfuscate everything would probably be too tedious. We can set up a man-in-the-middle proxy to intercept the requests and investigate. Unfortunately, the app makes requests to a HTTP server with TLS, and has certificate pinning implemented. We can patch the apk to disable the certificate pinning (or use some tools to do this automatically), then set up a mitm proxy to intercept the HTTP requests.

### Disabling Certificate Pinning

We start by decoding the apk with `apktool`

```
$ apktool d flag-getter.apk
```

This creates a directory with the app resources and smali code. We can find the code responsible for handling the certificate pinning logic using `grep`

```
$ grep -r certificate
e/j0/d/f.smali:    const-string v0, " not verified:\n              |    certificate: "
e/j0/d/f.smali:    const-string p3, " not verified (no certificates)"
e/h.smali:    const-string v2, "\n  Peer certificate chain:"
e/h.smali:    const-string p2, "\n  Pinned certificates for "
```

Looking in `h.smali`, we see that the method responsible for certificate pinning is defined in lines 171-699.

```
# virtual methods
.method public final a(Ljava/lang/String;Ljava/util/List;)V
    .locals 13
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "(",
            "Ljava/lang/String;",
            "Ljava/util/List<",
            "+",
            "Ljava/security/cert/Certificate;",
            ">;)V"
        }
    .end annotation

    if-eqz p1, :cond_14

    if-eqz p2, :cond_13

    .line 1
    sget-object v0, Ld/f/i;->a:Ld/f/i;
...
```

Adding `return-void` at the start of the method definition will disable the certificate pinning.

### Rebuilding the APK

Now that certificate pinning is disabled, we rebuild and sign the APK.

```
$ apktool b flag-getter -o patched-flag-getter.apk
I: Using Apktool 2.4.1
I: Checking whether sources has changed...
I: Smaling smali folder into classes.dex...
I: Checking whether resources has changed...
I: Building resources...
I: Copying libs... (/kotlin)
I: Building apk file...
I: Copying unknown files/dir...
I: Built apk...

$ keytool -genkey -v -keystore ks -keyalg RSA -keysize 2048 -validity 10000 -alias asdf
Enter keystore password:
Re-enter new password:
What is your first and last name?
  [Unknown]:
What is the name of your organizational unit?
  [Unknown]:
What is the name of your organization?
  [Unknown]:
What is the name of your City or Locality?
  [Unknown]:
What is the name of your State or Province?
  [Unknown]:
What is the two-letter country code for this unit?
  [Unknown]:
Is CN=Unknown, OU=Unknown, O=Unknown, L=Unknown, ST=Unknown, C=Unknown correct?
  [no]: yes

Generating 2,048 bit RSA key pair and self-signed certificate (SHA256withRSA) with a validity of 10,000 days
	for: CN=Unknown, OU=Unknown, O=Unknown, L=Unknown, ST=Unknown, C=Unknown
[Storing ks]

$ jarsigner -sigalg SHA1withRSA -digestalg SHA1 -keystore ks patched-flag-getter.apk asdf
Enter Passphrase for keystore:
jar signed.

Warning:
The signer's certificate is self-signed.

$ adb install patched-flag-getter.apk
Performing Push Install
patched-flag-getter.apk: 1 file pushed, 0 skipped. 448.6 MB/s (1224910 bytes in 0.003s)
	pkg: /data/local/tmp/patched-flag-getter.apk
Success
```

### Intercepting Requests

I used an Android emulator (running Android 5.1.1) and [mitmproxy](https://mitmproxy.org/) but other tools work too. The first thing we'll need to do is get the CA certificate onto the device. For mitmproxy, the generated certificates will be at `~/.mitmproxy`. Android stores CA certs in `/system/etc/security/cacerts/`. You could also install the cert via the Android settings for Android 6 and below.

```bash
$ cd ~/.mitmproxy

$ openssl x509 -inform PEM -subject_hash_old -in mitmproxy-ca-cert.cer | head -n 1
c8750f0d

$ cp mitmproxy-ca-cert.cer c8750f0d.0

$ adb shell 'mount -o rw,remount /system'

$ adb push c8750f0d.0 /system/etc/security/cacerts
c8750f0d.0: 1 file pushed, 0 skipped. 10.9 MB/s (1318 bytes in 0.000s)
```

Now all we need to do is change the emulator's settings to use the proxy, then start the proxy. Opening the patched app and pressing the buttons will show the requests in the proxy interface, and their responses contain the flag.
