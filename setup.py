from distutils.core import setup
import py2exe

setup(windows=['ui/main.py'],
      options= {
          'py2exe': {
              'dll_excludes': ['api-ms-win-core-processthreads-l1-1-2.dll',
                               'api-ms-win-core-sysinfo-l1-2-1.dll',
                               'api-ms-win-core-heap-l2-1-0.dll',
                               'api-ms-win-core-delayload-l1-1-1.dll',
                               'api-ms-win-core-errorhandling-l1-1-1.dll',
                               'api-ms-win-core-profile-l1-1-0.dll',
                               'api-ms-win-core-libraryloader-l1-2-0.dll',
                               'api-ms-win-core-string-obsolete-l1-1-0.dll',
                               'api-ms-win-security-activedirectoryclient-l1-1-0.dll',
                               'libpq.dll']

          }
      })
