#!/usr/bin/env bash
# 本番ブランチを作業ブランチに取り込み、衝突を自動で直す（日次サイクルの最後・PR を出す前に必ず実行）。
# 直し方: docs/seo/log.md は両方の記録を残す／docs/dashboard.md は作り直す／生成物は build.py で作り直す。
# それ以外のファイルが衝突したら止まって報告する（人の判断が要る）。
set -u
BASE=$(git ls-remote --symref origin HEAD | awk '/^ref:/{sub("refs/heads/","",$2); print $2}')
git fetch -q origin "$BASE" || { echo "fetch に失敗"; exit 1; }
if git merge-base --is-ancestor "origin/$BASE" HEAD; then echo "取り込み済み（衝突なし）"; exit 0; fi
git merge --no-edit "origin/$BASE" >/dev/null 2>&1
CONF=$(git diff --name-only --diff-filter=U)
if [ -z "$CONF" ]; then echo "取り込み完了（衝突なし）"; exit 0; fi
OTHER=""
for f in $CONF; do
  case "$f" in
    docs/seo/log.md|docs/seo/calendar.md|docs/seo/keywords.md|docs/seo/plan-tracking.md)
      python3 - "$f" <<'PY'
import re,sys
p=sys.argv[1]; s=open(p).read()
s=re.sub(r"<<<<<<< [^\n]*\n(.*?)=======\n(.*?)>>>>>>> [^\n]*\n", lambda m:m.group(1)+m.group(2), s, flags=re.S)
open(p,'w').write(s)
PY
      git add "$f";;
    docs/dashboard.md|docs/site-spec.md|js/media-index.js|seo/*|pages/*|llms.txt)
      git checkout --theirs -- "$f" 2>/dev/null; git add "$f";;
    *) OTHER="$OTHER $f";;
  esac
done
if [ -n "$OTHER" ]; then echo "自動で直せない衝突:$OTHER（人に報告する）"; exit 2; fi
python3 tools/build.py >/dev/null && python3 tools/build_dashboard.py >/dev/null
git add -A
git commit -q -m "本番ブランチを取り込み、衝突を自動で解消（log 等は両方残し、生成物は作り直し）" && echo "衝突を自動で解消した"
if grep -rlE '^(<<<<<<<|>>>>>>>) ' docs tools pages .claude 2>/dev/null | head -1 | grep -q .; then echo "衝突マーカーが残っている"; exit 2; fi
