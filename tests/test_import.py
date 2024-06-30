import unittest
from types import ModuleType
from lazyimport.lazy_import import Lib, LazyLoader


class TestLazyImport(unittest.TestCase):
    def test_ensure_expected_lazy_loading_behavior(self):
        class LazyLibs:
            mylib = Lib('tests.fixture')

        self.assertIsInstance(LazyLibs.mylib, LazyLoader)      # 1. proxy initially created
        self.assertEqual(LazyLibs.mylib.__version__, '1.2.3')  # 2. first attribute swaps it to the actual library
        self.assertIsInstance(LazyLibs.mylib, ModuleType)      # 3. proves the above claim.

    def test_specify_behavior_for_referenced_proxy(self):
        class LazyLibs:
            mylib = Lib('tests.fixture')

        lib = LazyLibs.mylib
        self.assertIsInstance(lib, LazyLoader)          # 1. proxy initially created
        self.assertEqual(lib.__version__, '1.2.3')      # 2. first attribute swaps it to the actual library
        self.assertIsInstance(lib, LazyLoader)          # 3. since the variable was bound to the proxy, the proxy acts
                                                        # noqa: E116 transparently except for the attributes contained.

        self.assertFalse('__version__' in vars(lib))    # as documented...
        self.assertTrue(hasattr(lib, '__version__'))    # ... but is transparent to most code use.
