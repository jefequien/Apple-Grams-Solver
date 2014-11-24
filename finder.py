from trie import *
def findPossParents(word, parents):
  possParents = []
  for parent in parents:
    compare = word
    containsAllLetters = True
    for char in parent:
      if char in compare:
        index = compare.index(char)
        compare = compare[:index] + compare[index+1:]
      else:
        containsAllLetters = False
    if containsAllLetters:
      possParents += [(parent, compare)]
  return possParents

class Finder:
  def __init__(self, trie):
    self.trie = trie
    self.results = []

  def find(self, chars):
    self._findSub(self.trie, '', chars)

  def _findSub(self, curr_trie, curr_str, chars):
    # Check if curr_str is a word
    if curr_trie.isWord:
      self.results.append(curr_str)

    # Call _findSub on the children as long as the prefix exists
    done_chars = set()

    for i in range(len(chars)):
      char = chars[i]

      if char in done_chars:
        continue

      done_chars.add(char)

      rest_chars = chars[:i] + chars[i+1:]

      if char == '*':  # wildcard
        for child in curr_trie.children:
          next_trie = curr_trie.children[child]
          self._findSub(next_trie, curr_str + child, rest_chars)
        continue

      if char in curr_trie.children:
        next_trie = curr_trie.children[char]
        self._findSub(next_trie, curr_str + char, rest_chars)

  def goodWords(self, length, word):
    bestWords = []
    for w in self.results:
      compare = w
      containsAllLetters = True
      for char in word:
        if char in compare:
          index = compare.index(char)
          compare = compare[:index] + compare[index+1:]
        else:
          containsAllLetters = False
      if containsAllLetters:
        if length < len(w):
          if w[:len(w)-1] != word:
            bestWords += [w]
    return bestWords


  def printSummary(self):
    # Consolidate by number of letters, and sort within each category
    results_by_num_letters = []
    for i in range(20):
      results_by_num_letters.append([])

    for result in self.results:
      length = len(result)
      results_by_num_letters[length].append(result)

    for i in range(20):
      curr_results = results_by_num_letters[i]
      if len(curr_results) > 0:
        curr_results.sort()

        print '%d letter words:' % i
        print curr_results

def loadWords(filepath):
  trie = Trie(isRoot=True, cacheOn=True)
  trie.importWords(filepath)
  return trie

if __name__ == '__main__':
  print '\nLoading dictionary of words...'
  trie = loadWords('./dictionary.txt')
  print 'Dictionary loaded!'

  board = ''#raw_input("\n What is the board? \n").upper()''
  wordsraw = raw_input("\n What are the words?\n")
  words = wordsraw.split()
  words = [word.upper() for word in words]

  while True:
    # prompt user for letters on board
    raw = raw_input("\nPlease enter the letter(s):\n")
    search_str = raw.strip(' ,').upper()
    board += search_str
    choices = []
    print 'Board: ', board
    for word in words:
      finder = Finder(trie)
      finder.find(word + board)
      choices += finder.goodWords(len(word), word)
    if len(board) >= 4:
      finder = Finder(trie)
      finder.find(board)
      choices += finder.goodWords(3, '')
    choices.sort(key = len)
    choices = choices[::-1]
    print 'Words: ', words
    print 'Choices: ', choices
    
    if len(choices) != 0:
      raw2 = raw_input("What word do you want? \n")
      if raw2 != '':
        if raw2.upper() in choices:
          NoParent = False
          possParents = findPossParents(raw2.upper(),words)
          if len(possParents) == 1:
            parent,chars = possParents[0]
          elif len(possParents) == 0:
            chars = raw2.upper()
            NoParent = True
          else:
            print [p[0] for p in possParents]
            question = raw_input("Which Parent? \n")
            if question.upper() in [p[0] for p in possParents]:
              for p in possParents:
                if p[0] == question.upper():
                  parent,chars = p
            else:
              print 'error'

          words += [raw2.upper()]
          if not NoParent:
            words.remove(parent)
            NoParent = False

          for char in chars:
           index = board.index(char)
           board = board[:index] + board[index+1:]

          print 'Words: ', words
        else:
          print 'Not possible'


