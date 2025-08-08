#!/usr/bin/env python3
"""
ECG AI Heart Diagnosis - Kivy GUI Launcher
Entry point for the Kivy-based GUI
"""

import sys
import os
import subprocess


def check_dependencies():
    """Check and install required dependencies for Kivy GUI.

    Honors local mirror preference; tries Tsinghua first, then fallbacks.
    """
    required_packages = [
        'kivy',
        'numpy',
        'pyserial',
    ]

    missing = []
    for pkg in required_packages:
        name = pkg.split('>=')[0]
        try:
            __import__(name)
        except Exception:
            missing.append(pkg)

    if not missing:
        return True

    print("🔧 Installing missing dependencies for Kivy GUI...")
    print(f"Missing: {', '.join(missing)}")

    mirrors = [
        'https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple',
        'https://pypi.douban.com/simple/',
        'https://mirrors.aliyun.com/pypi/simple/',
        'https://pypi.mirrors.ustc.edu.cn/simple/'
    ]

    for mirror in mirrors:
        host = mirror.split('//')[1].split('/')[0]
        print(f"🔄 Trying mirror: {host}")
        ok = True
        for pkg in missing:
            cmd = [sys.executable, '-m', 'pip', 'install', pkg, '-i', mirror, '--timeout', '60']
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
                if result.returncode != 0:
                    ok = False
                    print(f"   ❌ {pkg}: {result.stderr.splitlines()[-1] if result.stderr else 'unknown error'}")
                    break
                else:
                    print(f"   ✅ {pkg} installed")
            except subprocess.TimeoutExpired:
                ok = False
                print(f"   ⏱️ Timeout installing {pkg}")
                break
        if ok:
            print("✅ Dependencies installed successfully!")
            return True
        else:
            print(f"❌ Failed with {host}, trying next mirror...")

    print("\n❌ All mirrors failed or network unavailable.")
    print("\n📋 Manual installation options:")
    print("Option 1 - Mamba (recommended):")
    print("  /home/qiao/anaconda3/bin/mamba install -c conda-forge kivy numpy pyserial")
    print("Option 2 - Pip with Tsinghua mirror:")
    print("  python -m pip install -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple kivy numpy pyserial")
    return False


def main():
    print("🫀 ECG AI Heart Diagnosis - Kivy GUI")
    print("=" * 50)

    if not check_dependencies():
        print("❌ Please install missing dependencies before running.")
        sys.exit(1)

    try:
        # Ensure project root on sys.path
        project_root = os.path.dirname(os.path.abspath(__file__))
        if project_root not in sys.path:
            sys.path.insert(0, project_root)

        from ecg_receiver.gui_kivy.main_app import run_kivy_app
        print("🚀 Starting Kivy ECG interface...")
        run_kivy_app()

    except ImportError as e:
        print(f"❌ Import Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
