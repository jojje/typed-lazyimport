
# typed-lazyimport

Provides type hinted lazy import of slow to load libraries

# Usage

## Simple example and principal behavior

```python
from lazyimport import Libs
torch = Libs.torch         # does not trigger torch to be imported, but torch is still a typed variable

print(torch.__version__)   # causes torch to be imported and its version is then returned
print(torch.__version__)   # returns the same version from the already loaded library
```

## Intended use in a real codebase

```python
from lazyimport import Libs as L
torch = L.torch

def do_something_returning_a_tensor() -> torch.tensor:
    return torch.tensor(1)

# do various stuff that don't require torch and doesn't warrant loading it.
if condition:
    print(do_something_returning_a_tensor())  # only now do we pay the price for importing torch, since it adds value.
...
```

## Extending or lazily loading your own libraries

The provided `Libs` set is offered simply as a convenience, to offer close to zero-friction in order to gain lazy
importing of the most popular libraries. However, if your specific set of libraries isn't included, you can easily
create your own lazy-loaded library set.

Example:

```python
# mylibs.py (for example)
from __future__ import annotations         # only needed if you want type hints
from typing import TYPE_CHECKING           # -"-
from lazyimport import Lib

if TYPE_CHECKING:                          # -"-. Skip this block if you don't need type hints.
    from PIL import Image
    from myown.libs import flork

class Libraries:
    Image:Image = Lib('PIL.Image')         # the string the same format as "import" requires.
    flork:flork = Lib('myown.libs.flork')
```

Then you can happily use it with the same ease as the bundled library set:

```python
from mylibs import Libraries as L
flork = L.flork
Image = L.Image

flork(Image.open('cat.png'))
```

All type hinted of course.

One point of note is that the type hinting comes from the explicit type annotations used when defining each class variable.
Unfortunately those types are _only_ present when the type-checker runs, and not at program runtime.
This means that the nicer syntax option `Image = lib(Image)` isn't possible, because when the type-checker isn't running,
the type `Image` is never imported from `PIL`, and the program would crash as a result. That's why we have to specify the
import names using a _little_ bit of (horrible) type-unsafe "string programming". No way around it, but it's minimized.

To ensure there's no spelling mistake, my recommendation is to first enter `import <statement>` in the code editor or
interactive python, to verify the string is correct. Then copy the statement verbatim and quote it. That's the
least risky option I found (absent a better python type system).

## FAQ

### Q1: Why?

Because many popular libraries are _incredibly_ expensive (slow) to load. Especially ML related libraries.

### Q2: Why another library?

Because none of the ones available was trivial to use, absent of magic string-programming or error-prone dict mapping.

This library provides:

1. Transparent type hinting for a set of popular libraries that are known to be very slow to import.
2. Minimal additional complexity. A single additional import, but otherwise the syntax is pretty much identical to using 
   normal imports. In particular it allows the programmer to have module wide visibility of the imported types, just like
   with a normal import. It chucks away all the PEP 484 boilerplate that otherwise has to be added all across the code
   base, just to get some type hints. None of that needed here.

### Q3: Why isn't library X included?

Most likely since I don't use it myself.

The library is first and foremost a convenience library aimed at addressing the slow import of the most popular libraries. 
That said, I'm open to adding additional ones. Open an issue, let's discuss and then a PR (since I probably don't have
that library myself).

The cost of adding additional libraries is close to zero, so there's no practical reason for not expanding the set of
libraries provided out of the box in-finitum, other than it becoming harder for users to get an overview of which libraries
are made available.

If you have a special library or libraries you want to lazily load but that's not available in the `Libs` class, you can
easily create your own library set. 
See [Extending or lazily loading your own libraries](#extending-or-lazily-loading-your-own-libraries) 
as well as the unit-test in this project for an example that does just that. Take a look at the 
[lazy_import.py](./lazyimport/lazy_import.py) implementation itself for how to get typing support. It's really trivial
as can be seen by the minimal implementation of this package itself.


## Development

To execute the main function of the programs, either of the following options are viable

1. `python -m typed-lazyimport`
2. `python typed-lazyimport/__main__.py`

To simplify development, common actions are provided via [Makefile](Makefile) targets:

* test - default targets, runs pytest on the project
* build - create a wheel package distribution, ready to be uploaded to pypi or given to someone else.
* clean - removes temporary files generated as part of the package creation.
