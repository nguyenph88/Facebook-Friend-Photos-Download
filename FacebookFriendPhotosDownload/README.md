# Facebook Friend's Photos Download

[![N|Solid](https://cldup.com/dTxpPi9lDf.thumb.png)](https://nodesource.com/products/nsolid)

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

FFPD is a simple script that allows you to download all photos from your friend's albums.

# New Features

  - You can download photos from either Page or User
  - Each download will be saved in separated folder

### How to use
First, install `FFPD` with `pip`:  
```bash
$ pip install FacebookFriendPhotosDownload
```  

Then refert to the example.py as below:

**Example code**  

```python
from FacebookFriendPhotosDownload import FFPD

bot = FFPD(token=your_facebook_token, user_id=user_of_of_your_friends_account)
```


License
----

MIT

