import unittest
import os
from poweroperator.poweroperator_api import (
    redact_sensitive_env_vars,
    SENSITIVE_PATTERNS,
)


class TestRedaction(unittest.TestCase):
    def test_redaction_of_sensitive_vars(self):
        # Create test environment with sensitive variables
        test_env = {
            "PATH": "/usr/bin:/bin",
            "HOME": "/home/user",
            "API_KEY": "super-secret-123",
            "MY_PASSWORD": "password123",
            "SECRET_TOKEN": "abcdef123456",
            "AUTH_CREDENTIAL": "very-sensitive",
            "PRIVATE_KEY": "-----BEGIN PRIVATE KEY-----",
            "AWS_ACCESS_KEY": "AKIAIOSFODNN7EXAMPLE",
            "DATABASE_URL": "postgres://user:pass@localhost/db",
            "NORMAL_VAR": "not sensitive",
        }

        # Redact the environment
        redacted = redact_sensitive_env_vars(test_env)

        # Verify sensitive variables are redacted
        self.assertEqual(redacted["API_KEY"], "[**REDACTED**]")
        self.assertEqual(redacted["MY_PASSWORD"], "[**REDACTED**]")
        self.assertEqual(redacted["SECRET_TOKEN"], "[**REDACTED**]")
        self.assertEqual(redacted["AUTH_CREDENTIAL"], "[**REDACTED**]")
        self.assertEqual(redacted["PRIVATE_KEY"], "[**REDACTED**]")
        self.assertEqual(redacted["AWS_ACCESS_KEY"], "[**REDACTED**]")

        # Verify non-sensitive variables are unchanged
        self.assertEqual(redacted["PATH"], "/usr/bin:/bin")
        self.assertEqual(redacted["HOME"], "/home/user")
        # DATABASE_URL now has password component redacted
        self.assertNotEqual(redacted["DATABASE_URL"], "postgres://user:pass@localhost/db")
        self.assertEqual(redacted["DATABASE_URL"], "postgres://user:[**REDACTED**]@localhost/db")
        self.assertEqual(redacted["NORMAL_VAR"], "not sensitive")

    def test_non_dictionary_input(self):
        # Test with non-dictionary input
        result = redact_sensitive_env_vars("not a dict")
        self.assertEqual(result, "not a dict")

        result = redact_sensitive_env_vars(None)
        self.assertIsNone(result)
        
    def test_url_credential_redaction(self):
        # Test URLs with embedded credentials
        test_env = {
            "DB_URL": "postgresql://admin:secretpassword@database.example.com:5432/mydb",
            "REDIS_URL": "redis://user:complex-password@redis.example.com:6379",
            "MONGODB_URI": "mongodb://dbuser:dbpass@mongo.example.com:27017/test",
            "NORMAL_URL": "https://example.com/api/data"
        }
        
        redacted = redact_sensitive_env_vars(test_env)
        
        # Verify only the password portions are redacted
        self.assertEqual(redacted["DB_URL"], "postgresql://admin:[**REDACTED**]@database.example.com:5432/mydb")
        self.assertEqual(redacted["REDIS_URL"], "redis://user:[**REDACTED**]@redis.example.com:6379")
        self.assertEqual(redacted["MONGODB_URI"], "mongodb://dbuser:[**REDACTED**]@mongo.example.com:27017/test")
        self.assertEqual(redacted["NORMAL_URL"], "https://example.com/api/data")
        
    def test_token_pattern_redaction(self):
        # Test variables that contain values that look like tokens
        test_env = {
            "GITHUB_TOKEN_VALUE": "ghp_1234567890abcdefghijklmnopqrstuvwxyz",
            "AWS_KEY_VALUE": "AKIAIOSFODNN7EXAMPLE12345678901234567890",
            "OPENAI_API_KEY_VALUE": "sk-1234567890abcdefghijklmnopqrstuvwxyz",
            "NORMAL_LONG_VALUE": "this-is-just-a-very-long-normal-string-with-no-secrets-in-it",
            "NORMAL_STRING": "short string"
        }
        
        redacted = redact_sensitive_env_vars(test_env)
        
        # Verify token-like values in sensitive keys are redacted
        self.assertEqual(redacted["GITHUB_TOKEN_VALUE"], "[**REDACTED**]")
        self.assertEqual(redacted["AWS_KEY_VALUE"], "[**REDACTED**]")
        self.assertEqual(redacted["OPENAI_API_KEY_VALUE"], "[**REDACTED**]")
        
        # Verify non-sensitive values aren't redacted even if they're long
        self.assertEqual(redacted["NORMAL_LONG_VALUE"], 
                        "this-is-just-a-very-long-normal-string-with-no-secrets-in-it")
        self.assertEqual(redacted["NORMAL_STRING"], "short string")

    def test_all_sensitive_patterns(self):
        # Test that all patterns in SENSITIVE_PATTERNS are working
        test_vars = {}
        expected_redacted = {}

        # Create test variables for each pattern
        for i, pattern in enumerate(SENSITIVE_PATTERNS):
            # Extract the main part of the pattern for testing
            pattern_str = pattern.pattern
            # Remove regex parts to get a usable variable name
            clean_pattern = pattern_str.replace("(?i)", "").replace("[._-]?", "_")
            var_name = f"TEST_{clean_pattern.upper()}"

            test_vars[var_name] = f"sensitive-value-{i}"
            expected_redacted[var_name] = "[**REDACTED**]"

        redacted = redact_sensitive_env_vars(test_vars)

        # Check all variables were redacted
        for key, value in expected_redacted.items():
            self.assertEqual(redacted[key], value, f"Failed to redact {key}")


if __name__ == "__main__":
    unittest.main()
