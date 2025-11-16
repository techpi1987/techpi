"""
Safe Educational Password Tools
- DO NOT use any brute-force code on online accounts, servers, or any system
  you do not own or have explicit, written permission to test.
- This script is for learning: estimating brute-force difficulty, generating
  strong passwords, and an in-memory demonstration of how a brute-force loop works.

Usage:
- Run the script and follow menu choices.
"""

import itertools
import math
import secrets
import string
import time

# ---------------------------
# Utilities
# ---------------------------

def estimate_combinations(charset_size: int, length: int) -> int:
    """Return number of possible combinations (charset_size^length)."""
    return charset_size ** length

def estimate_time_seconds(combinations: int, guesses_per_second: float) -> float:
    """Estimate seconds to try all combinations at given guesses/second."""
    if guesses_per_second <= 0:
        raise ValueError("guesses_per_second must be positive")
    return combinations / guesses_per_second

def human_time(seconds: float) -> str:
    """Convert seconds to a human readable string (approx)."""
    if seconds < 1:
        return f"{seconds:.3f} seconds"
    minute = 60
    hour = 3600
    day = 86400
    year = 365 * day
    if seconds < minute:
        return f"{seconds:.1f} seconds"
    if seconds < hour:
        return f"{seconds/60:.1f} minutes"
    if seconds < day:
        return f"{seconds/hour:.1f} hours"
    if seconds < year:
        return f"{seconds/day:.1f} days"
    return f"{seconds/year:.2f} years"

# ---------------------------
# Password generator & strength estimator
# ---------------------------

def generate_password(length=16, use_lower=True, use_upper=True, use_digits=True, use_punct=True) -> str:
    """Generate a cryptographically secure password."""
    charset = ""
    if use_lower:
        charset += string.ascii_lowercase
    if use_upper:
        charset += string.ascii_uppercase
    if use_digits:
        charset += string.digits
    if use_punct:
        # remove ambiguous chars if you wish
        charset += "!@#$%^&*()-_=+[]{};:,.<>/?"
    if not charset:
        raise ValueError("At least one character class must be enabled")
    return ''.join(secrets.choice(charset) for _ in range(length))

def estimate_password_strength(password: str, guesses_per_second: float = 1e9) -> dict:
    """
    Estimate entropy and time to brute-force given guesses/sec.
    This is a rough estimator assuming each character could be any from the used classes.
    """
    classes = [
        (any(c.islower() for c in password), 26),
        (any(c.isupper() for c in password), 26),
        (any(c.isdigit() for c in password), 10),
        (any(c in string.punctuation for c in password), len("!@#$%^&*()-_=+[]{};:,.<>/?"))
    ]
    charset_size = sum(size for used, size in classes if used)
    length = len(password)
    combinations = estimate_combinations(charset_size if charset_size>0 else 1, length)
    entropy_bits = math.log2(combinations) if combinations>0 else 0
    secs = estimate_time_seconds(combinations, guesses_per_second)
    return {
        "length": length,
        "charset_size": charset_size,
        "combinations": combinations,
        "entropy_bits": entropy_bits,
        "time_seconds_at_guesses_per_sec": secs,
        "time_human": human_time(secs)
    }

# ---------------------------
# Educational brute-force simulator (local only)
# ---------------------------

def demo_bruteforce_local(target: str, charset: str, max_length: int = None):
    """
    Demo how brute-force tries combinations in memory.
    WARNING: This is purely educational and runs only locally against the 'target' string
             stored in this program. Do NOT use this against any remote system.
    For demonstration, keep charset and max_length very small (e.g., charset='ab', max_length=4).
    """
    assert target is not None
    if max_length is None:
        max_length = len(target)
    print(f"Starting local demo brute-force. Target length: {len(target)}. Charset length: {len(charset)}")
    start = time.time()
    tried = 0
    for length in range(1, max_length+1):
        for attempt in itertools.product(charset, repeat=length):
            tried += 1
            attempt_str = ''.join(attempt)
            if attempt_str == target:
                elapsed = time.time() - start
                print(f"Found target '{target}' after {tried} attempts in {elapsed:.4f} seconds.")
                return {"found": True, "attempts": tried, "time_seconds": elapsed}
    elapsed = time.time() - start
    print(f"Target not found after {tried} attempts in {elapsed:.4f} seconds.")
    return {"found": False, "attempts": tried, "time_seconds": elapsed}

# ---------------------------
# Interactive demo CLI
# ---------------------------

def main_menu():
    print("Safe Password Tools — educational only\n")
    while True:
        print("\nMenu:")
        print("1) Generate a strong password")
        print("2) Estimate strength of a password")
        print("3) Estimate brute-force time for given charset/length and guesses/sec")
        print("4) Run local (in-memory) brute-force demo (educational only)")
        print("5) Exit")
        choice = input("Choose an option (1-5): ").strip()
        if choice == "1":
            L = int(input("Length (e.g. 16): ").strip() or "16")
            pw = generate_password(length=L)
            print("Generated password:", pw)
        elif choice == "2":
            pw = input("Enter password to estimate: ").strip()
            gps = float(input("Assumed guesses per second (e.g. 1e9): ").strip() or "1e9")
            res = estimate_password_strength(pw, gps)
            print("Estimation:")
            for k, v in res.items():
                print(f"  {k}: {v}")
            print("Note: this is a rough estimate. Use long unique passphrases and a password manager.")
        elif choice == "3":
            charset = input("Enter charset (e.g. abc... or 'lower,upper,digits'): ").strip()
            if charset.lower() == "lower,upper,digits":
                charset_str = string.ascii_lowercase + string.ascii_uppercase + string.digits
            else:
                charset_str = charset
            length = int(input("Password length: ").strip())
            gps = float(input("Guesses per second (e.g. 1e9): ").strip() or "1e9")
            combos = estimate_combinations(len(charset_str), length)
            secs = estimate_time_seconds(combos, gps)
            print(f"Combinations: {combos}")
            print(f"Estimated time at {gps:.0f} guesses/sec: {human_time(secs)}")
        elif choice == "4":
            print("** LOCAL DEMO WARNING ** This demo is purely local and educational.")
            target = input("Enter target string (the script will try to find this): ").strip()
            charset = input("Enter a small charset to try (e.g. abcd): ").strip()
            max_len = int(input("Max length to attempt (keep small, e.g. 4): ").strip())
            demo_bruteforce_local(target, charset, max_len)
        elif choice == "5":
            print("Goodbye — stay safe and only test systems you own or are authorized to test.")
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main_menu()
