from kivy_deps import sdl2, glew
# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=True,
)

a.datas += [('logo.png', 'D:\\Doors\\pos\logo.png', 'DATA')]
a.datas += [('icon.ico', 'D:\\Doors\\pos\icon.ico', 'DATA')]

a.datas += [('main.kv', 'D:\\Doors\\pos\main.kv', 'DATA')]
a.datas += [('staff.kv', 'D:\\Doors\\pos\staff.kv', 'DATA')]
a.datas += [('signin.kv', 'D:\\Doors\\pos\signin.kv', 'DATA')]
a.datas += [('invoices.kv', 'D:\\Doors\\pos\invoices.kv', 'DATA')]
a.datas += [('admin.kv', 'D:\\Doors\\pos\admin.kv', 'DATA')]

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [('v', None, 'OPTION')],
    exclude_binaries=True,
    name='main',
    debug=True,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['icon.ico'],
)
coll = COLLECT(
    exe,
    Tree('D:\\Doors\\pos\\'),
    a.binaries,
    a.zipfiles,
    a.datas,
    *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main',
)