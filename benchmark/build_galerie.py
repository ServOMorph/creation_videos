import html
import json
import shutil
from pathlib import Path

from bench_wangp import I2V_CASES, T2V_CASES

PROMPTS_FR = {
    1: "Un chat roux assis sur un rebord de fenêtre dans la douce lumière du matin, il tourne lentement la tête vers la caméra. Plan fixe, réaliste.",
    2: "Travelling avant dans une forêt brumeuse à l'aube, rayons de soleil filtrant entre les arbres. Cinématographique.",
    3: "Une femme marche dans une rue pluvieuse la nuit, néons reflétés sur le sol mouillé. Cinématographique, réaliste.",
    4: "Des vagues se brisent sur des rochers au ralenti, eau et écume détaillées. Réaliste.",
    5: "Gros plan extrême d'une montre mécanique dont les rouages tournent, éclairage studio. Macro, net.",
}
I2V_PROMPTS_FR = {
    1: "La femme cligne lentement des yeux et sourit légèrement. Mouvement naturel et subtil, caméra fixe.",
    2: "Les nuages avancent lentement dans le ciel et les hautes herbes ondulent sous le vent. Caméra fixe.",
    3: "L'homme fait quelques pas vers la caméra. Marche naturelle, caméra fixe.",
    4: "L'oiseau déploie ses ailes et s'envole de la branche. Mouvement naturel.",
    5: "Des passants marchent sur le trottoir et des voitures roulent dans la rue. Caméra fixe.",
}
IMAGE_PROMPTS_FR = {
    1: "Photo en gros plan d'une jeune femme aux cheveux auburn, lumière naturelle douce de fenêtre, expression calme et neutre, yeux ouverts regardant la caméra, réaliste, détails nets.",
    2: "Photo de paysage large : prairie verte aux hautes herbes sous un ciel bleu avec de grands nuages blancs, collines au loin, lumière dorée de fin de journée, réaliste.",
    3: "Photo en pied d'un homme en veste sombre debout sur un trottoir de ville vide, face à la caméra, centré, lumière du jour, réaliste.",
    4: "Photo d'un petit oiseau perché sur une branche, ailes repliées, arrière-plan vert flou, lumière douce du matin, réaliste, net.",
    5: "Photo d'une rue de ville animée avec des piétons sur le trottoir et des voitures sur la chaussée, immeubles de chaque côté, de jour, vue de caméra fixe, réaliste.",
}
CRITERIA = ["Fidelite au prompt", "Coherence temporelle", "Qualite du mouvement", "Absence d'artefacts"]
KEEP = {"t2v", "i2v", "t2v_vitesse", "i2v_vitesse"}
SUFFIX_EN = "Cars drive forward in the direction they face. Everything moves at normal real-time speed, not slow motion."
SUFFIX_FR = "Les voitures avancent dans le sens où elles font face. Tout bouge à vitesse normale, en temps réel, pas au ralenti."
ROOT = Path(__file__).parent
OUT = ROOT / "galerie"
RAW = ROOT / "resultats_raw.jsonl"
IMG_EXT = {".png", ".jpg", ".jpeg", ".webp"}

I2V_LABELS = {
    1: "Portrait : clignement des yeux, leger sourire",
    2: "Paysage : nuages, herbe au vent",
    3: "Personnage en pied : quelques pas vers la camera",
    4: "Animal : un oiseau prend son envol",
    5: "Scene urbaine : passants et voitures, camera fixe",
}
T2V_LABELS = {
    1: "Chat roux sur un rebord de fenetre",
    2: "Travelling avant, foret brumeuse",
    3: "Femme dans une rue pluvieuse la nuit",
    4: "Vagues sur des rochers, ralenti",
    5: "Gros plan d'une montre mecanique",
}


def collect():
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "images").mkdir(parents=True)
    (OUT / "videos").mkdir()
    images = []
    src_images = ROOT / "images"
    if src_images.exists():
        for f in sorted(src_images.iterdir()):
            if f.suffix.lower() in IMG_EXT:
                shutil.copy2(f, OUT / "images" / f.name)
                images.append({"file": "images/" + f.name, "name": f.stem})
    videos = []
    if RAW.exists():
        for line in RAW.read_text(encoding="ascii").splitlines():
            if not line.strip():
                continue
            r = json.loads(line)
            if r["model"] not in KEEP:
                continue
            for i, p in enumerate(r.get("files", [])):
                src = Path(p)
                if not src.exists():
                    continue
                dst = "%s_case%s_%s%s" % (r["model"], r["case"], i, src.suffix)
                shutil.copy2(src, OUT / "videos" / dst)
                videos.append(
                    {
                        "file": "videos/" + dst,
                        "model": r["model"],
                        "case": r["case"],
                        "seconds": r.get("seconds"),
                        "vram": r.get("vram_max_mib"),
                        "errors": r.get("errors", []),
                    }
                )
    return images, videos


def render(images, videos):
    e = html.escape
    def card(v):
        meta = "%s s" % v["seconds"] if v["seconds"] is not None else ""
        if v["vram"]:
            meta += " - VRAM max %s Mio" % v["vram"]
        is_i2v = v["model"].startswith("i2v")
        fix = v["model"].endswith("_vitesse")
        prompt = (I2V_CASES if is_i2v else T2V_CASES).get(v["case"], (None, ""))[1]
        if fix:
            prompt += " " + SUFFIX_EN
        key = "%s_%s" % (v["model"], v["case"])
        rating = "".join(
            '<div class="crit"><span>%s</span><span class="btns">%s</span></div>'
            % (
                label,
                "".join(
                    '<button type="button" data-k="%s" data-c="%d" data-v="%d">%d</button>'
                    % (e(key), ci, n, n)
                    for n in range(4)
                ),
            )
            for ci, label in enumerate(CRITERIA)
        )
        return (
            '<figure class="vid" data-key="%s" data-model="%s" data-case="%s">'
            '<video src="%s" controls loop muted preload="metadata"></video>'
            "<figcaption><b>%s</b> - cas %s - %s"
            '<p class="prompt">%s</p><details><summary>Prompt envoyé au modèle (anglais)</summary>'
            '<p class="prompt">%s</p></details>%s</figcaption></figure>'
            % (
                e(key), e(v["model"]), v["case"], e(v["file"]), e(v["model"]), v["case"], e(meta),
                e((I2V_PROMPTS_FR if is_i2v else PROMPTS_FR).get(v["case"], prompt) + (" " + SUFFIX_FR if fix else "")), e(prompt), rating,
            )
        )
    i2v = {v["case"]: v for v in videos if v["model"] == "i2v"}
    i2v_fix = {v["case"]: v for v in videos if v["model"] == "i2v_vitesse"}
    pairs = ""
    for n, i in enumerate(images, 1):
        pairs += (
            '<div class="pair"><figure><img src="%s" alt="%s" loading="lazy"><figcaption>Image de reference %d : %s<p class="prompt">%s</p></figcaption></figure>%s</div>'
            % (e(i["file"]), e(i["name"]), n, e(I2V_LABELS.get(n, "")), e(IMAGE_PROMPTS_FR.get(n, "")), (card(i2v[n]) if n in i2v else ""))
        )
    img_html = pairs or '<p class="vide">Aucune image de reference pour le moment.</p>'
    vid_html = "".join(card(v) for v in sorted((v for v in videos if v["model"] == "t2v"), key=lambda v: v["case"]))
    fix_html = "".join(card(v) for v in videos if v["model"].endswith("_vitesse"))
    if not vid_html:
        vid_html = '<p class="vide">Aucune video generee pour le moment.</p>'
    return """<!DOCTYPE html>
<html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Benchmark videos IA - images et videos</title>
<style>
:root{color-scheme:light dark;--bg:#fff;--fg:#1a1a1a;--mut:#6b6b6b;--card:#f3f3f1}
@media(prefers-color-scheme:dark){:root{--bg:#161616;--fg:#eee;--mut:#9a9a9a;--card:#232323}}
body{margin:0;padding:16px;background:var(--bg);color:var(--fg);font:16px/1.4 system-ui,sans-serif}
h1{font-size:20px;margin:0 0 4px}h2{font-size:17px;margin:24px 0 8px}
.sub{color:var(--mut);margin:0 0 8px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:12px}
figure{margin:0;background:var(--card);border-radius:8px;overflow:hidden}
img,video{display:block;width:100%%;height:auto}
figcaption{padding:8px 10px;font-size:14px}
.vide{color:var(--mut)}
.pair{display:flex;flex-direction:column;gap:8px}
.prompt{margin:6px 0;color:var(--mut);font-size:13px;font-style:italic}
.crit{display:flex;justify-content:space-between;align-items:center;gap:8px;margin-top:6px;font-size:13px}
.btns{display:flex;gap:4px}
.btns button{min-width:34px;min-height:34px;border:1px solid var(--mut);border-radius:6px;background:transparent;color:var(--fg);font:inherit;cursor:pointer}
.btns button.on{background:var(--fg);color:var(--bg)}
.bar{position:sticky;bottom:0;margin-top:20px;padding:10px 0;background:var(--bg)}
.bar button{min-height:44px;padding:0 16px;border-radius:8px;border:1px solid var(--fg);background:var(--fg);color:var(--bg);font:inherit;cursor:pointer}
pre{white-space:pre-wrap;background:var(--card);padding:10px;border-radius:8px;font-size:13px}
.legende{color:var(--mut);font-size:14px}
</style></head><body>
<h1>Benchmark videos IA locales</h1>
<p class="sub">%d image(s) de reference - %d video(s). 832x480, seeds fixes.</p>
<p class="legende">Notes de 0 a 3 : 0 = rate, 1 = faible, 2 = correct, 3 = tres bon. Ordre : fidelite au prompt, coherence temporelle, qualite du mouvement, absence d'artefacts.</p>
<h2>Tests de correction (vitesse normale)</h2><div class="grid">%s</div>
<h2>Image vers video (i2v) : image de reference puis video</h2><div class="grid">%s</div>
<h2>Texte vers video (t2v)</h2>
<div class="grid">%s</div>
<div class="bar"><span id="etat" class="legende">Connexion...</span></div>
<script>
var S={},DB=null,E=document.getElementById("etat");
try{S=JSON.parse(localStorage.getItem("notes")||"{}")}catch(x){}
function local(){try{localStorage.setItem("notes",JSON.stringify(S))}catch(x){}}
function paint(){document.querySelectorAll(".btns button").forEach(function(b){
var a=S[b.dataset.k]||[];b.classList.toggle("on",a[b.dataset.c]===+b.dataset.v)})}
function figInfo(k){var f=document.querySelector('figure.vid[data-key="'+k+'"]');return {model:f.dataset.model,cas:+f.dataset.case}}
function push(k){local();if(!DB){E.textContent="Notes gardees sur cet appareil seulement (base indisponible).";return}
var i=figInfo(k);
DB.doc("notes/"+k).set({model:i.model,cas:i.cas,scores:S[k],updated:new Date().toISOString()})
.then(function(){E.textContent="Note enregistree. Dites-moi 'notes faites' quand vous avez fini."},
function(){E.textContent="Echec d'enregistrement ; note gardee sur cet appareil."})}
document.addEventListener("click",function(ev){var b=ev.target.closest(".btns button");if(!b)return;
var a=S[b.dataset.k]||[null,null,null,null];a[b.dataset.c]=+b.dataset.v;S[b.dataset.k]=a;paint();push(b.dataset.k)})
paint();
(function(){var t=setTimeout(function(){E.textContent="Base indisponible : notes gardees sur cet appareil seulement."},10000);
if(!window.claude||!claude.use){return}
claude.use("db").then(function(d){clearTimeout(t);if(!d){E.textContent="Base indisponible : notes gardees sur cet appareil seulement.";return}
DB=d;E.textContent="Notes enregistrees automatiquement.";
d.collection("notes").get().then(function(snap){snap.forEach(function(doc){var v=doc.data();if(v&&v.scores){S[doc.id]=v.scores}});paint()},function(){})
},function(){})})()
</script>
</body></html>""" % (len(images), len(videos), fix_html, img_html, vid_html)


def main():
    images, videos = collect()
    (OUT / "index.html").write_text(render(images, videos), encoding="utf-8")
    files = ["index.html"] + [i["file"] for i in images] + [v["file"] for v in videos]
    print(json.dumps(files))


if __name__ == "__main__":
    main()
