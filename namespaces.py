from contextlib import contextmanager
from typing import Optional

import __main__

class AttributeDict():
  """Base class with item get/set/contains methods that wrap over __dict__."""

  def __getitem__(self, key: str):
    return self.__dict__[key]

  def __setitem__(self, key: str, value):
    self.__dict__[key] = value

  def __contains__(self, key: str):
    return key in self.__dict__

class GlobalNamespace(AttributeDict):
  """Class used for the <G> object, which represents the global scope inside of a namespace block."""
  "Base class "

  def __setattr__(self, name: str, value):
    if name != '__dict__':
      self.__dict__[name] = value
    else:
      super().__setattr__(name, value)

class Namespace(GlobalNamespace):
  """Class used for namespaces (apart from the global namespace)."""

  def __call__(self):
     return use_namespace(ns=self)

class NamespaceHolder(AttributeDict):
  """Class used for the <namespaces> object, used to automagically create namespaces."""

  def __getattr__(self, name: str) -> Namespace:
      return self[name]

  def __getitem__(self, key: str):
    if key not in self.__dict__:
      self.__dict__[key] = Namespace() 

    return self.__dict__[key]


G = GlobalNamespace()
namespaces = NamespaceHolder()

class GDict(dict):
  def __setitem__(self, key, value):
    vars(__main__)[key] = value
    super().__setitem__(key, value)


def globals_snapshot():
  """Stores a snapshot of the current global namespace in the G object. This allows you to use the global namespace as if it was local, and then retrieve the original variables using <globals_restore()>."""
  G.__dict__ = GDict(vars(__main__).items())


def globals_restore():
  """Restores the global variables stored in the G object."""
  g = vars(__main__)
  gg = G
  fallback = g.copy()

  try:
    g.clear()
    g.update(gg.__dict__)
  except:
    g.update(fallback)
    raise
  finally:
    del gg.__dict__


@contextmanager
def use_namespace(enable: bool=True, name: Optional[str]=None, ns: Optional[Namespace]=None):
  if name is not None:
    ns = namespaces[name]

  globals_snapshot()
  if enable:
    try: 
      if ns is not None:
         ns.__dict__ = GDict(ns.__dict__.items())
         vars(__main__).update(ns.__dict__)
         yield ns
      else:
        yield None
        
    finally: 
      if ns is not None: 
        ns.__dict__ = dict(ns.__dict__.items())
      globals_restore()
  else:
    try: yield None
    finally: del G.__dict__
