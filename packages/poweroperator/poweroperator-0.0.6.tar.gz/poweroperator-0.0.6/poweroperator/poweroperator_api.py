import os
import json
import requests
from typing import List, Pattern, Dict
import re

BASE_URL: str = "https://poweroperator.com"

MAX_MODULE_BYTES : int = 40 * 1024 * 1024

SENSITIVE_PATTERNS: List[Pattern[str]] = [
    # API keys and tokens
    re.compile(r"(?i)api[._-]?key"),
    re.compile(r"(?i)secret[._-]?key"),
    re.compile(r"(?i)app[._-]?key"),
    re.compile(r"(?i)consumer[._-]?key"),
    re.compile(r"(?i)jwt[._-]?token"),
    re.compile(r"(?i)refresh[._-]?token"),
    re.compile(r"(?i)session[._-]?token"),
    re.compile(r"(?i)token"),
    # Passwords and secrets
    re.compile(r"(?i)password"),
    re.compile(r"(?i)passwd"),
    re.compile(r"(?i)pwd"),
    re.compile(r"(?i)pass"),
    re.compile(r"(?i)secret"),
    # Authentication related
    re.compile(r"(?i)auth"),
    re.compile(r"(?i)credential"),
    re.compile(r"(?i)basic[._-]?auth"),
    # Keys
    re.compile(r"(?i)private[._-]?key"),
    re.compile(r"(?i)access[._-]?key"),
    re.compile(r"(?i)license[._-]?key"),
    re.compile(r"(?i)encryption[._-]?key"),
    re.compile(r"(?i)ssh[._-]?key"),
    re.compile(r"(?i)certificate"),
    re.compile(r"(?i)cert"),
    # Service-specific patterns
    re.compile(r"(?i)(aws|amazon).*[._-]?(key|token|secret|credential|password)"),
    re.compile(r"(?i)(github|gh).*[._-]?(key|token|secret|credential|password)"),
    re.compile(
        r"(?i)(google|gcp|firebase).*[._-]?(key|token|secret|credential|password)"
    ),
    re.compile(r"(?i)(azure|microsoft).*[._-]?(key|token|secret|credential|password)"),
    re.compile(
        r"(?i)(stripe|paypal|braintree).*[._-]?(key|token|secret|credential|password)"
    ),
    # Database credentials
    re.compile(r"(?i)database[._-]?password"),
    re.compile(r"(?i)db[._-]?password"),
    re.compile(r"(?i)database[._-]?secret"),
    re.compile(r"(?i)db[._-]?secret"),
    re.compile(r"(?i)redis[._-]?password"),
]


def redact_sensitive_env_vars(environ: os._Environ) -> os._Environ:
    """
    Redact sensitive environment variables like API keys and passwords.

    Args:
        environ: Dictionary of environment variables or any non-dict value

    Returns:
        Dictionary with sensitive values redacted or the original value if not a dict
    """
    if not isinstance(environ, dict):
        return environ

    redacted_environ = environ.copy()

    # Check for sensitive environment variables by key name
    for key in redacted_environ:
        # First check if the key is sensitive
        for pattern in SENSITIVE_PATTERNS:
            if pattern.search(key):
                redacted_environ[key] = "[**REDACTED**]"
                break

        # Additional check for URL-based credentials in values
        # Only do this check if the value hasn't already been redacted
        if redacted_environ[key] != "[**REDACTED**]" and isinstance(
            redacted_environ[key], str
        ):
            value = redacted_environ[key]
            # Check for username:password pattern in URLs
            if re.search(r"://[^:]+:[^@]+@", value):
                # Redact just the password portion of URLs like http://user:pass@example.com
                redacted_environ[key] = re.sub(
                    r"(://[^:]+:)[^@]+(@)", r"\1[**REDACTED**]\2", value
                )

            # Check for typical token patterns in values (long hex/base64 strings)
            elif re.search(r"[A-Za-z0-9_\-]{20,}", value):
                # Check if it looks like a token/key pattern
                if any(
                    token_word in key.lower()
                    for token_word in [
                        "token",
                        "key",
                        "secret",
                        "password",
                        "credential",
                    ]
                ):
                    redacted_environ[key] = "[**REDACTED**]"

    return redacted_environ


def upload_mark_with_file(
    user: str,
    item: str,
    file_path: str,
    hostname: str,
    argv: list[str] | str,
    environ: os._Environ,
    cwd: str,
    modules: List[Dict],
) -> None:
    """Upload benchmark data to /api/mark endpoint"""
    endpoint = f"{BASE_URL}/api/mark"
    form_data = {
        "user": user,
        "item": item,
        "hostname": hostname,
        "cwd": cwd,
    }

    if isinstance(argv, list):
        form_data["argv"] = " ".join(str(arg) for arg in argv)
    else:
        form_data["argv"] = str(argv)

    redacted_environ = redact_sensitive_env_vars(environ)
    form_data["environ"] = " ".join(
        f"{key}={value}" for key, value in redacted_environ.items()
    )

    if modules:
        limited_modules = []
        total_size = 0

        for module in modules:
            module_json = json.dumps(module)
            module_size = len(module_json.encode('utf-8'))

            total_size += module_size
            if total_size > MAX_MODULE_BYTES:
                break

            limited_modules.append(module)

        form_data["modules"] = json.dumps(limited_modules)

    # print(f"[poweroperator] Sending POST request to {endpoint} with form data and file")
    # print(f"[poweroperator] Form data: {json.dumps(form_data, indent=2)}")

    files = {}
    if file_path and os.path.exists(file_path):
        files = {"file": open(file_path, "rb")}
    else:
        raise ValueError(f"No file provided or file not found: {file_path}")

    try:
        response = requests.post(endpoint, data=form_data, files=files)
        if response.status_code != 200:
            print(f"[poweroperator] Status Code: {response.status_code}")
            print(f"[poweroperator] Response: {response.text}")
            try:
                response_json = response.json()
                print(
                    f"[poweroperator] Response: {response.status_code} {json.dumps(response_json, indent=2)}"
                )
            except json.JSONDecodeError:
                raise Exception(
                    f"Response was not valid JSON: {response.status_code} {response}"
                )
        # Close file if opened
        if "file" in files and files["file"]:
            files["file"].close()
    except requests.exceptions.RequestException as e:
        if "file" in files and files["file"]:
            files["file"].close()
        raise e
