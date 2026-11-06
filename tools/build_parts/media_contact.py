# -*- coding: utf-8 -*-
# build.py の一部：アキヤド：お問い合わせ・送信完了のページ。
# 単独では動かない。build.py が決まった順番で読み込み、1つのファイルとして実行する
# （ほかの部分の関数・定数はそのまま使える。import は不要）。

# ---------------------------------------------------------------- アキヤド：お問い合わせ（コーポレートとは別の、アキヤド専用のページ）
MEDIA_CONTACT_TOPICS = [
    ("sell", "アキヤド買取プラン（空き家を売りたい）",
     "【買取について】\n・売りたい物件：\n・空き家になった時期：\n・気になっていること（例：古くて売れるか不安）：\n"),
    ("use operation", "アキヤド借り上げプラン（空き家を活かしたい）",
     "【借り上げについて】\n・活かしたい物件：\n・家を残したい理由や、将来使う予定：\n・気になっていること（例：改修の費用）：\n"),
    ("side management", "アキヤド開業・運営プラン（民泊・小さな宿をはじめたい）",
     "【開業・運営について】\n・物件の有無（ある／探している）：\n・はじめたい宿のイメージ：\n・ご予算の目安：\n・自分で運営に関わりたい範囲：\n"),
    # 「サービス資料がほしい」の文言は tools/forms/Code.gs の DOC_REQUEST_VALUES（資料の自動添付の判定）と一致させる
    ("document", "サービス資料がほしい", "【資料について】\nサービス資料を希望します。\n"),
    ("other", "まだ決めていない・その他", "【ご相談】\n・いまの状況：\n・聞いてみたいこと：\n"),
]
MEDIA_CONTACT_SOURCES = ["検索（Google・Yahoo!など）", "AI（ChatGPTなど）", "SNS", "知人の紹介", "不動産会社・専門家の紹介", "その他"]


def media_contact_page():
    topics = "\n".join(
        f'              <label class="mform__check"><input type="checkbox" name="ご相談の内容" value="{e(t)}" data-keys="{k}" data-template="{e(tpl)}"><span>{e(t)}</span></label>'
        for k, t, tpl in MEDIA_CONTACT_TOPICS)
    def select(id_, name, label, options):
        opts = "".join(f'<option value="{e(o)}">{e(o)}</option>' for o in options)
        return f"""          <div class="mform__field">
            <label for="{id_}">{label} <span class="mform__opt">任意</span></label>
            <div class="select"><select id="{id_}" name="{name}"><option value="" selected>選択してください</option>{opts}</select></div>
          </div>"""
    prop = "\n".join([
        select("m-type", "物件の種類", "物件の種類", ["一戸建て", "古民家", "マンション・アパート", "土地", "まだ物件はない", "その他"]),
        select("m-state", "物件の状況", "物件の状況", ["空き家になっている", "住んでいる・使っている", "相続の手続き中", "購入を検討している", "その他"]),
        select("m-age", "築年数の目安", "築年数の目安", ["20年未満", "20〜40年", "40年以上", "わからない"]),
        select("m-when", "ご検討の時期", "ご検討の時期", ["すぐにでも", "3か月以内", "半年〜1年以内", "まだ決めていない"]),
    ])
    contact_ways = "".join(f'<label class="mform__radio"><input type="radio" name="ご希望の連絡方法" value="{w}"{" checked" if i == 0 else ""}><span>{w}</span></label>' for i, w in enumerate(["メール", "電話", "オンライン面談"]))
    sources = "".join(f'<option value="{e(x)}">{e(x)}</option>' for x in MEDIA_CONTACT_SOURCES)
    crumbs = media_crumbs([("アキヤド", "media.html"), ("無料相談・お問い合わせ", "")])
    body = f"""{media_hero("Contact", "無料相談・お問い合わせ", "空き家の売却・活用、民泊の開業について、アキヤドが無料でご相談に乗ります。まだ決めていない段階でも大丈夫です。2営業日以内に、メールでご連絡します。", crumbs)}

    <section class="section msec msec--first">
      <div class="container mform-wrap">
        <ul class="mcta__points mform__points reveal"><li>相談・お見積りは無料</li><li>全国対応・オンライン可</li><li>しつこい営業はしません</li></ul>
        <form class="mform reveal" action="https://script.google.com/macros/s/AKfycbx-SeTX9iRu6f45DUkCBj28vYeyQZnXH-958CJ6XYU0y7Ie1Pn1hDV1ahcyxWaBX3Uc/exec" method="POST" enctype="multipart/form-data" data-thanks="thanks.html">
          <input type="text" name="_hp" class="hp-field" tabindex="-1" autocomplete="off" data-lpignore="true" data-1p-ignore aria-hidden="true">
          <input type="hidden" name="_subject" value="【アキヤド】無料相談・お問い合わせ">
          <input type="hidden" name="流入元" id="from-field" value="">
          <div class="mform__field">
            <label for="m-name">お名前 <span class="mform__req">必須</span></label>
            <input type="text" id="m-name" name="name" placeholder="山田 太郎" autocomplete="name" required>
          </div>
          <div class="mform__field">
            <label for="m-email">メールアドレス <span class="mform__req">必須</span></label>
            <input type="email" id="m-email" name="email" placeholder="your@email.com" autocomplete="email" required>
          </div>
          <div class="mform__field">
            <label for="m-tel">電話番号 <span class="mform__req">必須</span></label>
            <input type="tel" id="m-tel" name="tel" placeholder="090-1234-5678" autocomplete="tel" inputmode="tel" pattern="[0-9０-９+\\-－ー\\(\\)（） ]{{10,}}" title="電話番号を数字で入力してください（例：090-1234-5678）" required>
            <p class="mform__help">ご連絡は、ご希望の方法（メール・お電話）でいたします。</p>
          </div>
          <fieldset class="mform__field">
            <legend>ご相談の内容 <span class="mform__opt">複数選択可</span></legend>
            <div class="mform__checks">
{topics}
            </div>
          </fieldset>
          <fieldset class="mform__field">
            <legend>ご希望の連絡方法</legend>
            <div class="mform__radios">{contact_ways}</div>
          </fieldset>
          <p class="mform__group">物件について <span>わかる範囲で大丈夫です</span></p>
          <div class="mform__field">
            <label for="m-place">物件の所在地 <span class="mform__opt">任意</span></label>
            <input type="text" id="m-place" name="物件の所在地" placeholder="例：静岡県下田市（市区町村まででも大丈夫です）">
          </div>
{prop}
          <div class="mform__field">
            <label for="m-message">ご相談の詳細 <span class="mform__opt">任意</span></label>
            <textarea id="m-message" name="message" rows="5" placeholder="物件の状況や、気になっていることをご自由にお書きください。上の「ご相談の内容」を選ぶと、書き方の例が入ります。"></textarea>
          </div>
          <div class="mform__field">
            <label for="m-file">ファイル <span class="mform__opt">任意</span></label>
{file_box("attachment", "ファイルを添付する", "写真・図面など（複数可）", "image/*,.pdf,.doc,.docx,.xls,.xlsx", attrs='id="m-file" multiple', cls="file--compact")}
            <p class="mform__help">物件の写真や図面があれば添付してください（合計10MBまで）。</p>
          </div>
          <div class="mform__field">
            <label for="m-source">アキヤドを知ったきっかけ <span class="mform__opt">任意</span></label>
            <div class="select"><select id="m-source" name="知ったきっかけ"><option value="" selected>選択してください</option>{sources}</select></div>
          </div>
          <div class="mform__consent">
            <label class="mform__agree"><input type="checkbox" name="プライバシーポリシーへの同意" value="同意する" required><span><a href="privacy.html" target="_blank" rel="noopener">プライバシーポリシー</a>に同意する <span class="mform__req">必須</span></span></label>
            <div class="mform__optin">
              <label class="mform__agree"><input type="checkbox" name="newsletter" value="希望する"><span>{NEWSLETTER_LABEL} <span class="mform__opt">任意</span></span></label>
              <p class="mform__optin-note">{NEWSLETTER_NOTE}</p>
            </div>
          </div>
          <button type="submit" class="mbtn mform__submit">【無料】相談・お問い合わせをする {ARROW}</button>
          <p class="mform__note">ご提案まではすべて無料です。内容を見てから、進めるかどうかを決めていただけます。</p>
        </form>
        <p class="mform__corp reveal">アキヤドは、合同会社RIVIA&amp;CO.が運営しています。不動産会社様との協業や、WEB集客・採用のご相談は<a href="CORP_CONTACT">RIVIA&amp;CO.のお問い合わせ</a>からお願いします。</p>
      </div>
    </section>"""
    page("media/contact.html", "無料相談・お問い合わせ｜アキヤド",
         "アキヤドへの無料相談・お問い合わせ。空き家の買取・借り上げ、民泊の開業・運営について、相談・お見積りは無料です。全国対応・オンライン可。",
         body, current="media", jsonld=[{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "アキヤド", "item": f"{SITE}/media.html"}, {"@type": "ListItem", "position": 2, "name": "無料相談・お問い合わせ", "item": f"{SITE}/media/contact.html"}]}])


def media_thanks_page():
    body = f"""{media_hero("Thank you", "送信が完了しました", "お問い合わせいただき、ありがとうございます。内容を確認のうえ、2営業日以内にメールでご連絡します。")}

    <section class="section msec msec--first">
      <div class="container mform-wrap">
        <p class="mform__help mthanks__note">連絡が届かない場合は、迷惑メールフォルダもご確認ください。</p>
        <div class="msv-band__btns mthanks__btns">
          <a href="media.html" class="mbtn">アキヤドのトップへ {ARROW}</a>
          <a href="media/learn.html" class="mbtn mbtn--sub">基礎から学ぶ {ARROW}</a>
        </div>
      </div>
    </section>
    <script>
      // 相談か資料請求かを lead_type で区別（lead は js/main.js が付ける）
      if (typeof gtag === 'function') {{ gtag('event', 'generate_lead', {{ form_type: 'akiyado', lead_type: new URLSearchParams(location.search).get('lead') || 'consult' }}); }}
    </script>"""
    page("media/thanks.html", "送信完了｜アキヤド", "アキヤドへのお問い合わせを受け付けました。", body, current="media", noindex=True)
