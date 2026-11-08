#!/usr/bin/env python3
"""サポートページ（support/<言語>/index.html と support/index.html）を作る。

使い方: python3 scripts/build-support.py

アプリの画面の文言（タブ名・ボタン名・「ファイル」アプリの場所など）は、アプリの
Shared/Localizable.xcstrings の各言語の訳に合わせてある。アプリの文言を変えたら、ここも合わせる。
"""
import html
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ISSUES = "https://github.com/Eiryyy/shrinkaway-site/issues"

# 各言語: name（言語名）, app（アプリ名）, title, contact（{issues} にリンク）, faq, qa（質問と答えの段落）
PAGES = {
    "ja": dict(
        name="日本語", app="消せる圧縮", title="サポート",
        contact="お問い合わせ",
        contact_body="不具合のご報告やご要望は、{issues} からお送りください（GitHub のアカウントが必要です。内容は公開されるため、個人情報は書かないでください）。",
        issues="GitHub の Issues",
        faq="よくある質問",
        qa=[
            ("「ファイル」に保存した画像はどこにありますか？",
             ["「ファイル」アプリ › このiPhone内（iPad では このiPad内）› 消せる圧縮 › 圧縮画像 にあります。Webサイトの「ファイルを選択」からも選べます。"]),
            ("保存した圧縮画像はいつ削除されますか？",
             ["「ファイル」に保存した画像は、「設定」で選んだ期限（1時間・24時間・7日間）を過ぎたあと、次にアプリを開いたときや切り替えて戻ったときに削除されます。「自動削除しない」も選べます。",
              "写真ライブラリに保存した画像は自動では削除されず、期限を過ぎると「管理」タブで削除をおすすめします。どちらも「管理」タブからいつでも削除できます。"]),
            ("写真ライブラリから削除した画像はどうなりますか？",
             ["写真アプリの「最近削除した項目」に移ります。本アプリは、自分が保存した圧縮画像であることを確かめてから削除するので、元の写真が削除されることはありません。"]),
            ("Pro 版を購入したのに使えません",
             ["「設定」タブの「購入を復元」をお試しください。購入時と同じ Apple アカウントでサインインしている必要があります。"]),
            ("写真へのアクセスを「制限付き」にしています",
             ["圧縮と保存は使えます。写真ライブラリから削除するときは、本アプリが保存した画像かどうかを確かめられない場合があり、その場合は安全のため削除しません。"]),
        ]),
    "en": dict(
        name="English", app="Shrinkaway", title="Support",
        contact="Contact",
        contact_body="To report a problem or send a request, please use {issues} (a GitHub account is required; issues are public, so please don’t include personal information).",
        issues="GitHub Issues",
        faq="FAQ",
        qa=[
            ("Where are the images I saved to Files?",
             ["In the Files app › On My iPhone (On My iPad on iPad) › Shrinkaway › Compressed Images. You can also pick them from “Choose File” on websites."]),
            ("When are saved images deleted?",
             ["Images saved to Files are deleted after the expiry period you choose in Settings (1 hour, 24 hours, or 7 days), the next time you open or return to the app. You can also choose “Never auto-delete.”",
              "Images saved to your Photo Library are not deleted automatically; once they expire, the Manage tab suggests deleting them. You can delete either kind anytime in the Manage tab."]),
            ("What happens to images deleted from my Photo Library?",
             ["They move to Recently Deleted in the Photos app. The app checks that each image is a compressed copy it saved before deleting it, so your original photos are never deleted."]),
            ("I bought Pro but it isn’t available",
             ["Tap Restore Purchase in the Settings tab. Make sure you’re signed in with the same Apple Account you used to buy it."]),
            ("I gave the app limited photo access",
             ["Compressing and saving work as usual. When deleting from your Photo Library, the app may not be able to confirm that an image is one it saved; in that case it won’t delete it, for safety."]),
        ]),
    "ko": dict(
        name="한국어", app="지우는 압축", title="지원",
        contact="문의",
        contact_body="문제 신고나 요청은 {issues}로 보내 주세요(GitHub 계정이 필요합니다. 내용이 공개되므로 개인 정보는 적지 마세요).",
        issues="GitHub Issues",
        faq="자주 묻는 질문",
        qa=[
            ("'파일'에 저장한 이미지는 어디에 있나요?",
             ["'파일' 앱 › 나의 iPhone(iPad에서는 나의 iPad) › 지우는 압축 › 압축 이미지에 있습니다. 웹 사이트의 '파일 선택'에서도 고를 수 있습니다."]),
            ("저장한 압축 이미지는 언제 삭제되나요?",
             ["'파일'에 저장한 이미지는 '설정'에서 고른 기한(1시간, 24시간, 7일)이 지난 뒤, 다음에 앱을 열거나 앱으로 돌아왔을 때 삭제됩니다. '자동 삭제 안 함'도 고를 수 있습니다.",
              "사진 보관함에 저장한 이미지는 자동으로 삭제되지 않으며, 기한이 지나면 '관리' 탭에서 삭제를 권합니다. 두 가지 모두 '관리' 탭에서 언제든지 삭제할 수 있습니다."]),
            ("사진 보관함에서 삭제한 이미지는 어떻게 되나요?",
             ["사진 앱의 '최근 삭제된 항목'으로 이동합니다. 이 앱은 자신이 저장한 압축 이미지인지 확인한 뒤에 삭제하므로 원본 사진이 삭제되는 일은 없습니다."]),
            ("Pro 버전을 구입했는데 사용할 수 없습니다",
             ["'설정' 탭의 '구입 항목 복원'을 눌러 보세요. 구입할 때와 같은 Apple 계정으로 로그인되어 있어야 합니다."]),
            ("사진 접근 권한을 '제한된 접근'으로 설정했습니다",
             ["압축과 저장은 그대로 사용할 수 있습니다. 사진 보관함에서 삭제할 때는 이 앱이 저장한 이미지인지 확인할 수 없는 경우가 있으며, 그럴 때는 안전을 위해 삭제하지 않습니다."]),
        ]),
    "zh-Hans": dict(
        name="简体中文", app="一次性压缩", title="支持",
        contact="联系我们",
        contact_body="如需报告问题或提出建议，请通过 {issues} 提交（需要 GitHub 账户；内容会公开，请勿填写个人信息）。",
        issues="GitHub Issues",
        faq="常见问题",
        qa=[
            ("存储到“文件”的图像在哪里？",
             ["在“文件”App › 我的 iPhone（iPad 上为我的 iPad）› 一次性压缩 › 压缩图像 中。也可以在网站的“选取文件”中选择。"]),
            ("存储的压缩图像什么时候删除？",
             ["存储到“文件”的图像会在超过“设置”中选择的期限（1 小时、24 小时或 7 天）后，于下次打开或切换回本 App 时删除。也可以选择“不自动删除”。",
              "存储到照片图库的图像不会自动删除；过期后，“管理”标签页会建议删除。两种图像都可以随时在“管理”标签页中删除。"]),
            ("从照片图库删除的图像会怎样？",
             ["会移到“照片”App 的“最近删除”中。本 App 会先确认图像是自己存储的压缩图像再删除，因此不会删除你的原始照片。"]),
            ("购买了 Pro 版却无法使用",
             ["请在“设置”标签页中轻点“恢复购买”。需要登录购买时使用的同一 Apple 账户。"]),
            ("我将照片访问权限设为了“受限访问”",
             ["压缩和存储可以照常使用。从照片图库删除时，本 App 有时无法确认图像是否由它存储；这种情况下，为安全起见不会删除。"]),
        ]),
    "zh-Hant": dict(
        name="繁體中文", app="一次性壓縮", title="支援",
        contact="聯絡我們",
        contact_body="如需回報問題或提出建議，請透過 {issues} 提交（需要 GitHub 帳號；內容會公開，請勿填寫個人資料）。",
        issues="GitHub Issues",
        faq="常見問題",
        qa=[
            ("儲存到「檔案」的影像在哪裡？",
             ["在「檔案」App › 我的 iPhone（iPad 上為我的 iPad）› 一次性壓縮 › 壓縮影像 中。也可以在網站的「選擇檔案」中選取。"]),
            ("儲存的壓縮影像何時刪除？",
             ["儲存到「檔案」的影像會在超過「設定」中選擇的期限（1 小時、24 小時或 7 天）後，於下次開啟或切換回本 App 時刪除。也可以選擇「不自動刪除」。",
              "儲存到照片圖庫的影像不會自動刪除；過期後，「管理」標籤頁會建議刪除。兩種影像都可以隨時在「管理」標籤頁中刪除。"]),
            ("從照片圖庫刪除的影像會怎樣？",
             ["會移到「照片」App 的「最近刪除」中。本 App 會先確認影像是自己儲存的壓縮影像再刪除，因此不會刪除你的原始照片。"]),
            ("購買了 Pro 版卻無法使用",
             ["請在「設定」標籤頁中點一下「恢復購買項目」。需要登入購買時使用的同一個 Apple 帳號。"]),
            ("我將照片取用權限設為「有限取用」",
             ["壓縮和儲存可以照常使用。從照片圖庫刪除時，本 App 有時無法確認影像是否由它儲存；這種情況下，為了安全不會刪除。"]),
        ]),
    "fr": dict(
        name="Français", app="Shrinkaway", title="Assistance",
        contact="Contact",
        contact_body="Pour signaler un problème ou faire une demande, utilisez les {issues} (un compte GitHub est nécessaire ; les tickets sont publics, n’y indiquez donc pas d’informations personnelles).",
        issues="GitHub Issues",
        faq="Questions fréquentes",
        qa=[
            ("Où se trouvent les images enregistrées dans Fichiers ?",
             ["Dans l’app Fichiers › Sur mon iPhone (Sur mon iPad sur iPad) › Shrinkaway › Images compressées. Vous pouvez aussi les choisir via « Choisir un fichier » sur les sites web."]),
            ("Quand les images enregistrées sont-elles supprimées ?",
             ["Les images enregistrées dans Fichiers sont supprimées une fois passé le délai choisi dans Réglages (1 heure, 24 heures ou 7 jours), la prochaine fois que vous ouvrez l’app ou y revenez. Vous pouvez aussi choisir « Jamais ».",
              "Les images enregistrées dans la Photothèque ne sont pas supprimées automatiquement ; une fois expirées, l’onglet Gérer propose de les supprimer. Vous pouvez supprimer les unes comme les autres à tout moment depuis l’onglet Gérer."]),
            ("Que deviennent les images supprimées de la Photothèque ?",
             ["Elles sont placées dans « Supprimés récemment » de l’app Photos. L’app vérifie que chaque image est une copie compressée qu’elle a enregistrée avant de la supprimer : vos photos originales ne sont jamais supprimées."]),
            ("J’ai acheté Pro, mais il n’est pas disponible",
             ["Touchez « Restaurer l’achat » dans l’onglet Réglages. Vous devez être connecté avec le même compte Apple que lors de l’achat."]),
            ("J’ai accordé un accès limité aux photos",
             ["La compression et l’enregistrement fonctionnent normalement. Lors d’une suppression dans la Photothèque, l’app peut ne pas pouvoir vérifier qu’une image a été enregistrée par elle ; dans ce cas, par sécurité, elle ne la supprime pas."]),
        ]),
    "es": dict(
        name="Español", app="Shrinkaway", title="Soporte",
        contact="Contacto",
        contact_body="Para informar de un problema o enviar una sugerencia, usa {issues} (se necesita una cuenta de GitHub; las incidencias son públicas, así que no incluyas datos personales).",
        issues="GitHub Issues",
        faq="Preguntas frecuentes",
        qa=[
            ("¿Dónde están las imágenes que guardé en Archivos?",
             ["En la app Archivos › En mi iPhone (En mi iPad en el iPad) › Shrinkaway › Imágenes comprimidas. También puedes elegirlas desde “Seleccionar archivo” en los sitios web."]),
            ("¿Cuándo se eliminan las imágenes guardadas?",
             ["Las imágenes guardadas en Archivos se eliminan cuando pasa el plazo que elegiste en Ajustes (1 hora, 24 horas o 7 días), la próxima vez que abres la app o vuelves a ella. También puedes elegir “Nunca”.",
              "Las imágenes guardadas en la Fototeca no se eliminan automáticamente; cuando caducan, la pestaña Gestionar te sugiere eliminarlas. Puedes eliminar ambas en cualquier momento desde la pestaña Gestionar."]),
            ("¿Qué pasa con las imágenes eliminadas de la Fototeca?",
             ["Pasan a “Eliminado” en la app Fotos. La app comprueba que cada imagen sea una copia comprimida que ella guardó antes de eliminarla, así que tus fotos originales nunca se eliminan."]),
            ("Compré Pro, pero no está disponible",
             ["Toca “Restaurar compra” en la pestaña Ajustes. Debes haber iniciado sesión con la misma cuenta de Apple que usaste para comprarlo."]),
            ("Le di a la app acceso limitado a las fotos",
             ["Comprimir y guardar funcionan con normalidad. Al eliminar de la Fototeca, puede que la app no pueda confirmar que una imagen la guardó ella; en ese caso, por seguridad, no la elimina."]),
        ]),
    "pt-BR": dict(
        name="Português (Brasil)", app="Shrinkaway", title="Suporte",
        contact="Contato",
        contact_body="Para relatar um problema ou enviar uma sugestão, use as {issues} (é preciso ter uma conta do GitHub; as issues são públicas, então não inclua informações pessoais).",
        issues="GitHub Issues",
        faq="Perguntas frequentes",
        qa=[
            ("Onde ficam as imagens que salvei no Arquivos?",
             ["No app Arquivos › No Meu iPhone (No Meu iPad no iPad) › Shrinkaway › Imagens Comprimidas. Você também pode escolhê-las em “Escolher Arquivo” nos sites."]),
            ("Quando as imagens salvas são apagadas?",
             ["As imagens salvas no Arquivos são apagadas depois do prazo escolhido em Ajustes (1 hora, 24 horas ou 7 dias), na próxima vez que você abrir ou voltar ao app. Você também pode escolher “Nunca”.",
              "As imagens salvas na Fototeca não são apagadas automaticamente; quando expiram, a aba Gerenciar sugere apagá-las. Você pode apagar as duas a qualquer momento na aba Gerenciar."]),
            ("O que acontece com as imagens apagadas da Fototeca?",
             ["Elas vão para “Apagados” no app Fotos. O app confirma que cada imagem é uma cópia comprimida que ele salvou antes de apagá-la, então suas fotos originais nunca são apagadas."]),
            ("Comprei o Pro, mas ele não está disponível",
             ["Toque em “Restaurar Compra” na aba Ajustes. É preciso estar conectado com a mesma Conta Apple usada na compra."]),
            ("Dei acesso limitado às fotos",
             ["Comprimir e salvar funcionam normalmente. Ao apagar da Fototeca, o app pode não conseguir confirmar que uma imagem foi salva por ele; nesse caso, por segurança, ele não a apaga."]),
        ]),
    "pt-PT": dict(
        name="Português (Portugal)", app="Shrinkaway", title="Suporte",
        contact="Contacto",
        contact_body="Para comunicar um problema ou enviar uma sugestão, utilize as {issues} (é necessária uma conta GitHub; as issues são públicas, por isso não inclua dados pessoais).",
        issues="GitHub Issues",
        faq="Perguntas frequentes",
        qa=[
            ("Onde estão as imagens que guardei em Ficheiros?",
             ["Na app Ficheiros › No meu iPhone (No meu iPad no iPad) › Shrinkaway › Imagens comprimidas. Também as pode escolher em “Escolher ficheiro” nos sites."]),
            ("Quando são apagadas as imagens guardadas?",
             ["As imagens guardadas em Ficheiros são apagadas depois do prazo escolhido em Definições (1 hora, 24 horas ou 7 dias), da próxima vez que abrir ou regressar à app. Também pode escolher “Nunca”.",
              "As imagens guardadas na Fototeca não são apagadas automaticamente; quando expiram, o separador Gerir sugere apagá-las. Pode apagar ambas a qualquer momento no separador Gerir."]),
            ("O que acontece às imagens apagadas da Fototeca?",
             ["Passam para “Apagados recentemente” na app Fotografias. A app confirma que cada imagem é uma cópia comprimida que guardou antes de a apagar, por isso as suas fotografias originais nunca são apagadas."]),
            ("Comprei o Pro, mas não está disponível",
             ["Toque em “Restaurar compra” no separador Definições. Tem de ter sessão iniciada com a mesma conta Apple utilizada na compra."]),
            ("Dei acesso limitado às fotografias",
             ["Comprimir e guardar funcionam normalmente. Ao apagar da Fototeca, a app pode não conseguir confirmar que uma imagem foi guardada por ela; nesse caso, por segurança, não a apaga."]),
        ]),
    "de": dict(
        name="Deutsch", app="Shrinkaway", title="Support",
        contact="Kontakt",
        contact_body="Probleme und Wünsche kannst du über {issues} melden (ein GitHub-Account ist erforderlich; Issues sind öffentlich, gib daher keine persönlichen Daten an).",
        issues="GitHub Issues",
        faq="Häufige Fragen",
        qa=[
            ("Wo sind die Bilder, die ich in Dateien gesichert habe?",
             ["In der App „Dateien“ › Auf meinem iPhone (auf dem iPad: Auf meinem iPad) › Shrinkaway › Komprimierte Bilder. Auf Websites kannst du sie auch über „Datei auswählen“ auswählen."]),
            ("Wann werden gesicherte Bilder gelöscht?",
             ["In Dateien gesicherte Bilder werden nach der in den Einstellungen gewählten Frist (1 Stunde, 24 Stunden oder 7 Tage) gelöscht, sobald du die App das nächste Mal öffnest oder zu ihr zurückkehrst. Du kannst auch „Nicht automatisch löschen“ wählen.",
              "In der Fotomediathek gesicherte Bilder werden nicht automatisch gelöscht; nach Ablauf schlägt der Tab „Verwalten“ vor, sie zu löschen. Beide Arten kannst du jederzeit im Tab „Verwalten“ löschen."]),
            ("Was passiert mit Bildern, die aus der Fotomediathek gelöscht werden?",
             ["Sie landen in der Fotos-App unter „Zuletzt gelöscht“. Die App prüft vor dem Löschen, ob es sich um eine von ihr gesicherte komprimierte Kopie handelt – deine Originalfotos werden also nie gelöscht."]),
            ("Ich habe Pro gekauft, kann es aber nicht nutzen",
             ["Tippe im Tab „Einstellungen“ auf „Kauf wiederherstellen“. Du musst mit demselben Apple Account angemeldet sein wie beim Kauf."]),
            ("Ich habe der App nur eingeschränkten Zugriff auf Fotos gegeben",
             ["Komprimieren und Sichern funktionieren wie gewohnt. Beim Löschen aus der Fotomediathek kann die App manchmal nicht prüfen, ob ein Bild von ihr gesichert wurde; dann löscht sie es sicherheitshalber nicht."]),
        ]),
    "it": dict(
        name="Italiano", app="Shrinkaway", title="Assistenza",
        contact="Contatti",
        contact_body="Per segnalare un problema o inviare una richiesta, usa le {issues} (serve un account GitHub; le issue sono pubbliche, quindi non inserire dati personali).",
        issues="GitHub Issues",
        faq="Domande frequenti",
        qa=[
            ("Dove si trovano le immagini salvate in File?",
             ["Nell’app File › Sul mio iPhone (Sul mio iPad su iPad) › Shrinkaway › Immagini compresse. Sui siti web puoi sceglierle anche con “Scegli file”."]),
            ("Quando vengono eliminate le immagini salvate?",
             ["Le immagini salvate in File vengono eliminate dopo la scadenza scelta in Impostazioni (1 ora, 24 ore o 7 giorni), la prossima volta che apri l’app o ci torni. Puoi anche scegliere “Non eliminare automaticamente”.",
              "Le immagini salvate nella Libreria foto non vengono eliminate automaticamente; alla scadenza, il pannello Gestisci suggerisce di eliminarle. Puoi eliminare entrambe in qualsiasi momento dal pannello Gestisci."]),
            ("Cosa succede alle immagini eliminate dalla Libreria foto?",
             ["Vengono spostate in “Eliminati di recente” nell’app Foto. L’app verifica che ogni immagine sia una copia compressa salvata da lei prima di eliminarla, quindi le tue foto originali non vengono mai eliminate."]),
            ("Ho acquistato Pro ma non è disponibile",
             ["Tocca “Ripristina acquisto” nel pannello Impostazioni. Devi aver effettuato l’accesso con lo stesso Account Apple usato per l’acquisto."]),
            ("Ho concesso all’app un accesso limitato alle foto",
             ["La compressione e il salvataggio funzionano normalmente. Quando elimini dalla Libreria foto, l’app potrebbe non riuscire a verificare che un’immagine sia stata salvata da lei; in tal caso, per sicurezza, non la elimina."]),
        ]),
    "nl": dict(
        name="Nederlands", app="Shrinkaway", title="Ondersteuning",
        contact="Contact",
        contact_body="Meld problemen of wensen via {issues} (een GitHub-account is vereist; issues zijn openbaar, dus vermeld geen persoonlijke gegevens).",
        issues="GitHub Issues",
        faq="Veelgestelde vragen",
        qa=[
            ("Waar staan de afbeeldingen die ik in Bestanden heb bewaard?",
             ["In de app Bestanden › Op mijn iPhone (op de iPad: Op mijn iPad) › Shrinkaway › Gecomprimeerde afbeeldingen. Op websites kun je ze ook kiezen via ‘Kies bestand’."]),
            ("Wanneer worden bewaarde afbeeldingen verwijderd?",
             ["Afbeeldingen in Bestanden worden verwijderd na de termijn die je in Instellingen kiest (1 uur, 24 uur of 7 dagen), zodra je de app weer opent of ernaar terugkeert. Je kunt ook ‘Niet automatisch verwijderen’ kiezen.",
              "Afbeeldingen in de fotobibliotheek worden niet automatisch verwijderd; na het verlopen stelt het tabblad Beheer voor ze te verwijderen. Beide soorten kun je altijd verwijderen via het tabblad Beheer."]),
            ("Wat gebeurt er met afbeeldingen die uit de fotobibliotheek worden verwijderd?",
             ["Ze gaan naar ‘Recent verwijderd’ in de Foto’s-app. De app controleert vóór het verwijderen of een afbeelding een gecomprimeerde kopie is die zij zelf heeft bewaard, dus je originele foto’s worden nooit verwijderd."]),
            ("Ik heb Pro gekocht, maar het werkt niet",
             ["Tik in het tabblad Instellingen op ‘Herstel aankoop’. Je moet zijn ingelogd met hetzelfde Apple Account als bij de aankoop."]),
            ("Ik heb de app beperkte toegang tot foto’s gegeven",
             ["Comprimeren en bewaren werken gewoon. Bij verwijderen uit de fotobibliotheek kan de app soms niet controleren of een afbeelding door haar is bewaard; dan verwijdert ze die voor de zekerheid niet."]),
        ]),
    "pl": dict(
        name="Polski", app="Shrinkaway", title="Pomoc",
        contact="Kontakt",
        contact_body="Problemy i sugestie zgłaszaj przez {issues} (wymagane jest konto GitHub; zgłoszenia są publiczne, więc nie podawaj danych osobowych).",
        issues="GitHub Issues",
        faq="Najczęstsze pytania",
        qa=[
            ("Gdzie są zdjęcia zapisane w aplikacji Pliki?",
             ["W aplikacji Pliki › Na moim iPhonie (na iPadzie: Na moim iPadzie) › Shrinkaway › Skompresowane zdjęcia. Na stronach internetowych możesz je też wybrać przyciskiem „Wybierz plik”."]),
            ("Kiedy zapisane zdjęcia są usuwane?",
             ["Zdjęcia zapisane w Plikach są usuwane po upływie terminu wybranego w Ustawieniach (1 godzina, 24 godziny lub 7 dni), przy następnym otwarciu aplikacji lub powrocie do niej. Możesz też wybrać „Bez automatycznego usuwania”.",
              "Zdjęcia zapisane w bibliotece zdjęć nie są usuwane automatycznie; po wygaśnięciu karta Zarządzaj proponuje ich usunięcie. Oba rodzaje możesz w każdej chwili usunąć na karcie Zarządzaj."]),
            ("Co się dzieje ze zdjęciami usuniętymi z biblioteki zdjęć?",
             ["Trafiają do albumu „Ostatnio usunięte” w aplikacji Zdjęcia. Przed usunięciem aplikacja sprawdza, czy to skompresowana kopia, którą sama zapisała, więc Twoje oryginalne zdjęcia nigdy nie są usuwane."]),
            ("Kupiłem/kupiłam Pro, ale nie działa",
             ["Stuknij „Przywróć zakup” na karcie Ustawienia. Musisz być zalogowany(-a) na to samo konto Apple, którego użyto przy zakupie."]),
            ("Dałem/dałam aplikacji ograniczony dostęp do zdjęć",
             ["Kompresowanie i zapisywanie działają normalnie. Przy usuwaniu z biblioteki zdjęć aplikacja czasem nie może sprawdzić, czy zdjęcie zapisała ona; wtedy dla bezpieczeństwa go nie usuwa."]),
        ]),
    "ru": dict(
        name="Русский", app="Shrinkaway", title="Поддержка",
        contact="Связаться с нами",
        contact_body="Сообщить о проблеме или отправить пожелание можно через {issues} (нужна учетная запись GitHub; обращения публичны, поэтому не указывайте личные данные).",
        issues="GitHub Issues",
        faq="Частые вопросы",
        qa=[
            ("Где изображения, сохраненные в «Файлы»?",
             ["В приложении «Файлы» › «На iPhone» (на iPad — «На iPad») › Shrinkaway › Сжатые изображения. Их также можно выбрать на сайтах с помощью кнопки «Выбрать файл»."]),
            ("Когда удаляются сохраненные изображения?",
             ["Изображения в «Файлах» удаляются по истечении срока, выбранного в настройках (1 час, 24 часа или 7 дней), когда вы в следующий раз откроете приложение или вернетесь в него. Можно также выбрать «Не удалять автоматически».",
              "Изображения в медиатеке автоматически не удаляются; по истечении срока вкладка «Управление» предлагает их удалить. Оба вида можно удалить в любое время на вкладке «Управление»."]),
            ("Что происходит с изображениями, удаленными из медиатеки?",
             ["Они перемещаются в альбом «Недавно удаленные» приложения «Фото». Перед удалением приложение проверяет, что это сжатая копия, сохраненная им самим, поэтому ваши оригинальные фото никогда не удаляются."]),
            ("Я купил(а) Pro, но он недоступен",
             ["Нажмите «Восстановить покупку» на вкладке «Настройки». Нужно войти в ту же учетную запись Apple, с которой была сделана покупка."]),
            ("Я предоставил(а) приложению ограниченный доступ к фото",
             ["Сжатие и сохранение работают как обычно. При удалении из медиатеки приложение иногда не может проверить, что изображение сохранено им; в таком случае оно в целях безопасности его не удаляет."]),
        ]),
    "tr": dict(
        name="Türkçe", app="Shrinkaway", title="Destek",
        contact="İletişim",
        contact_body="Sorun bildirmek veya istekte bulunmak için {issues} sayfasını kullanın (GitHub hesabı gerekir; kayıtlar herkese açıktır, bu yüzden kişisel bilgi yazmayın).",
        issues="GitHub Issues",
        faq="Sık sorulan sorular",
        qa=[
            ("Dosyalar’a kaydettiğim görüntüler nerede?",
             ["Dosyalar uygulaması › iPhone’umda (iPad’de iPad’imde) › Shrinkaway › Sıkıştırılmış Görüntüler. Web sitelerinde “Dosya Seç” ile de seçebilirsiniz."]),
            ("Kaydedilen görüntüler ne zaman silinir?",
             ["Dosyalar’a kaydedilen görüntüler, Ayarlar’da seçtiğiniz süre (1 saat, 24 saat veya 7 gün) dolduktan sonra, uygulamayı bir sonraki açışınızda veya uygulamaya döndüğünüzde silinir. “Otomatik silme kapalı” seçeneğini de seçebilirsiniz.",
              "Fotoğraf Arşivi’ne kaydedilen görüntüler otomatik olarak silinmez; süreleri dolunca Yönet sekmesi silmenizi önerir. Her ikisini de istediğiniz zaman Yönet sekmesinden silebilirsiniz."]),
            ("Fotoğraf Arşivi’nden silinen görüntülere ne olur?",
             ["Fotoğraflar uygulamasındaki “Son Silinenler”e taşınır. Uygulama, silmeden önce görüntünün kendi kaydettiği sıkıştırılmış bir kopya olduğunu doğrular; bu yüzden orijinal fotoğraflarınız asla silinmez."]),
            ("Pro’yu satın aldım ama kullanamıyorum",
             ["Ayarlar sekmesinde “Satın Alımı Geri Yükle”ye dokunun. Satın alırken kullandığınız Apple Hesabı ile oturum açmış olmanız gerekir."]),
            ("Uygulamaya fotoğraflara sınırlı erişim verdim",
             ["Sıkıştırma ve kaydetme normal şekilde çalışır. Fotoğraf Arşivi’nden silerken uygulama, bir görüntüyü kendisinin kaydettiğini bazen doğrulayamayabilir; bu durumda güvenlik için silmez."]),
        ]),
    "id": dict(
        name="Bahasa Indonesia", app="Shrinkaway", title="Dukungan",
        contact="Kontak",
        contact_body="Untuk melaporkan masalah atau mengirim permintaan, gunakan {issues} (memerlukan akun GitHub; laporan bersifat publik, jadi jangan cantumkan informasi pribadi).",
        issues="GitHub Issues",
        faq="Pertanyaan umum",
        qa=[
            ("Di mana gambar yang saya simpan ke File?",
             ["Di app File › Di iPhone Saya (Di iPad Saya pada iPad) › Shrinkaway › Gambar Terkompresi. Anda juga dapat memilihnya melalui “Pilih File” di situs web."]),
            ("Kapan gambar yang disimpan dihapus?",
             ["Gambar yang disimpan ke File dihapus setelah jangka waktu yang Anda pilih di Pengaturan (1 jam, 24 jam, atau 7 hari) berlalu, saat Anda membuka atau kembali ke app berikutnya. Anda juga dapat memilih “Jangan hapus otomatis”.",
              "Gambar yang disimpan ke Perpustakaan Foto tidak dihapus otomatis; setelah kedaluwarsa, tab Kelola menyarankan untuk menghapusnya. Keduanya dapat Anda hapus kapan saja di tab Kelola."]),
            ("Apa yang terjadi pada gambar yang dihapus dari Perpustakaan Foto?",
             ["Gambar dipindahkan ke “Baru Dihapus” di app Foto. App ini memastikan bahwa setiap gambar adalah salinan terkompresi yang disimpannya sebelum menghapus, sehingga foto asli Anda tidak pernah terhapus."]),
            ("Saya sudah membeli Pro tetapi tidak bisa digunakan",
             ["Ketuk “Pulihkan Pembelian” di tab Pengaturan. Anda harus masuk dengan Akun Apple yang sama dengan yang digunakan saat membeli."]),
            ("Saya memberi app akses terbatas ke foto",
             ["Kompresi dan penyimpanan tetap berfungsi seperti biasa. Saat menghapus dari Perpustakaan Foto, app mungkin tidak dapat memastikan bahwa gambar disimpan olehnya; dalam hal itu, demi keamanan, gambar tidak dihapus."]),
        ]),
    "th": dict(
        name="ไทย", app="บีบอัดแล้วลบ", title="ฝ่ายสนับสนุน",
        contact="ติดต่อเรา",
        contact_body="หากต้องการแจ้งปัญหาหรือส่งคำขอ โปรดใช้ {issues} (ต้องมีบัญชี GitHub และเนื้อหาจะเป็นสาธารณะ จึงไม่ควรใส่ข้อมูลส่วนตัว)",
        issues="GitHub Issues",
        faq="คำถามที่พบบ่อย",
        qa=[
            ("รูปภาพที่บันทึกไว้ใน \"ไฟล์\" อยู่ที่ไหน",
             ["อยู่ในแอปไฟล์ › บน iPhone ของฉัน (บน iPad คือ บน iPad ของฉัน) › บีบอัดแล้วลบ › รูปภาพบีบอัด และยังเลือกได้จาก \"เลือกไฟล์\" บนเว็บไซต์"]),
            ("รูปภาพบีบอัดที่บันทึกไว้จะถูกลบเมื่อใด",
             ["รูปภาพที่บันทึกไว้ใน \"ไฟล์\" จะถูกลบหลังจากพ้นระยะเวลาที่เลือกไว้ใน \"การตั้งค่า\" (1 ชั่วโมง, 24 ชั่วโมง หรือ 7 วัน) เมื่อคุณเปิดแอปหรือสลับกลับมาที่แอปครั้งถัดไป และยังเลือก \"ไม่ลบอัตโนมัติ\" ได้",
              "รูปภาพที่บันทึกไว้ในคลังรูปภาพจะไม่ถูกลบอัตโนมัติ เมื่อพ้นกำหนดแล้วแท็บ \"จัดการ\" จะแนะนำให้ลบ ทั้งสองแบบลบได้ทุกเมื่อจากแท็บ \"จัดการ\""]),
            ("รูปภาพที่ลบออกจากคลังรูปภาพจะเป็นอย่างไร",
             ["จะย้ายไปที่ \"ที่เพิ่งลบ\" ในแอปรูปภาพ แอปนี้จะตรวจสอบก่อนลบว่าเป็นรูปภาพบีบอัดที่แอปบันทึกไว้เอง ดังนั้นรูปภาพต้นฉบับของคุณจะไม่ถูกลบ"]),
            ("ซื้อรุ่น Pro แล้วแต่ใช้ไม่ได้",
             ["แตะ \"กู้คืนการซื้อ\" ในแท็บ \"การตั้งค่า\" โดยต้องลงชื่อเข้าด้วยบัญชี Apple เดียวกับที่ใช้ซื้อ"]),
            ("ฉันให้สิทธิ์เข้าถึงรูปภาพแบบจำกัด",
             ["การบีบอัดและการบันทึกใช้งานได้ตามปกติ เมื่อลบออกจากคลังรูปภาพ แอปอาจตรวจสอบไม่ได้ว่ารูปภาพนั้นบันทึกโดยแอปหรือไม่ ในกรณีนั้นแอปจะไม่ลบเพื่อความปลอดภัย"]),
        ]),
    "vi": dict(
        name="Tiếng Việt", app="Nén rồi xóa", title="Hỗ trợ",
        contact="Liên hệ",
        contact_body="Để báo lỗi hoặc gửi yêu cầu, vui lòng dùng {issues} (cần có tài khoản GitHub; nội dung được công khai nên đừng ghi thông tin cá nhân).",
        issues="GitHub Issues",
        faq="Câu hỏi thường gặp",
        qa=[
            ("Ảnh tôi đã lưu vào Tệp nằm ở đâu?",
             ["Trong ứng dụng Tệp › Trên iPhone (trên iPad là Trên iPad) › Nén rồi xóa › Ảnh nén. Bạn cũng có thể chọn chúng từ “Chọn tệp” trên các trang web."]),
            ("Khi nào ảnh đã lưu bị xóa?",
             ["Ảnh lưu vào Tệp sẽ bị xóa sau thời hạn bạn chọn trong Cài đặt (1 giờ, 24 giờ hoặc 7 ngày), vào lần tiếp theo bạn mở hoặc quay lại ứng dụng. Bạn cũng có thể chọn “Không tự động xóa”.",
              "Ảnh lưu vào Thư viện ảnh không bị xóa tự động; khi hết hạn, tab Quản lý sẽ đề xuất xóa. Bạn có thể xóa cả hai loại bất cứ lúc nào trong tab Quản lý."]),
            ("Ảnh bị xóa khỏi Thư viện ảnh sẽ ra sao?",
             ["Chúng được chuyển vào “Đã xóa gần đây” trong ứng dụng Ảnh. Ứng dụng kiểm tra rằng mỗi ảnh là bản sao đã nén do chính nó lưu trước khi xóa, nên ảnh gốc của bạn không bao giờ bị xóa."]),
            ("Tôi đã mua Pro nhưng không dùng được",
             ["Chạm vào “Khôi phục giao dịch mua” trong tab Cài đặt. Bạn cần đăng nhập bằng cùng Tài khoản Apple đã dùng để mua."]),
            ("Tôi đã cho ứng dụng quyền truy cập ảnh giới hạn",
             ["Việc nén và lưu vẫn hoạt động bình thường. Khi xóa khỏi Thư viện ảnh, ứng dụng có thể không xác nhận được ảnh có phải do nó lưu hay không; khi đó, để an toàn, ứng dụng sẽ không xóa."]),
        ]),
}

ORDER = ["ja", "en", "ko", "zh-Hans", "zh-Hant", "fr", "es", "pt-BR", "pt-PT", "de", "it", "nl", "pl", "ru", "tr", "id", "th", "vi"]
# 追加の言語は scripts/support/<言語>.json（PAGES の各要素と同じ形）に置く
SUPPORT_DIR = os.path.join(ROOT, "scripts", "support")
if os.path.isdir(SUPPORT_DIR):
    for fn in sorted(os.listdir(SUPPORT_DIR)):
        if fn.endswith(".json"):
            code = fn[:-5]
            with open(os.path.join(SUPPORT_DIR, fn), encoding="utf-8") as f:
                PAGES[code] = json.load(f)
            ORDER.append(code)
RTL = {"ar", "he", "ur"}
assert sorted(ORDER) == sorted(PAGES)

e = html.escape


def lang_nav(current, prefix):
    links = []
    for code in ORDER:
        name = e(PAGES[code]["name"])
        if code == current:
            links.append(f'<strong lang="{code}">{name}</strong>')
        else:
            links.append(f'<a href="{prefix}{code}/" lang="{code}" hreflang="{code}">{name}</a>')
    return '<nav class="langs">' + "".join(links) + "</nav>"


def section(code):
    p = PAGES[code]
    link = f'<a href="{ISSUES}">{e(p["issues"])}</a>'
    body = e(p["contact_body"]).replace("{issues}", link)
    dir_attr = ' dir="rtl"' if code in RTL else ""
    out = [f'<section class="lang" lang="{code}"{dir_attr}>', f'  <h2>{e(p["contact"])}</h2>', f"  <p>{body}</p>", f'  <h2>{e(p["faq"])}</h2>']
    for q, answers in p["qa"]:
        out.append(f"  <h3>{e(q)}</h3>")
        out += [f"  <p>{e(a)}</p>" for a in answers]
    out.append("</section>")
    return "\n".join(out)


def alternates(prefix):
    return "\n".join(f'<link rel="alternate" hreflang="{c}" href="{prefix}{c}/">' for c in ORDER)


def page(code):
    p = PAGES[code]
    return f"""<!doctype html>
<html lang="{code}"{' dir="rtl"' if code in RTL else ''}>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(p["title"])} - {e(p["app"])}</title>
<link rel="stylesheet" href="../../style.css">
{alternates("../")}
</head>
<body>
<main>
  <header><a href="../../">← {e(p["app"])}</a></header>
  <h1>{e(p["title"])}</h1>
  {lang_nav(code, "../")}
{section(code)}
</main>
</body>
</html>
"""


def index():
    # 以前からの URL（App Store Connect に登録済み）。日本語と英語の内容を載せ、ほかの言語へのリンクを付ける
    return f"""<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>サポート / Support - 消せる圧縮 / Shrinkaway</title>
<link rel="stylesheet" href="../style.css">
{alternates("")}
</head>
<body>
<main>
  <header><a href="../">← 消せる圧縮 / Shrinkaway</a></header>
  <h1>サポート<br>Support</h1>
  {lang_nav(None, "")}
{section("ja")}
{section("en")}
</main>
</body>
</html>
"""


for code in ORDER:
    d = os.path.join(ROOT, "support", code)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
        f.write(page(code))
with open(os.path.join(ROOT, "support", "index.html"), "w", encoding="utf-8") as f:
    f.write(index())
print(f"{len(ORDER)} 言語 + support/index.html")
