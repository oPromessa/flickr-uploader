"""
    by oPromessa, 2017
    Published on https://github.com/oPromessa/flickr-uploader/

    Helper class and functions to print messages.
"""

# ----------------------------------------------------------------------------
# Import section for Python 2 and 3 compatible code
# from __future__ import absolute_import, division, print_function, unicode_literals
from __future__ import division    # This way: 3 / 2 == 1.5; 3 // 2 == 1

# ----------------------------------------------------------------------------
# Import section
#
import sys
import os
import logging
import time
from . import UPLDRConstants as UPLDRConstantsClass
UPLDRConstants = UPLDRConstantsClass.UPLDRConstants()

# -----------------------------------------------------------------------------
# class niceprint to be used to print messages.
#
class niceprint:
    """
        >>> import niceprint as npc
        >>> np = npc.niceprint()
        >>> np.isThisStringUnicode('Hello')
        False
        >>> np.isThisStringUnicode(u'With u prefix')
        True
    """
    # -------------------------------------------------------------------------
    # class niceprint __init__
    #
    def __init__(self):
        """ class niceprint __init__
        """
        pass

    # -------------------------------------------------------------------------
    # isThisStringUnicode
    #
    # Returns true if String is Unicode
    #
    def isThisStringUnicode(self, s):
        """
        Determines if a string is Unicode (return True) or not (returns False)
        to allow correct print operations.

        Used by StrUnicodeOut function.
        Example:
            niceprint('Checking file:[{!s}]...'.format(
                                     file.encode('utf-8') \
                                     if isThisStringUnicode(file) \
                                     else file))

        >>> import niceprint as npc
        >>> np = npc.niceprint()
        >>> np.isThisStringUnicode('No Unicode string')
        False
        >>> np.isThisStringUnicode(u'Unicode string')
        True
        >>> isThisStringUnicode(2)
        False
        """
        # CODING: Python 2 and 3 compatibility
        # CODING: On Python 3 should always return False to return s
        # in the example
        #    s.encode('utf-8') if isThisStringUnicode(s) else s
        if sys.version_info < (3, ):
            if isinstance(s, unicode):
                return True
            elif isinstance(s, str):
                return False
            else:
                return False
        elif isinstance(s, str):
            return False
        else:
            return False


    # -------------------------------------------------------------------------
    # StrUnicodeOut
    #
    # Returns true if String is Unicode
    #
    def StrUnicodeOut(self, s):
        """
        Outputs s.encode('utf-8') if isThisStringUnicode(s) else s
            niceprint('Checking file:[{!s}]...'.format(StrUnicodeOut(file))

        >>> import niceprint as npc
        >>> np = npc.niceprint()
        >>> np.StrUnicodeOut('Hello')
        'Hello'
        """
        if s is not None:
            return s.encode('utf-8') if self.isThisStringUnicode(s) else s
        else:
            return ''.encode('utf-8') if self.isThisStringUnicode('') else ''


    # -------------------------------------------------------------------------
    # niceprint
    #
    # Print a message with the format:
    #   [2017.10.25 22:32:03]:[PRINT   ]:[uploadr] Some Message
    #
    def niceprint(self, s, fname='uploadr'):
        """
        Print a message with the format:
            [2017.11.19 01:53:57]:[PID       ][PRINT   ]:[uploadr] Some Message
            Accounts for UTF-8 Messages

        """
        print('{}[{!s}][{!s}]:[{!s:11s}]{}[{!s:8s}]:[{!s}] {!s}'.format(
                UPLDRConstants.G,
                UPLDRConstants.Run,
                time.strftime(UPLDRConstants.TimeFormat),
                os.getpid(),
                UPLDRConstants.W,
                'PRINT',
                self.StrUnicodeOut(fname),
                self.StrUnicodeOut(s)))


    # -------------------------------------------------------------------------
    # niceassert
    #
    def niceassert(self, s):
        """
         Returns a message with the format:
             [2017.11.19 01:53:57]:[PID       ][ASSERT  ]:[uploadr] Message
             Accounts for UTF-8 Messages

         Usage:
             assert param1 >= 0, niceassert('param1 is not >= 0:'
                                            .format(param1))
        """
        return('{}[{!s}][{!s}]:[{!s:11s}]{}[{!s:8s}]:[{!s}] {!s}'.format(
               UPLDRConstants.R,
               UPLDRConstants.Run,
               time.strftime(UPLDRConstants.TimeFormat),
               os.getpid(),
               UPLDRConstants.W,
               'ASSERT',
               'uploadr',
               self.StrUnicodeOut(s)))

    # -------------------------------------------------------------------------
    # reportError
    #
    # Provides a messaging wrapper for logging.error, niceprint and
    # str(sys.exc_info() functions.
    #
    # Examples of use of reportError:
    # except flickrapi.exceptions.FlickrError as ex:
    #     reportError(Caught=True,
    #                 CaughtPrefix='+++',
    #                 CaughtCode='990',
    #                 CaughtMsg='Flickrapi exception on photos.setdates',
    #                 exceptUse=True,
    #                 exceptCode=ex.code,
    #                 exceptMsg=ex,
    #                 NicePrint=True,
    #                 exceptSysInfo=True)
    # except lite.Error as e:
    #     reportError(Caught=True,
    #                 CaughtPrefix='+++ DB',
    #                 CaughtCode='991',
    #                 CaughtMsg='DB error on INSERT: [{!s}]'
    #                           .format(e.args[0]),
    #                 NicePrint=True)
    #     # Release the lock on error.
    #     self.useDBLock(lock, False)
    #     success = False
    # except:
    #     reportError(Caught=True,
    #                 CaughtPrefix='+++',
    #                 CaughtCode='992',
    #                 CaughtMsg='Caught exception in XXXX',
    #                 exceptSysInfo=True)
    #
    def reportError(self,
                    Caught=False, CaughtPrefix='', CaughtCode=0, CaughtMsg='',
                    NicePrint=False,
                    exceptUse=False, exceptCode=0, exceptMsg='',
                    exceptSysInfo=''):
        """ reportError

          Caught = True/False
          CaughtPrefix
            ===     Multiprocessing related
            +++     Exceptions handling related
            +++ DB  Database Exceptions handling related
            xxx     Error related
          CaughtCode = '010'
          CaughtMsg = 'Flickrapi exception on...'/'DB Error on INSERT'
          NicePrint = True/False
          exceptUse = True/False
          exceptCode = ex.code
          exceptMsg = ex
          exceptSysInfo = True/False
        """

        if Caught is not None and Caught:
            logging.error('{!s}#{!s}: {!s}'.format(CaughtPrefix,
                                                   CaughtCode,
                                                   CaughtMsg))
            if NicePrint is not None and NicePrint:
                self.niceprint('{!s}#{!s}: {!s}'.format(CaughtPrefix,
                                                        CaughtCode,
                                                        CaughtMsg))
        if exceptUse is not None and exceptUse:
            logging.error('Error code: [{!s}]'.format(exceptCode))
            logging.error('Error code: [{!s}]'.format(exceptMsg))
            if NicePrint is not None and NicePrint:
                self.niceprint('Error code: [{!s}]'.format(exceptCode))
                self.niceprint('Error code: [{!s}]'.format(exceptMsg))
        if exceptSysInfo is not None and exceptSysInfo:
            logging.error(str(sys.exc_info()))
            if NicePrint is not None and NicePrint:
                self.niceprint(str(sys.exc_info()))

        sys.stderr.flush()
        if NicePrint is not None and NicePrint:
            sys.stdout.flush()


# -----------------------------------------------------------------------------
# If called directly run doctests
#
if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG,
                        format='[%(asctime)s]:[%(processName)-11s]' +
                               '[%(levelname)-8s]:[%(name)s] %(message)s')

    import doctest
    doctest.testmod()

    # Comment following line to allow further debugging/testing
    sys.exit(0)