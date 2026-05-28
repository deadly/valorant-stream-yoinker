# -*- mode: python ; coding: utf-8 -*-
# Build from project root:
#   pip install pyinstaller
#   pyinstaller valorant-stream-yoinker-bomb-timer.spec
# Output: dist/ValorantStreamYoinkerBombTimer.exe

import os

block_cipher = None

src_dir = os.path.join(SPECPATH, 'src')
img_dir = os.path.join(src_dir, 'img')
datas = [(img_dir, 'img')] if os.path.isdir(img_dir) else []

a = Analysis(
    [os.path.join(src_dir, 'main.py')],
    pathex=[src_dir],
    binaries=[],
    datas=datas,
    hiddenimports=[
        'valclient',
        'valclient.client',
        'PIL',
        'PIL.Image',
        'PIL.ImageGrab',
        'cv2',
        'numpy',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='ValorantStreamYoinkerBombTimer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
