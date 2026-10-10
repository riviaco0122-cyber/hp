#!/usr/bin/env bash
# コミット前の鍵の混入チェック（日次サイクルで git add の後・git commit の前に実行する）。
#
# 使い方: bash tools/check_secrets.sh
#   ステージ済みの変更（git diff --cached）で「追加された行」に、鍵・トークンらしい文字列があれば
#   該当ファイル名を出して終了コード 1。なければ 0。
#
# 見るもの（下の PATTERN）: サービスアカウント JSON の秘密鍵の項目名、PEM の秘密鍵の見出し、
#   Google の API キー（AIza で始まる39字前後）、サービスアカウントのメールアドレス、
#   GitHub のトークン（classic と fine-grained の接頭辞）。
# ※ このファイル自身が引っかからないよう、パターンは [_] などで書いている（意味は同じ）。
#   このファイルのコメントにも、パターンに一致する文字列をそのまま書かないこと。
set -u
cd "$(git rev-parse --show-toplevel)" || exit 2

PATTERN='private[_]key|BEGIN PRIVATE[ ]KEY|AIza[0-9A-Za-z_-]{30,}|client[_]email.*iam[.]gserviceaccount|gh[p]_|github[_]pat_'

found=0
while IFS= read -r -d '' f; do
  hits=$(git diff --cached --no-color --no-ext-diff -U0 -- "$f" | grep -E '^\+' | grep -vE '^\+\+\+ ' | grep -cE "$PATTERN")
  if [ "${hits:-0}" -gt 0 ]; then
    echo "鍵・トークンらしい文字列: $f（${hits} 行）" >&2
    found=1
  fi
done < <(git diff --cached --name-only -z --diff-filter=ACMR)

if [ "$found" -ne 0 ]; then
  echo "コミットを中止してください。該当ファイルを git restore --staged で外し、鍵は環境変数から読むように直す。" >&2
  exit 1
fi
echo "check_secrets: 問題なし"
exit 0
