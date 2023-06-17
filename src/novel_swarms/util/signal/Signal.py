

class Signal:
    def __init__(self, start=None):
        self.hist = [] if start is None else start
        self.sig_pattern = None

    def sig(self, val):
        self.hist.append(val)

    def kmp_search(self, pat, txt):
        """
        KMP Search is adapted from Code writen by Bhavya Jain
        (https://www.geeksforgeeks.org/kmp-algorithm-for-pattern-searching/)
        """
        M = len(pat)
        N = len(txt)

        # create lps[] that will hold the longest prefix suffix
        # values for pattern
        lps = [0] * M
        j = 0  # index for pat[]

        # Preprocess the pattern (calculate lps[] array)
        self.compute_lsp_array(pat, M, lps)

        i = 0  # index for txt[]
        while (N - i) >= (M - j):
            if pat[j] == txt[i]:
                i += 1
                j += 1

            if j == M:
                print("Found pattern at index " + str(i - j))
                j = lps[j - 1]

            # mismatch after j matches
            elif i < N and pat[j] != txt[i]:
                # Do not match lps[0..lps[j-1]] characters,
                # they will match anyway
                if j != 0:
                    j = lps[j - 1]
                else:
                    i += 1

    def compute_lsp_array(self, pat, M, lps):
        """
        LPS Array is adapted from Code writen by Bhavya Jain
        (https://www.geeksforgeeks.org/kmp-algorithm-for-pattern-searching/)
        """
        _len = 0
        lps[0] = 0
        i = 1
        while i < M:
            if pat[i] == pat[_len]:
                _len += 1
                lps[i] = _len
                i += 1
            else:
                if _len != 0:
                    _len = lps[_len - 1]
                else:
                    lps[i] = 0
                    i += 1

