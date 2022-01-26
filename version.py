"""
This script generates a text file that will be used to write properties in the executable
"""

import codecs
import sys

sys.path.append('./Sources')
sys.path.append('./UI')

from mainwindow import MAJOR, MINOR, REV

VS_VERSION_INFO = """
VSVersionInfo(
  ffi=FixedFileInfo(
    # filevers and prodvers should be always a tuple with four items: (1, 2, 3, 4)
    # Set not needed items to zero 0.
    filevers=(%(revcomma)s),
    prodvers=(%(revcomma)s),
    # Contains a bitmask that specifies the valid bits 'flags'r
    mask=0x3f,
    # Contains a bitmask that specifies the Boolean attributes of the file.
    flags=0x0,
    # The operating system for which this file was designed.
    # 0x4 - NT and there is no need to change it.
    OS=0x4,
    # The general type of file.
    # 0x1 - the file is an application.
    fileType=0x1,
    # The function of the file.
    # 0x0 - the function is not defined for this fileType
    subtype=0x0,
    # Creation date and time stamp.
    date=(0, 0)
    ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'000004b0',
        [StringStruct(u'CompanyName', u''),
        StringStruct(u'FileDescription', u'Application that lists all real and virtual serial COM ports on a machine'),
        StringStruct(u'FileVersion', u'%(revpoint)s'),
        StringStruct(u'InternalName', u'PyCOM'),
        StringStruct(u'LegalCopyright', u'Copyright © 2020-2022'),
        StringStruct(u'OriginalFilename', u'pycom.exe'),
        StringStruct(u'ProductName', u'pyCOM'),
        StringStruct(u'ProductVersion', u'%(revpoint)s')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [0, 1200])])
  ]
)
"""

revcomma = f'{MAJOR}, {MINOR}, {REV}, 0'
revpoint = f'{MAJOR}.{MINOR}.{REV}'

# Write version info.
with codecs.open('version.txt', 'w', 'utf-8') as f:
    f.write('# UTF-8\n' + VS_VERSION_INFO % {
        'revcomma': revcomma,
        'revpoint': revpoint
    })
