# Comix publisher

Script for posting random xkcd comix to your vk.com group


## How to install

Python 3 has to be installed. You might have to run python3 instead of python depending on system if there is a conflict with Python2. Then use pip (or pip3) to install dependencies:

```commandline
pip install -r requirements.txt
```
You need to specify [AccessToken](https://vk.com/dev/implicit_flow_user) and [GroupID](http://regvk.com/id/) in .env file.

Run `python main.py`. Downloaded image are saved as `comix.png` to the same directory where script run. It will be deleted after uploading.


## Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).
