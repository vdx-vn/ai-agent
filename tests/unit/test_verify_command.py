import subprocess
import unittest


class VerifyCommandTests(unittest.TestCase):
    def test_verify_command_returns_zero(self) -> None:
        result = subprocess.run(
            ["python3", "-m", "tooling.cli", "verify"],
            check=False,
        )
        self.assertEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
