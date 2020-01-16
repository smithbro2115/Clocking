# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['/Users/pro/PycharmProjects/Clocking', "C:/Users/Josh/PycharmProjects/Clocking"],
             binaries=[],
             datas=[('Time Sheet.xlsx', '.'), ('Clocking Buttons.exe', '.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='Clocking',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False, icon="clock_icon.ico" )
app = BUNDLE(exe,
             name='Clocking.app',
             icon='clock_icon.icns',
             bundle_identifier=None,
             info_plist={
                'NSHighResolutionCapable': 'True'
                }
             )
