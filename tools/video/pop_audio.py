#!/usr/bin/env python3
"""解説アニメ用の音（明るいポップなBGMと効果音）を numpy だけで合成する。外部の音源は使わない。

- bgm(dur): 120BPM・ヘ長調。I–V–vi–IV の進行で、木琴のような和音の刻み・ベース・手拍子・ハイハット・鉄琴のメロディ。
- sfx(events, dur): (秒, 種類) の並びから効果音を作る。種類: pop / whoosh / ding / coin / tick / click / chime / rise
- write(path, dur, events): BGM と効果音を混ぜて、ステレオの WAV に書き出す。
"""
import wave

import numpy as np

SR = 44100


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def _add(buf, start, v):
    a = int(start * SR)
    if a >= len(buf) or a + len(v) <= 0:
        return
    if a < 0:
        v = v[-a:]; a = 0
    e = min(len(buf), a + len(v))
    buf[a:e] += v[: e - a]


def pluck(f, dur=0.9, bright=1.0, decay=4.0):
    """木琴・ウクレレのような、はじく音（倍音ごとに減衰の速さを変える）"""
    t = np.arange(int(dur * SR)) / SR
    v = np.zeros_like(t)
    for k in range(1, 7):
        v += (bright ** (k - 1)) / k ** 1.3 * np.sin(2 * np.pi * f * k * t) * np.exp(-t * (decay + k * 2.2))
    return v * np.minimum(1.0, t / 0.004)


def glock(f, dur=1.2):
    t = np.arange(int(dur * SR)) / SR
    v = np.sin(2 * np.pi * f * t) * np.exp(-t * 3.0) + 0.35 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t * 7) + 0.15 * np.sin(2 * np.pi * f * 5.4 * t) * np.exp(-t * 12)
    return v * np.minimum(1.0, t / 0.002)


def kick():
    t = np.arange(int(0.35 * SR)) / SR
    ph = 2 * np.pi * np.cumsum(48 + 110 * np.exp(-t * 32)) / SR
    return np.sin(ph) * np.exp(-t * 9)


def _hp(x):
    return np.concatenate([[0], np.diff(x)])


def clap(rng):
    out = np.zeros(int(0.25 * SR))
    for o in (0.0, 0.011, 0.022):
        t = np.arange(int(0.2 * SR)) / SR
        n = _hp(rng.uniform(-1, 1, len(t))) * np.exp(-t * (40 if o < 0.02 else 16))
        a = int(o * SR); out[a:a + len(n)] += n[: len(out) - a]
    return out * 0.6


def hat(rng, open_=False):
    t = np.arange(int((0.18 if open_ else 0.05) * SR)) / SR
    return _hp(_hp(rng.uniform(-1, 1, len(t)))) * np.exp(-t * (18 if open_ else 70)) * 0.35


def bgm(dur):
    rng = np.random.default_rng(7)
    n = int(dur * SR) + SR
    L = np.zeros(n); R = np.zeros(n)
    beat = 60 / 120; bar = beat * 4; s16 = beat / 4
    prog = [(53, [65, 69, 72]), (48, [64, 67, 72]), (50, [65, 69, 74]), (46, [65, 70, 74])]  # F  C/E  Dm  B♭
    comp = [0, 3, 6, 8, 11, 14]
    bass = [0, 3, 6, 8, 10, 12, 14]
    # 鉄琴のメロディ（2小節で1まとまり。ヘ長調のペンタトニック）
    mel = [[(0, 77), (2, 79), (4, 81), (8, 84), (12, 81)], [(0, 79), (4, 77), (6, 74), (8, 77), (14, 72)],
           [(0, 77), (2, 79), (4, 81), (8, 84), (10, 86), (12, 84)], [(0, 81), (4, 79), (8, 77)]]
    nbar = int(dur / bar) + 1
    for b in range(nbar):
        t0 = b * bar
        root, ch = prog[b % 4]
        last = t0 > dur - bar * 1.2
        for p in comp:
            for j, m in enumerate(ch):
                v = pluck(hz(m), 0.5, 0.75, 7.0) * 0.055
                pan = 0.3 + 0.2 * j
                _add(L, t0 + p * s16 + j * 0.008, v * (1 - pan) * 1.4); _add(R, t0 + p * s16 + j * 0.008, v * pan * 1.4)
        if b >= 1:
            for p in bass:
                m = root - 12 + (12 if p in (6, 14) else 0)
                v = pluck(hz(m), 0.45, 0.5, 6.0) * 0.16
                _add(L, t0 + p * s16, v); _add(R, t0 + p * s16, v)
        if b >= 2 and not last:
            for p in (0, 8, 10):
                if p == 10 and b % 2 == 0:
                    continue
                v = kick() * 0.32; _add(L, t0 + p * s16, v); _add(R, t0 + p * s16, v)
            for p in (4, 12):
                v = clap(rng) * 0.42; _add(L, t0 + p * s16, v * 0.9); _add(R, t0 + p * s16, v)
            for p in range(0, 16, 2):
                v = hat(rng, open_=(p % 4 == 2 and p == 14)) * (0.55 if p % 4 else 0.35)
                _add(L, t0 + p * s16, v * 0.6); _add(R, t0 + p * s16, v)
        if b >= 4 and not last and (b // 8) % 2 == 0:
            for p, m in mel[b % 4]:
                v = glock(hz(m)) * 0.06
                _add(L, t0 + p * s16, v * 0.8); _add(R, t0 + p * s16, v * 1.1)
    # 軽い残響（ディレイ2本）
    d1, d2 = int(0.375 * SR), int(0.25 * SR)
    L2, R2 = L.copy(), R.copy()
    L2[d1:] += 0.18 * R[:-d1]; R2[d2:] += 0.18 * L[:-d2]
    m = int(dur * SR)
    L2, R2 = L2[:m], R2[:m]
    idx = np.arange(m)
    env = np.minimum(1.0, np.minimum(idx / int(0.3 * SR), (m - idx) / int(2.0 * SR)))
    return L2 * env, R2 * env


def _sweep(f0, f1, dur, shape=2.0):
    t = np.arange(int(dur * SR)) / SR
    f = f0 + (f1 - f0) * (t / dur) ** shape
    return np.sin(2 * np.pi * np.cumsum(f) / SR), t


def _lp(x, a):
    """一次のローパス（a: 0〜1、小さいほどこもる）。a は配列でもよい"""
    y = np.zeros_like(x); s = 0.0
    a = np.broadcast_to(a, x.shape)
    for i in range(len(x)):
        s += a[i] * (x[i] - s); y[i] = s
    return y


def sfx_sound(kind, rng):
    if kind == "pop":
        v, t = _sweep(260, 980, 0.09, 0.6)
        return v * np.exp(-t * 34) * 0.5
    if kind == "whoosh":
        t = np.arange(int(0.42 * SR)) / SR
        cut = 0.04 + 0.5 * np.sin(np.pi * t / 0.42) ** 2
        v = _lp(rng.uniform(-1, 1, len(t)), cut)
        return v * np.sin(np.pi * t / 0.42) ** 1.5 * 0.9
    if kind == "ding":
        return glock(hz(88), 1.0) * 0.32 + glock(hz(95), 1.0) * 0.12
    if kind == "coin":
        a = glock(hz(83), 0.12)[: int(0.08 * SR)]
        b = glock(hz(88), 0.6)
        return np.concatenate([a, b]) * 0.3
    if kind == "tick":
        t = np.arange(int(0.03 * SR)) / SR
        return _hp(rng.uniform(-1, 1, len(t))) * np.exp(-t * 160) * 0.35
    if kind == "click":
        t = np.arange(int(0.06 * SR)) / SR
        return (_hp(rng.uniform(-1, 1, len(t))) * np.exp(-t * 220) * 0.5 + np.sin(2 * np.pi * 180 * t) * np.exp(-t * 60) * 0.3)
    if kind == "chime":
        out = np.zeros(int(1.4 * SR))
        for j, m in enumerate((84, 88, 91, 96)):
            g = glock(hz(m), 1.0) * 0.16; a = int(j * 0.07 * SR); out[a:a + len(g)] += g[: len(out) - a]
        return out
    if kind == "rise":
        v, t = _sweep(220, 660, 1.4, 1.2)
        return v * np.sin(np.pi * t / 1.4) * 0.12
    raise ValueError(kind)


def sfx(events, dur):
    rng = np.random.default_rng(3)
    n = int(dur * SR)
    L = np.zeros(n); R = np.zeros(n)
    cache = {}
    for t0, kind in events:
        if kind not in cache or kind in ("whoosh", "tick", "click"):
            cache[kind] = sfx_sound(kind, rng)
        v = cache[kind]
        _add(L, t0, v); _add(R, t0, v)
    return L, R


def write(path, dur, events, bgm_gain=0.55):
    bl, br = bgm(dur)
    pk = max(np.abs(bl).max(), np.abs(br).max()) or 1
    sl, sr_ = sfx(events, dur)
    L = bl / pk * bgm_gain + sl
    R = br / pk * bgm_gain + sr_
    pk2 = max(np.abs(L).max(), np.abs(R).max(), 1.0)
    st = np.empty(len(L) * 2, dtype=np.int16)
    st[0::2] = np.clip(L / pk2 * 0.95, -1, 1) * 32767
    st[1::2] = np.clip(R / pk2 * 0.95, -1, 1) * 32767
    with wave.open(path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(st.tobytes())
