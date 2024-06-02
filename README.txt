*** PROOF OF CONCEPT // READ LEGAL STATEMENT // STRICTLY FOR EDUCATIONAL USE ***

This repository houses two files.

    rware.py --- The ransomware itself 
    cure.py ---- The decryptor tool

################
# How it works #
################
    INDEXING
    1) Rware indexes all files held in common user-directories (Desktop, Videos, Music, Downloads, Documents, 
       and Pictures) and add them to a list
    2) Next a local Fernet encryption key is generated and written into the working directory of Rware

    SORTING / LOCKING
    3) Rware iterates through/encrypts each indexed file. If a file-extension is part of the blacklist (pre-set
       by the attacker) the file is skipped. This helps avoid unnecessary files that yield no benefit to lock.
    4) After encryption, files are then renamed to have a .lock file-extension. This ensures Rware won't overwrite
       the same file upon next reboot.

    EXFILTRATION
    5) Once all files have been locked, a sub-routine then creates a message containing: the encryption key, a
       custom user-ID and the account name (used for C2 indentification), network IP address, and the timestamp
       of the encryption. This entire message is then sent to the pre-set Discord webhook. The local Fernet
       encryption key is now deleted.

    NOTIFICATION
    6) A primivite HTML notification is constructed in the /tmp directory and then opened up in the victim's
       default web browser. The message explains what has happened, how to pay for the decryption software,
       etc.

    PERSISTENCE
    7) Finally, the Rware script is written to the local CronTab for system persistence. It will run each time
       the machine reboots.

    THE CURE
    8) The cure works similarly. Upon payment, the victim is instructed to email the attacker with the crypto
       transaction ID and their UID. The attacker looks up UID and locates the encryption key(s) used. Each reboot
       will produce its own new encryption key and pass it to the web hook. The encryption keys need manually added
       to the list in cure.py. The cure.py script does everything in reverse. Indexes all .lock files this time, and
       overwrites the files with their decrypted content. It also removes the .lock file-extension and resets the
       file to the original name.

##############
# Known bugs #
##############

    Although I've spent several hours trying to figure this out through trial/error (and not like it matters much
    since this is a POC and not a script that should be used seriously in the field) Rware often skips a file every
    now and then, even though said files were all found in the indexing list. No errors are raised, and I assume
    somewhere around line #159 things aren't working smoothely. Since Rware is persistent, it gets the rest sooner
    or later. If you've found a fix, please reach out. 

###############
# Life advice #
###############

    In addition to the legal statement, don't be a douche with this. Use it responsibly and never to commit
    final crime / extortion. 
