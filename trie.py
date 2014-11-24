class Trie:
  def __init__(self, isRoot=False, cacheOn=True):
    """Constructs a Trie instance. If isRoot is set to True, treats
    this Trie instance as the root. If cacheOn is set to True,
    caches will be maintained for word and prefix lookups. If cacheOn
    is set to True, isRoot must be set accordingly as well."""
    self.isRoot = isRoot
    self.cacheOn = cacheOn
    if isRoot:
      self.wordCache = {}
      self.prefixCache = {}
    self.children = {}
    self.isWord = False

  def importWords(self, filepath):
    """Given a filepath to a file of words separated by newlines,
    adds all the words to the trie.""" 
    for raw_word in open(filepath, 'r'):
      word = raw_word.strip(' ').strip('\n').upper()
      self.add(word)

  def add(self, s):
    """Add the string `s` in this subtree."""
    head, tail = s[0], s[1:]
    if head not in self.children:
      self.children[head] = Trie(isRoot=False, cacheOn=self.cacheOn)
    next_node = self.children[head]
    if not tail: # no further recursion
      next_node.isWord = True
    else:
      self.children[head].add(tail)

  def containsWord(self, s):
    if self.isRoot:
      if s not in self.wordCache:
        self.wordCache[s] = self._containsWordCompute(s)
      return self.wordCache[s]
    else:
      return self._containsWordCompute(s)

  def containsPrefix(self, s):
    if self.isRoot:
      if s not in self.prefixCache:
        self.prefixCache[s] = self._containsPrefixCompute(s)
      return self.prefixCache[s]
    else:
      return self._containsPrefixCompute(s)

  def _containsWordCompute(self, s):
    """Returns true if the string `s` is contained
    in the trie."""      
    if not s:
      return self.isWord
    head, tail = s[0], s[1:]
    if head not in self.children:
      return False
    next_node = self.children[head]
    return next_node.containsWord(tail)

  def _containsPrefixCompute(self, s):
    """Check whether the given string `s` is a prefix of
    some member string."""
    if not s:
      return True
    head, tail = s[0], s[1:]
    if head not in self.children:
      return False
    next_node = self.children[head]
    return next_node.containsPrefix(tail)
