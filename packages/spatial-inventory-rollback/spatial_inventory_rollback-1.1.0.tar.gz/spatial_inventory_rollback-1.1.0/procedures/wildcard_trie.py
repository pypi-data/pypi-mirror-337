from typing import Sequence


class TrieNode:
    def __init__(self, wildcard):
        self._children = {}
        self._value = None
        self._wildcard = wildcard

    def find(self, token):
        return self._children.get(token, None)

    def get(self, token, allow_wildcard=True) -> "TrieNode":
        match = self.find(token)
        if match is None:
            if allow_wildcard:
                wildcard_match = self.find(self._wildcard)
                if wildcard_match is None:
                    return None
                return wildcard_match
        return match

    def add(self, token) -> None:
        self._children[token] = TrieNode(self._wildcard)

    def get_value(self):
        return self._value

    def set_value(self, value):
        self._value = value


class Trie:
    def __init__(self, wildcard):
        self.wildcard = wildcard
        self.root = TrieNode(wildcard)

    def _find(
        self,
        node: TrieNode,
        key: Sequence,
        best_match_only: bool,
        include_score: bool,
        include_match: bool,
    ) -> list:
        results = []
        self._recursive_search(
            node,
            0,
            key,
            results,
            0,
            [0],
            best_match_only,
            include_score,
            include_match,
            [],
        )
        if results:
            return results
        return []

    def _create_results_dict(
        self,
        score: int,
        value,
        match: list,
        include_score: bool,
        include_match: bool,
    ):
        result = {"value": value}
        if include_match:
            result["match"] = match
        if include_score:
            result["score"] = score
        return result

    def _recursive_search(
        self,
        node: TrieNode,
        depth: int,
        search: Sequence,
        results: list,
        branch_score: int,
        best_score: int,
        best_match_only: bool,
        include_score: bool,
        include_match: bool,
        branch_match: list,
    ):
        if search[depth] == self.wildcard:
            children = node._children.items()
        else:
            children = []
            if search[depth] in node._children:
                children.append((search[depth], node._children[search[depth]]))
            if self.wildcard in node._children:
                children.append((self.wildcard, node._children[self.wildcard]))

        for k, v in children:
            if (
                search[depth] == k
                or k == self.wildcard
                or search[depth] == self.wildcard
            ):
                if include_match:
                    match = branch_match.copy()
                    match.append(k)
                else:
                    match = None

                if search[depth] == k:
                    score = branch_score + 1
                else:
                    score = branch_score
                if score > best_score[0]:
                    best_score[0] = score
                if v.get_value() is not None:
                    if best_match_only:
                        if branch_score > best_score[0] or not results:
                            results.clear()
                            results.append(
                                self._create_results_dict(
                                    score,
                                    v.get_value(),
                                    match,
                                    include_score,
                                    include_match,
                                )
                            )
                    else:
                        results.append(
                            self._create_results_dict(
                                score,
                                v.get_value(),
                                match,
                                include_score,
                                include_match,
                            )
                        )

                else:
                    self._recursive_search(
                        v,
                        depth + 1,
                        search,
                        results,
                        score,
                        best_score,
                        best_match_only,
                        include_score,
                        include_match,
                        match,
                    )

    def _insert(self, root: TrieNode, key, value):
        curr_node = root
        i = 0
        while i < len(key):
            token = key[i]
            n = curr_node.get(token, allow_wildcard=False)

            if n is not None:
                curr_node = n
                i += 1
            else:
                break
        while i < len(key):
            token = key[i]
            curr_node.add(token)
            curr_node = curr_node.get(token)
            i += 1
        curr_node.set_value(value)

    def find(
        self,
        key: Sequence,
        best_match_only: bool = True,
        include_score: bool = False,
        include_match: bool = False,
    ):
        return self._find(
            self.root, key, best_match_only, include_score, include_match
        )

    def insert(self, key: Sequence, value):
        return self._insert(self.root, key, value)
