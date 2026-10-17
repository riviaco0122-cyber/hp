#!/usr/bin/env bash
# 動画づくりに使う VOICEVOX（voicevox_core 0.16.4）を VOICEVOX_DIR（既定 /tmp/vv）に用意する。
# 定期実行（新しいコンテナ）の最初に1回だけ実行する。すでにあるものは取り直さない。
# 使う声のモデル: 0（ずんだもん）4（玄野武宏・剣崎雌雄）6（No.7）12（雀松朱司・麒ヶ島宗麟）15（青山龍星・もち子さん・小夜）
set -euo pipefail
VV="${VOICEVOX_DIR:-/tmp/vv}"
V=0.16.4
mkdir -p "$VV/models"
cd "$VV"
dl() { [ -s "$2" ] || curl -sSfL --retry 4 -o "$2" "$1"; }
dl "https://github.com/VOICEVOX/voicevox_core/releases/download/$V/voicevox_core-$V-cp310-abi3-manylinux_2_34_x86_64.whl" "voicevox_core-$V-cp310-abi3-manylinux_2_34_x86_64.whl"
python3 -c "import voicevox_core" 2>/dev/null || python3 -m pip install -q "voicevox_core-$V-cp310-abi3-manylinux_2_34_x86_64.whl" || python3 -m pip install -q --break-system-packages "voicevox_core-$V-cp310-abi3-manylinux_2_34_x86_64.whl"
if [ ! -d voicevox_onnxruntime-linux-x64-1.17.3 ]; then
  dl "https://github.com/VOICEVOX/onnxruntime-builder/releases/download/voicevox_onnxruntime-1.17.3/voicevox_onnxruntime-linux-x64-1.17.3.tgz" ort.tgz
  tar xzf ort.tgz
fi
if [ ! -d open_jtalk_dic_utf_8-1.11 ]; then
  dl "https://github.com/r9y9/open_jtalk/releases/download/v1.11.1/open_jtalk_dic_utf_8-1.11.tar.gz" dic.tgz
  tar xzf dic.tgz
fi
for m in 0 4 6 9 10 12 14 15 19; do
  dl "https://github.com/VOICEVOX/voicevox_vvm/releases/download/$V/$m.vvm" "models/$m.vvm"
done
echo "VOICEVOX の準備ができました: $VV"
