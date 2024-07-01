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

    def test_specify_transparent_behavior_for_referenced_proxy(self):
        class LazyLibs:
            mylib = Lib('tests.fixture')

        lib = LazyLibs.mylib
        self.assertIsInstance(lib, LazyLoader)          # 1. proxy initially created
        self.assertEqual(lib.__version__, '1.2.3')      # 2. first attribute access imports the actual library
        self.assertIsInstance(lib, LazyLoader)          # 3. proxy is still in place...

        self.assertIsInstance(lib, ModuleType)          # ... but looks like the real module
        self.assertTrue('__version__' in vars(lib))     # -"-
        self.assertTrue(hasattr(lib, '__version__'))    # -"-

    def test_lib_usage_example(self):
        import tests.fixture as fixture

        class LazyLibs:
            mylib:fixture = Lib('tests.fixture')

        f = LazyLibs.mylib.f                            # "from ... import ..." syntax analog, triggers the import
        Florker = LazyLibs.mylib.Flork                  # "from ... import ... as ..." analog, from already loaded lib

        self.assertEqual(f(3), 3)
        self.assertEqual(Florker().echo(4), 4)
