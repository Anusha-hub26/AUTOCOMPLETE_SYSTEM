from collections import defaultdict


class TrieNode:
    def __init__(self):
        self.children = {}
        self.top_k = []


class AutocompleteSystem:
    def __init__(self, k=3):
        self.root = TrieNode()
        self.k = k
        self.freq_map = defaultdict(int)

    def insert(self, word: str, freq: int = 1):
        self.freq_map[word] += freq

        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()

            node = node.children[char]
            self._update_top_k(node, word)

    def _update_top_k(self, node, word):
        if word not in node.top_k:
            node.top_k.append(word)

        node.top_k.sort(key=lambda w: (-self.freq_map[w], w))

        if len(node.top_k) > self.k:
            node.top_k.pop()

    def search(self, prefix: str):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        return node.top_k

    def select(self, word):
        # simulate user selecting suggestion
        self.insert(word, 1)

    def delete(self, word):
        if word in self.freq_map:
            del self.freq_map[word]
            print(f"[DELETED] {word}")
        else:
            print("[ERROR] Word not found.")

    def show_all(self):
        print("\n=== WORD DATABASE ===")
        for word, freq in sorted(self.freq_map.items(), key=lambda x: (-x[1], x[0])):
            print(f"{word} (freq: {freq})")
        print("=====================\n")


# ------------------------
# INTERACTIVE PROGRAM
# ------------------------

if __name__ == "__main__":

    print("==== AUTOCOMPLETE SYSTEM ====")
    k = int(input("Enter Top-K suggestions limit: "))
    auto = AutocompleteSystem(k)

    while True:
        print("""
Commands:
1. insert  -> Add word
2. search  -> Get suggestions
3. select  -> Select suggestion (increase freq)
4. delete  -> Delete word
5. show    -> Show all words
6. exit
""")

        command = input("Enter command: ").strip().lower()

        if command == "insert":
            word = input("Enter word: ").strip()
            freq = int(input("Enter frequency: "))
            auto.insert(word, freq)
            print(f"[INSERTED] {word} (freq: {auto.freq_map[word]})")

        elif command == "search":
            prefix = input("Enter prefix: ").strip()
            suggestions = auto.search(prefix)
            print("Suggestions:", suggestions)

        elif command == "select":
            word = input("Enter selected word: ").strip()
            auto.select(word)
            print(f"[UPDATED] {word} (freq: {auto.freq_map[word]})")

        elif command == "delete":
            word = input("Enter word to delete: ").strip()
            auto.delete(word)

        elif command == "show":
            auto.show_all()

        elif command == "exit":
            print("Exiting system.")
            break

        else:
            print("Invalid command.")