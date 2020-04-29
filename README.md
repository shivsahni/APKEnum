# APKEnum: Passive Enumeration Utility For Android Applications

[![https://www.python.org/static/community_logos/python-logo.png](https://www.python.org/static/community_logos/python-logo.png)


## Installation
### Prerequisites
- Support For Python 2.7
- APKTool JAR


**Note:**  The latest APKTool(v2.4.1) JAR file is already shipped with the package. In case you face decompilation issues, you can download the latest version from [here](https://bitbucket.org/iBotPeaches/apktool/downloads/) and place it in the Dependency directory with name *apktool.jar*

### Walkthrough
To have a look at the quick walkthrough of APKEnum have a look at [this](https://medium.com/@shivsahni2/apkenum-a-python-utility-for-apk-enumeration-cce0eda6fa30) Medium story.

## Usage
The utility takes APK file as an input, performs reverse engineering and gathers information from the decompiled binary. As of now, the script provides the following information by searching the decompiled code:

* List of domains in the application

* List of S3 buckets referenced in the code

* List of S3 websites referenced in the code

* List of IP addresses referenced in the code

![](https://cdn-images-1.medium.com/max/3448/1*2e5i-_GDljBNRDOYdEscaA.png)

Once downloaded, you just need to provide the pathname of the APK file as shown below:

```
python APKEnum.py -p ~/Downloads/app-debug.apk
```

Optionally, we can also provide a list of keywords related to the target, the script would then create an additional list of in-scope domains based on the input keyword list apart from the aforementioned lists by performing string match. 

```
python APKEnum.py ~/Downloads/app-debug.apk -s "shiv,sahni,alpha,charlie,example"
```