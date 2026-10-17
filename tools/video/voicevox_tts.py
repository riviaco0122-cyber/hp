#!/usr/bin/env python3
"""VOICEVOX（voicevox_core）でセリフを音声にする。同じセリフ・声は作り直さない（キャッシュ）。

準備（一度だけ。GitHub のリリースから取る。合計で約300MB）:
  VOICEVOX_DIR（既定 /tmp/vv）に次を置く
  - voicevox_core の Python パッケージ（voicevox_core-0.16.x-...whl を pip install）
  - voicevox_onnxruntime-linux-x64-1.17.3/lib/libvoicevox_onnxruntime.so（VOICEVOX/onnxruntime-builder）
  - open_jtalk_dic_utf_8-1.11/（r9y9/open_jtalk）
  - models/<番号>.vvm（VOICEVOX/voicevox_vvm。使う声の入ったものだけでよい）
利用条件: 作った音声を使うときは「VOICEVOX:キャラクター名」のクレジットが要る（各キャラクターの規約に従う）。
"""
import hashlib, os, subprocess

VV = os.environ.get("VOICEVOX_DIR", "/tmp/vv")
_syn = None


def _synth(models):
    global _syn
    if _syn is None:
        from voicevox_core.blocking import Onnxruntime, OpenJtalk, Synthesizer, VoiceModelFile
        ort = Onnxruntime.load_once(filename=os.path.join(VV, "voicevox_onnxruntime-linux-x64-1.17.3", "lib", "libvoicevox_onnxruntime.so"))
        _syn = Synthesizer(ort, OpenJtalk(os.path.join(VV, "open_jtalk_dic_utf_8-1.11")))
        for m in models:
            with VoiceModelFile.open(os.path.join(VV, "models", f"{m}.vvm")) as f:
                _syn.load_voice_model(f)
    return _syn


def tts(text, style, models, cache, speed=1.0, pitch=0.0, intonation=1.0):
    """text を style（スタイルID）の声で WAV にし、(ファイル, 秒) を返す。前後の無音は切る"""
    os.makedirs(cache, exist_ok=True)
    key = hashlib.sha1(f"{style}|{speed}|{pitch}|{intonation}|{text}".encode()).hexdigest()[:16]
    raw, out = os.path.join(cache, key + "_raw.wav"), os.path.join(cache, key + ".wav")
    if not os.path.exists(out):
        syn = _synth(models)
        q = syn.create_audio_query(text, style)
        q.speed_scale, q.pitch_scale, q.intonation_scale = speed, pitch, intonation
        q.pre_phoneme_length, q.post_phoneme_length = 0.05, 0.05
        open(raw, "wb").write(syn.synthesis(q, style))
        trim = "silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0.02"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-af", f"{trim},areverse,{trim},areverse", "-ar", "44100", "-ac", "1", out], check=True)
    d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", out], capture_output=True, text=True, check=True).stdout)
    return out, d
