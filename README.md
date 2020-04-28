
# APKEnum: A Python Utility For APK Enumeration

The utility takes APK file as an input, performs reverse engineering and gathers information from the decompiled binary. As of now, the script provides the following information by searching the decompiled code:

* List of domains in the application

* List of S3 buckets referenced in the code

* List of S3 websites referenced in the code

* List of IP addresses referenced in the code

Once downloaded, we just need to provide the pathname of the APK file. Optionally, we can also provide a list of keywords related to the target, the script would then create an additional list of in-scope domains based on the input keyword list apart from the aforementioned lists.

![](https://cdn-images-1.medium.com/max/3448/1*2e5i-_GDljBNRDOYdEscaA.png)

To have a look at the quick wakkthrough of APKEnum read [this](https://medium.com/@shivsahni2/apkenum-a-python-utility-for-apk-enumeration-cce0eda6fa30).

**Would appreciate bugs, suggestions and contributions from your end**
