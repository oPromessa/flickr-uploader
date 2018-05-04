"""
    by oPromessa, 2017
    Published on https://github.com/oPromessa/flickr-uploader/

    Helper class and functions to print messages.
"""

# -----------------------------------------------------------------------------
# Import section for Python 2 and 3 compatible code
# from __future__ import absolute_import, division, print_function,
#    unicode_literals
from __future__ import division    # This way: 3 / 2 == 1.5; 3 // 2 == 1

# -----------------------------------------------------------------------------
# Import section
#
import sys
import os
import logging
import time
import lib.UPLDRConstants as UPLDRConstantsClass
UPLDRConstants = UPLDRConstantsClass.UPLDRConstants()


# -----------------------------------------------------------------------------
# class NicePrint to be used to print messages.
#
class NicePrint:
    """
        >>> import sys
        >>> import lib.NicePrint as npc
        >>> np = npc.NicePrint()
        >>> if sys.version_info < (3, ):
        ...     np.is_str_unicode('Something') == False
        ... else:
        ...     np.is_str_unicode('Something') == False
        True
        >>> if sys.version_info < (3, ):
        ...     np.is_str_unicode(u'With u prefix') == True
        ... else:
        ...     np.is_str_unicode(u'With u prefix') == False
        True
        >>> np.is_str_unicode(245)
        False
    """

    # -------------------------------------------------------------------------
    # class NicePrint __init__
    #
    def __init__(self):
        """ class NicePrint __init__
        """
        pass

    # -------------------------------------------------------------------------
    # is_str_unicode
    #
    # Returns true if String is Unicode
    #
    def is_str_unicode(self, astr):
        """
        Determines if a string is Unicode (return True) or not (returns False)
        to allow correct print operations.

        Used by strunicodeout function.
        Example:
            NicePrint('Checking file:[{!s}]...'.format(
                                     file.encode('utf-8') \
                                     if is_str_unicode(file) \
                                     else file))
        """
        # CODING: Python 2 and 3 compatibility
        # CODING: On Python 3 should always return False to return s
        # in the example
        #    s.encode('utf-8') if is_str_unicode(s) else s
        if sys.version_info < (3, ):
            if isinstance(astr, unicode):  # noqa
                result = True
            elif isinstance(astr, str):
                result = False
            else:
                result = False
        elif isinstance(astr, str):
            result = False
        else:
            result = False
        return result

    # -------------------------------------------------------------------------
    # strunicodeout
    #
    # Returns true if String is Unicode
    #
    def strunicodeout(self, astr):
        """
        Outputs s.encode('utf-8') if is_str_unicode(s) else s
            NicePrint('Checking file:[{!s}]...'.format(strunicodeout(file))

        >>> import lib.NicePrint as npc
        >>> np = npc.NicePrint()
        >>> np.strunicodeout('Hello')
        'Hello'
        """
        astr = '' if astr is None else astr
        return astr.encode('utf-8') if self.is_str_unicode(astr) else astr

    # -------------------------------------------------------------------------
    # niceprint
    #
    # Print a message with the format:
    #   [2017.10.25 22:32:03]:[PRINT   ]:[uploadr] Some Message
    #
    def niceprint(self, astr, fname='uploadr'):
        """
        Print a message with the format:
            [2017.11.19 01:53:57]:[PID       ][PRINT   ]:[uploadr] Some Message
            Accounts for UTF-8 Messages

        """
        print('{}[{!s}][{!s}]:[{!s:11s}]{}[{!s:8s}]:[{!s}] {!s}'
              .format(UPLDRConstants.G,
                      UPLDRConstants.Run,
                      time.strftime(UPLDRConstants.TimeFormat),
                      os.getpid(),
                      UPLDRConstants.W,
                      'PRINT',
                      self.strunicodeout(fname),
                      self.strunicodeout(astr)))

    # -------------------------------------------------------------------------
    # niceassert
    #
    def niceassert(self, astr):
        """
         Returns a message with the format:
             [2017.11.19 01:53:57]:[PID       ][ASSERT  ]:[uploadr] Message
             Accounts for UTF-8 Messages

         Usage:
             assert param1 >= 0, niceassert('param1 is not >= 0:'
                                            .format(param1))
        """
        return('{}[{!s}][{!s}]:[{!s:11s}]{}[{!s:8s}]:[{!s}] {!s}'
               .format(UPLDRConstants.R,
                       UPLDRConstants.Run,
                       time.strftime(UPLDRConstants.TimeFormat),
                       os.getpid(),
                       UPLDRConstants.W,
                       'ASSERT',
                       'uploadr',
                       self.strunicodeout(astr)))

    # -------------------------------------------------------------------------
    # niceerror
    #
    # Provides a messaging wrapper for logging.error, niceprint and
    # str(sys.exc_info() functions.
    #
    # Examples of use of niceerror:
    # except flickrapi.exceptions.FlickrError as ex:
    #     niceerror(caught=True,
    #               caughtprefix='+++',
    #               caughtcode='990',
    #               caughtmsg='Flickrapi exception on photos.setdates',
    #               exceptuse=True,
    #               exceptcode=ex.code,
    #               exceptmsg=ex,
    #               useniceprint=True,
    #               exceptsysinfo=True)
    # except lite.Error as e:
    #     niceerror(caught=True,
    #               caughtprefix='+++ DB',
    #               caughtcode='991',
    #               caughtmsg='DB error on INSERT: [{!s}]'
    #                         .format(e.args[0]),
    #               useniceprint=True)
    #     # Release the lock on error.
    #     self.useDBLock(lock, False)
    #     success = False
    # except:
    #     niceerror(caught=True,
    #               caughtprefix='+++',
    #               caughtcode='992',
    #               caughtmsg='Caught exception in XXXX',
    #               exceptsysinfo=True)
    #
    def niceerror(self,
                  caught=False, caughtprefix='', caughtcode=0, caughtmsg='',
                  useniceprint=False,
                  exceptuse=False, exceptcode=0, exceptmsg='',
                  exceptsysinfo=''):
        """ niceerror

          caught = True/False
          caughtprefix
            ===     Multiprocessing related
            +++     Exceptions handling related
            +++ DB  Database Exceptions handling related
            xxx     Error related
          caughtcode = '010'
          caughtmsg = 'Flickrapi exception on...'/'DB Error on INSERT'
          useniceprint = True/False
          exceptuse = True/False
          exceptcode = ex.code
          exceptmsg = ex
          exceptsysinfo = True/False
        """

        if caught is not None and caught:
            logging.error('%s#%s: %s',
                          caughtprefix,
                          caughtcode,
                          caughtmsg)
            if useniceprint is not None and useniceprint:
                self.niceprint('{!s}#{!s}: {!s}'.format(caughtprefix,
                                                        caughtcode,
                                                        caughtmsg))
        if exceptuse is not None and exceptuse:
            logging.error('Error code: [%s]', exceptcode)
            logging.error('Error code: [%s]', exceptmsg)
            if useniceprint is not None and useniceprint:
                self.niceprint('Error code: [{!s}]'.format(exceptcode))
                self.niceprint('Error code: [{!s}]'.format(exceptmsg))
        if exceptsysinfo is not None and exceptsysinfo:
            logging.error(str(sys.exc_info()))
            if useniceprint is not None and useniceprint:
                self.niceprint(str(sys.exc_info()))

        sys.stderr.flush()
        if useniceprint is not None and useniceprint:
            sys.stdout.flush()

    # -------------------------------------------------------------------------
    # niceprocessedfiles
    #
    # Nicely print number of processed files
    #
    def niceprocessedfiles(self, count, ctotal, total):
        """
        niceprocessedfiles

        count  = Nicely print number of processed files rounded to 100's
        ctotal = Shows also the total number of items to be processed
        total  = if true shows the final count (use at the end of processing)
        """

        if not total:
            if int(count) % 100 == 0:
                self.niceprint('Files Processed:[{!s:>6s}] of [{!s:>6s}]'
                               .format(count, ctotal))
        else:
            if int(count) % 100 > 0:
                self.niceprint('Files Processed:[{!s:>6s}] of [{!s:>6s}]'
                               .format(count, ctotal))

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
