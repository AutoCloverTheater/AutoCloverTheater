# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['src/app/main.py'],
    pathex=['src'],
    binaries=[],
    datas=[('img', 'img'),('src','src')],
    hiddenimports=[
    'yaml',
    'Flask',
    'Flask_Cors',
    'ImageHash',
    'loguru',
    'cnocr',
    'cnstd',
    'numpy',
    'opencv_contrib_python',
    'opencv_python',
    'Pillow',
    'PyYAML',
    'uiautomator2'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='MyApp_mac',
    debug=True,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
app = BUNDLE(
    exe,
    name='MyApp_mac.app',
    icon=None,
    bundle_identifier=None,
)
