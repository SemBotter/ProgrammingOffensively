# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

import sys
import os
import shutil

# Modify the ProgrammingOffensively.py file to use relative paths for venv
with open('ProgrammingOffensively.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Create a backup of the original file
if not os.path.exists('ProgrammingOffensively.py.bak'):
    with open('ProgrammingOffensively.py.bak', 'w', encoding='utf-8') as f:
        f.write(content)

# Modify the content to use runtime_tmpdir and relative paths
modified_content = content.replace(
    'venv_dir = os.path.join(targetDir, "venv")',
    'venv_dir = os.path.join(sys._MEIPASS, "venv") if hasattr(sys, "_MEIPASS") else os.path.join(targetDir, "venv")'
)

# Write the modified content back
with open('ProgrammingOffensively.py', 'w', encoding='utf-8') as f:
    f.write(modified_content)

a = Analysis(
    ["ProgrammingOffensively.py"],
    pathex=['.', 'src/'],
    datas=[
        ('src', 'src'),
        ('.env', '.') if os.path.exists('.env') else None
    ],
    binaries=[],
    hiddenimports=[
        'venv',
        'subprocess',
        'asyncio',
        'ThreadManager',
        'persist',
        'os',
        'sys'
    ],
    hookspath=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Filter out None values from datas
a.datas = [item for item in a.datas if item is not None]

# Create directory for Python environment files
venv_source = os.path.dirname(sys.executable)
temp_dir = os.path.abspath("temp_venv")
venv_target_dir = os.path.join(temp_dir, "venv")

# Create temporary directory to copy Python files
if not os.path.exists(venv_target_dir):
    os.makedirs(venv_target_dir, exist_ok=True)

# Define directories to copy
dirs_to_copy = ['DLLs', 'Lib', 'Scripts', 'include']

# Copy directories to temporary location before creating the executable
for dir_name in dirs_to_copy:
    src_dir = os.path.join(venv_source, dir_name)
    dst_dir = os.path.join(venv_target_dir, dir_name)
    if os.path.exists(src_dir):
        print(f"Copying directory: {src_dir} -> {dst_dir}")
        shutil.copytree(src_dir, dst_dir, dirs_exist_ok=True)

# Copy Python executables and DLLs
for file_name in os.listdir(venv_source):
    if file_name.endswith('.exe') or file_name.endswith('.dll'):
        src_file = os.path.join(venv_source, file_name)
        dst_file = os.path.join(venv_target_dir, file_name)
        print(f"Copying file: {src_file} -> {dst_file}")
        shutil.copy2(src_file, dst_file)

# Also handle run_discordbot.bat to use relative paths
bat_file = os.path.join('src', 'run_discordbot.bat')
if os.path.exists(bat_file):
    with open(bat_file, 'r', encoding='utf-8') as f:
        bat_content = f.read()
    
    # Create backup
    if not os.path.exists(bat_file + '.bak'):
        with open(bat_file + '.bak', 'w', encoding='utf-8') as f:
            f.write(bat_content)
    
    # Modify content to use relative paths
    mod_bat = bat_content.replace(
        '&&CURDIR&&', 
        '%~dp0'  # This is batch script for "directory of this batch file"
    ).replace(
        '&&VENVDIR&&', 
        '%~dp0\\venv'
    )
    
    # Write modified batch file
    with open(bat_file, 'w', encoding='utf-8') as f:
        f.write(mod_bat)

# Special handling for venv
for root, dirs, files in os.walk(venv_target_dir):
    # Create relative path for data
    rel_dir = os.path.relpath(root, temp_dir)
    
    # Add directory structure to datas
    for file in files:
        file_path = os.path.join(root, file)
        rel_path = os.path.join(rel_dir, file)
        a.datas.append((rel_path, file_path, 'DATA'))

# Enable UPX for better compression
upx_args = ['--ultra-brute']

# Add resource file for application icon and version info
resource_file = []
version_info = None
if os.path.exists('app_icon.ico'):
    resource_file.append('app_icon.ico')
    version_info = {
        'version': '1.0.0',
        'company_name': 'Your Company',
        'file_description': 'Programming Offensively',
        'product_name': 'ProgrammingOffensively',
        'legal_copyright': '2025'
    }

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# Create a single executable with all files included
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas, 
    [],
    name='ProgrammingOffensively',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_args=upx_args,
    upx_exclude=[],
    runtime_tmpdir=None,  # Extract to temp at runtime
    console=True,
    icon=resource_file[0] if resource_file else None,
    version=version_info
)

# Restore original files
def restore_originals():
    if os.path.exists('ProgrammingOffensively.py.bak'):
        shutil.copy2('ProgrammingOffensively.py.bak', 'ProgrammingOffensively.py')
        os.remove('ProgrammingOffensively.py.bak')
    
    bat_bak = os.path.join('src', 'run_discordbot.bat.bak')
    if os.path.exists(bat_bak):
        shutil.copy2(bat_bak, os.path.join('src', 'run_discordbot.bat'))
        os.remove(bat_bak)
    
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)

import atexit
atexit.register(restore_originals)


