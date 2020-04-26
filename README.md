
# APKEnum: A Python Utility For APK Enumeration


**Reconnaissance** is indeed the most critical and time-consuming phase of a penetration test. In this phase, we collect as much information as possible about the target. The more information we have, the more are the chances of successful exploitation. 

Over the past few years, I have had multiple experiences where the mobile front of applications are missing the fundamental security practices whereas corresponding web applications are far more robust. This is definitely an area of opportunity for red teamers, penetration tester and bug bounty hunters wherein they could identify some cool security issues. 

With all that in mind and COVID-19 lockdown, I thought of brushing up my scripting skills to come up with a **passive enumeration utility** for Android applications. The script takes APK file as an input, performs reverse engineering and gathers information from the decompiled binary. As of now, the script provides the following information by searching the decompiled code:

* List of domains in the application

* List of S3 buckets referenced in the code

* List of S3 websites referenced in the code

* List of IP addresses referenced in the. code

I wrote this story to walk you through the script. It is open source and can be easily download from [here](https://github.com/shivsahni/APKEnum). 

As shown below, once downloaded, we just need to provide the pathname of the APK file. Optionally, we can also provide a list of keywords related to the target, the script would then create an additional list of in-scope domains based on the input keyword list apart from the aforementioned lists.

![](https://cdn-images-1.medium.com/max/3448/1*2e5i-_GDljBNRDOYdEscaA.png)

To test this out, I created a sample application with the following test data and executed APKEnum on the sample app.

![](https://cdn-images-1.medium.com/max/2096/1*roTCfcNhX8satg05m1hMPw.png)

The following screenshots show the results for the sample application

![](https://cdn-images-1.medium.com/max/3452/1*4hfhqYxOaYUboAp5bBCFrA.png)

![](https://cdn-images-1.medium.com/max/3452/1*sFXM2xs3C118aWYcZyJDuA.png)

Would appreciate bugs, suggestions and contributions from your end. 

Github Repo: [https://github.com/shivsahni/APKEnum](https://github.com/shivsahni/APKEnum)




