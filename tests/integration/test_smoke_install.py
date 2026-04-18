import shutil
import unittest

from tooling.smoke_install import smoke_install


@unittest.skipUnless(shutil.which("claude"), "claude CLI is required for smoke install test")
class SmokeInstallIntegrationTests(unittest.TestCase):
    def test_smoke_install_returns_zero(self) -> None:
        self.assertEqual(smoke_install(), 0)


if __name__ == "__main__":
    unittest.main()
