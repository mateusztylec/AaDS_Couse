#!/usr/bin/python
# -*- coding: utf-8 -*-
def naiwna(S: str, W: str):
    word_find = 0
    i = 0
    m = 0
    comp_count = 0
    flag = True
    S_len = len(S)
    while m < S_len:
        for i in range(len(W)):
            comp_count += 1
            if W[i] != S[m + i]:
                break
        else:
            word_find += 1

        m += 1
    return word_find, comp_count


def rabin_karpa(S: str, W: str):
    d = 256
    q = 101
    hW = hash(W, d, q)
    h = 1
    comp_count = 0
    col_count = q
    find_count = 0
    M: int = len(S)
    N: int = len(W)
    for i in range(N - 1):
        h = (h * d) % q
    hS = hash(S[0:N], d, q)
    for m in range(M - N + 1):
        if m > 0:
            hS = (d * (hS - ord(S[m - 1]) * h) + ord(S[m + N - 1])) % q
            # hS = hash(S[m:N+m], d, q)
        if hS < 0:
            hS += q
        comp_count += 1
        if hS == hW:
            if S[m:m + N] == W:
                find_count += 1
            else:
                col_count += 1
    return find_count, comp_count, col_count


def hash(word, d, q):
    hw = 0
    for i in range(len(word)):  # N - to długość wzorca
        hw = (hw * d + ord(word[
                               i])) % q  # dla d będącego potęgą 2 można mnożenie zastąpić shiftem uzyskując pewne przyspieszenie obliczeń
    return hw


def kmp_search(S: str, W: str):
    m = 0
    i = 0
    P = []
    T = kmp_table(W)
    S_len = len(S)
    comp_count = 0
    while m < S_len:
        if W[i] == S[m]:
            comp_count += 1
            m += 1  # index in S
            i += 1  # index in W
            if i == len(W):
                P.append(m - i)
                i = T[i]
        else:
            i = T[i]
            if i < 0:
                m += 1
                i += 1
    return len(P), comp_count


def kmp_table(W):
    pos = 1
    cnd = 0
    T = [0] * (len(W) + 1)
    T[0] = -1
    while pos < len(W):
        if W[pos] == W[cnd]:
            T[pos] = T[cnd]
        else:
            T[pos] = cnd
            while cnd >= 0 and W[pos] != W[cnd]:
                cnd = T[cnd]
        pos += 1
        cnd += 1
    T[pos] = cnd
    return T


if __name__ == "__main__":
    with open("lotr.txt", encoding='utf-8') as f:
        text = f.readlines()
    S = ' '.join(text).lower()
    x1, y1 = naiwna(S, 'time.')
    print(f"{x1};{y1}")

    x2, y2, z2 = rabin_karpa(S, 'time.')
    print(f"{x2};{y2};{z2}")

    x3, y3 = kmp_search(S, 'time.')
    print("{};{}".format(x3, y3))
