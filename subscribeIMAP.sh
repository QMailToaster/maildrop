#!/bin/sh
#
# $Id: subscribeIMAP.sh,v 1.2 2004/02/18 15:54:44 matt Exp $
#
# This subscribes the folder passed as $1 to courier imap
# so that IMAP clients (including some webmail programs like
# Mailman and Squirrelmail) will recognize the extra folder.
#
# Matt Simerson - 12 June 2003
# Eric Shubert - 13 Nov 2013 - Modified for dovecot

LIST="$2/Maildir/subscriptions"

if [ -f "$LIST" ]; then
  # if the file exists, check it for the new folder
  TEST=`cat "$LIST" | grep "$1"`
  # if it is not there, add it
  if [ "$TEST" == "" ]; then
    echo "$1" >> $LIST
  fi
else
  # the file does not exist so we define the full list
  # and then create the file.
  FULL="INBOX\nSent\nTrash\nDrafts\nINBOX.$1"
  echo -e $FULL > $LIST
  /bin/chown vpopmail:vchkpw $LIST
  /bin/chmod 644 $LIST
fi
