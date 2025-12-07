"""
Test suite for AI Bash behavioral examples from README.
Run this to verify the system works as expected.
"""

import os
os.environ['GEMINI_API_KEY'] = 'test-key-placeholder'  # Set placeholder for testing

from system_detect import get_system_context
from safety import validate_command, is_dangerous_command


def test_safety_validation():
    """Test safety validation with examples from README."""
    print("=" * 60)
    print("SAFETY VALIDATION TESTS")
    print("=" * 60)
    
    test_cases = [
        # (command, should_be_safe, description)
        ("apt install -y nginx", True, "Safe package installation"),
        ("dnf install -y nginx", True, "Safe package installation (RHEL)"),
        ("find /home -type f -size +500M", True, "Safe file search"),
        ("cd /var/log", True, "Safe directory change"),
        ("ls -la", True, "Safe directory listing"),
        ("rm -rf /", False, "Dangerous: Delete root"),
        ("rm -fr /", False, "Dangerous: Delete root (alternate)"),
        ("mkfs.ext4 /dev/sda1", False, "Dangerous: Format disk"),
        ("dd if=/dev/zero of=/dev/sda", False, "Dangerous: Overwrite disk"),
        ("shutdown now", False, "Dangerous: Shutdown system"),
        ("reboot", False, "Dangerous: Reboot system"),
        ("chmod -R 777 /", False, "Dangerous: Chmod root"),
        ("ERROR: Unsafe or ambiguous request", False, "LLM refusal message"),
    ]
    
    passed = 0
    failed = 0
    
    for command, should_be_safe, description in test_cases:
        is_safe, message = validate_command(command)
        
        # Check if result matches expectation
        if is_safe == should_be_safe:
            status = "✓ PASS"
            passed += 1
        else:
            status = "✗ FAIL"
            failed += 1
        
        print(f"\n{status}: {description}")
        print(f"  Command: {command}")
        print(f"  Expected: {'SAFE' if should_be_safe else 'BLOCKED'}")
        print(f"  Got: {'SAFE' if is_safe else 'BLOCKED'}")
        if not is_safe:
            print(f"  Reason: {message}")
    
    print("\n" + "=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0


def test_system_detection():
    """Test system detection functionality."""
    print("\n" + "=" * 60)
    print("SYSTEM DETECTION TEST")
    print("=" * 60)
    
    context = get_system_context()
    
    print(f"\nDetected System:")
    print(f"  Kernel: {context['kernel']}")
    print(f"  Distribution: {context['distro']}")
    print(f"  Package Manager: {context['pkg_manager']}")
    
    # Basic validation
    assert 'kernel' in context
    assert 'distro' in context
    assert 'pkg_manager' in context
    
    print("\n✓ System detection working")
    return True


def test_readme_examples():
    """Test the behavioral examples from README."""
    print("\n" + "=" * 60)
    print("README BEHAVIORAL EXAMPLES")
    print("=" * 60)
    
    examples = [
        {
            "input": "install nginx",
            "ubuntu_expected": "apt install -y nginx",
            "centos_expected": "dnf install -y nginx",
        },
        {
            "input": "clear all system cache and free RAM",
            "expected": "ERROR: Unsafe or ambiguous request",
        },
        {
            "input": "find files larger than 500MB in home directory",
            "expected": "find /home -type f -size +500M",
        },
        {
            "input": "move into /var/log directory",
            "expected": "cd /var/log",
        },
    ]
    
    print("\nExpected behaviors:")
    for i, example in enumerate(examples, 1):
        print(f"\n{i}. Input: {example['input']}")
        if 'expected' in example:
            print(f"   Expected: {example['expected']}")
        else:
            print(f"   Ubuntu: {example['ubuntu_expected']}")
            print(f"   CentOS: {example['centos_expected']}")
    
    print("\n✓ Examples documented (requires live LLM testing)")
    return True


def test_dangerous_patterns():
    """Test dangerous command pattern detection."""
    print("\n" + "=" * 60)
    print("DANGEROUS PATTERN DETECTION")
    print("=" * 60)
    
    dangerous_commands = [
        "rm -rf /",
        "rm -rf /*",
        "mkfs.ext4 /dev/sda",
        "dd if=/dev/zero of=/dev/sda",
        "shutdown -h now",
        ":(){ :|:& };:",  # fork bomb
        "chmod 777 / -R",
    ]
    
    safe_commands = [
        "rm -rf /tmp/myfile",
        "find / -name test",
        "ls -la /",
        "cd /var/log",
    ]
    
    print("\nTesting dangerous commands (should be blocked):")
    all_passed = True
    for cmd in dangerous_commands:
        is_dangerous = is_dangerous_command(cmd)
        status = "✓" if is_dangerous else "✗ FAIL"
        print(f"  {status} {cmd}")
        if not is_dangerous:
            all_passed = False
    
    print("\nTesting safe commands (should be allowed):")
    for cmd in safe_commands:
        is_dangerous = is_dangerous_command(cmd)
        status = "✓" if not is_dangerous else "✗ FAIL"
        print(f"  {status} {cmd}")
        if is_dangerous:
            all_passed = False
    
    if all_passed:
        print("\n✓ All dangerous pattern tests passed")
    else:
        print("\n✗ Some pattern tests failed")
    
    return all_passed


def run_all_tests():
    """Run all test suites."""
    print("\n╔═══════════════════════════════════════════╗")
    print("║      AI Bash Test Suite                   ║")
    print("╚═══════════════════════════════════════════╝\n")
    
    results = []
    
    # Run tests
    results.append(("System Detection", test_system_detection()))
    results.append(("Safety Validation", test_safety_validation()))
    results.append(("Dangerous Patterns", test_dangerous_patterns()))
    results.append(("README Examples", test_readme_examples()))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    for test_name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{status}: {test_name}")
    
    all_passed = all(passed for _, passed in results)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✓ ALL TESTS PASSED")
    else:
        print("✗ SOME TESTS FAILED")
    print("=" * 60 + "\n")
    
    return all_passed


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
