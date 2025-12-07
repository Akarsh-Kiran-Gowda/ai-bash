"""
System detection module for AI Bash.
Detects Linux distribution, kernel version, and package manager.
"""

import platform
import subprocess


def get_system_context():
    """
    Detect system environment including kernel, distribution, and package manager.
    
    Returns:
        dict: System context with kernel, distro, and pkg_manager keys
    """
    kernel = platform.release()
    distro = "unknown"

    try:
        distro = subprocess.check_output(
            ["bash", "-c", "source /etc/os-release && echo $ID"],
            text=True
        ).strip()
    except Exception:
        pass

    # Determine package manager based on distribution
    pkg_manager = "unknown"
    if distro in ["ubuntu", "debian"]:
        pkg_manager = "apt"
    elif distro in ["centos", "rhel", "rocky", "almalinux"]:
        pkg_manager = "yum/dnf"

    return {
        "kernel": kernel,
        "distro": distro,
        "pkg_manager": pkg_manager
    }


if __name__ == "__main__":
    # Test the detection
    context = get_system_context()
    print("System Context:")
    print(f"  Kernel: {context['kernel']}")
    print(f"  Distribution: {context['distro']}")
    print(f"  Package Manager: {context['pkg_manager']}")
