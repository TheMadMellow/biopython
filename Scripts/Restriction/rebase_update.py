#!/usr/bin/env python
#
#      Restriction Analysis Libraries.
#      Copyright (C) 2004. Frederic Sohm.
#
# This code is part of the Biopython distribution and governed by its
# license.  Please see the LICENSE file that should have been included
# as part of this package.
#

"""Update the Rebase emboss files.

These are used by Restriction to build the Restriction_Dictionary.py module.
"""

from __future__ import print_function

import os
import sys
import time
import optparse


try:
    from urllib import FancyURLopener
except ImportError:
    # Python 3
    from urllib.request import FancyURLopener

from Bio.Restriction.RanaConfig import ftp_proxy, ftp_Rebase, Rebase_name
from Bio.Restriction.RanaConfig import ftp_emb_e, ftp_emb_s, ftp_emb_r


class RebaseUpdate(FancyURLopener):

    def __init__(self, ftpproxy=''):
        """RebaseUpdate([ftpproxy]]) -> new RebaseUpdate instance.

        if ftpproxy is not given RebaseUpdate uses the corresponding
        variable from RanaConfig.

        ftpproxy is the proxy to use if any.
        """
        proxy = {'ftp': ftpproxy or ftp_proxy}
        if not Rebase_name:
            raise FtpNameError('Rebase')
        if not proxy['ftp']:
            proxy = {}
        FancyURLopener.__init__(self, proxy)

    def openRebase(self, name=ftp_Rebase):
        print('\n Please wait, trying to connect to Rebase\n')
        try:
            self.open(name)
        except:
            raise ConnectionError('Rebase')
        return

    def getfiles(self, *files):
        for file in self.update(*files):
            print('copying %s' % file)
            fn = os.path.basename(file)
            # filename = os.path.join(Rebase, fn)
            filename = os.path.join(os.getcwd(), fn)
            print('to %s' % filename)
            self.retrieve(file, filename)
        self.close()
        return

    def localtime(self):
        t = time.gmtime()
        year = str(t.tm_year)[-1]
        month = str(t.tm_mon)
        if len(month) == 1:
            month = '0' + month
        return year + month

    def update(self, *files):
        if not files:
            files = [ftp_emb_e, ftp_emb_s, ftp_emb_r]
        return [x.replace('###', self.localtime()) for x in files]

    def __del__(self):
        if hasattr(self, 'tmpcache'):
            self.close()
        #
        #   self.tmpcache is created by URLopener.__init__ method.
        #
        return


class FtpNameError(ValueError):

    def __init__(self, which_server):
        print(" In order to connect to %s ftp server, you must provide a name.\
        \n Please edit Bio.Restriction.RanaConfig\n" % which_server)
        sys.exit()


class ConnectionError(IOError):

    def __init__(self, which_server):
        print('\
        \n Unable to connect to the %s ftp server, make sure your computer\
        \n is connected to the internet and that you have correctly configured\
        \n the ftp proxy.\
        \n Use the --proxy switch to enter the address of your proxy\
        \n' % which_server)
        sys.exit()


if __name__ == '__main__':
    parser = optparse.OptionParser()
    add = parser.add_option

    add('-p', '--proxy',
        action="store",
        dest='ftp_proxy',
        default='',
        help="set the proxy to be used by the ftp connection.")

    (option, args) = parser.parse_args()

    Getfiles = RebaseUpdate(option.ftp_proxy)
    Getfiles.openRebase()
    Getfiles.getfiles()
    Getfiles.close()
    sys.exit()
