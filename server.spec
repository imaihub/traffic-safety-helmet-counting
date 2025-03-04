# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files
from PyInstaller.building.datastruct import Tree
import glob

datas = []
datas += collect_data_files('gradio_client')
datas += collect_data_files('gradio')

def get_tree(path: str):
    files = glob.glob(path + "/**", recursive=True)
    tree = []
    for f in files:
        if os.path.isfile(f):  # Ensure we're only adding files, not directories
            dest = os.path.join("models", os.path.dirname(os.path.relpath(f, path)))
            tree.append((f, dest))
            print(f"Adding file {f} to {dest}")
    return tree

datas.extend(get_tree("models"))

datas.append(("config.yaml", "."))

a = Analysis(
    ['gradio_server/server.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
    module_collection_mode={
        'gradio': 'py',  # Collect gradio package as source .py files
    },
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='server',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='server',
)
