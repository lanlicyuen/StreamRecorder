from win32_version_info import *

version_info = VSVersionInfo(
    ffi=FixedFileInfo(
        filevers=(1, 4, 0, 0),
        prodvers=(1, 4, 0, 0),
        mask=0x3f,
        flags=0x0,
        OS=0x40004,
        fileType=0x1,
        subtype=0x0,
        date=(0, 0)
    ),
    kids=[
        StringFileInfo([
            StringTable(
                '040904B0',
                [
                    StringStruct('CompanyName', 'Lanlic Yuen'),
                    StringStruct('FileDescription', 'Stream Recorder Application'),
                    StringStruct('FileVersion', '1.4.0.0'),
                    StringStruct('InternalName', 'StreamRecorder'),
                    StringStruct('LegalCopyright', '© 2024 Lanlic Yuen. All rights reserved.'),
                    StringStruct('OriginalFilename', 'StreamRecorder.exe'),
                    StringStruct('ProductName', 'Stream Recorder'),
                    StringStruct('ProductVersion', '1.4.0.0')
                ]
            )
        ]),
        VarFileInfo([VarStruct('Translation', [0x0409, 0x04B0])])
    ]
)