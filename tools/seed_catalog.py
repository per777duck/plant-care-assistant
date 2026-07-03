#!/usr/bin/env python3
"""Download plant images from Wikimedia Commons and generate SQL seed."""

import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IMAGES_DIR = ROOT / "src" / "main" / "resources" / "static" / "images" / "plants"
SQL_FILE = ROOT / "src" / "main" / "resources" / "db" / "catalog-seed.sql"
API = "https://commons.wikimedia.org/w/api.php"

EXISTING = [
    {"id": 1, "slug": "monstera", "search": "Monstera deliciosa plant"},
    {"id": 2, "slug": "ficus", "search": "Ficus benjamina"},
    {"id": 3, "slug": "cactus", "search": "Cactus houseplant"},
    {"id": 4, "slug": "orchid", "search": "Phalaenopsis orchid"},
    {"id": 5, "slug": "aloe", "search": "Aloe vera plant"},
    {"id": 6, "slug": "spathiphyllum", "search": "Spathiphyllum plant"},
    {"id": 7, "slug": "dracaena", "search": "Dracaena marginata"},
    {"id": 8, "slug": "palm", "search": "Areca palm indoor"},
    {"id": 9, "slug": "ivy", "search": "Hedera helix"},
    {"id": 10, "slug": "begonia", "search": "Begonia houseplant"},
    {"id": 11, "slug": "sansevieria", "search": "Sansevieria trifasciata"},
    {"id": 12, "slug": "philodendron", "search": "Philodendron houseplant"},
    {"id": 13, "slug": "zz-plant", "search": "Zamioculcas zamiifolia"},
    {"id": 14, "slug": "laurel", "search": "Laurus nobilis"},
    {"id": 15, "slug": "rose", "search": "Rosa chinensis flower"},
    {"id": 16, "slug": "geranium", "search": "Pelargonium flower"},
    {"id": 17, "slug": "peperomia", "search": "Peperomia plant"},
    {"id": 18, "slug": "calathea", "search": "Calathea plant"},
    {"id": 19, "slug": "chlorophytum", "search": "Chlorophytum comosum"},
    {"id": 20, "slug": "yucca", "search": "Yucca elephantipes"},
]

NEW_PLANTS = [
    ("Антуриум", "anthurium", "Anthurium andraeanum", "1 раз в неделю", "Яркий рассеянный свет", "Раз в 2 года", "Ядовит", "Любит влажность"),
    ("Азалия", "azalea", "Azalea indica", "2-3 раза в неделю", "Рассеянный свет", "Раз в год", "Слабо ядовита", "Прохладная зимовка"),
    ("Бамбук счастья", "lucky-bamboo", "Dracaena sanderiana", "1 раз в 2 недели", "Полутень", "По необходимости", "Не ядовит", "Можно в воде"),
    ("Бромелия", "bromeliad", "Bromeliaceae plant", "1 раз в неделю", "Яркий рассеянный свет", "Не пересаживают", "Не ядовита", "Полив в розетку"),
    ("Вриезия", "vriesea", "Vriesea bromeliad", "1 раз в неделю", "Рассеянный свет", "Раз в 2 года", "Не ядовита", "Влажный воздух"),
    ("Гардения", "gardenia", "Gardenia jasminoides", "2 раза в неделю", "Яркий свет без солнца", "Раз в год", "Слабо ядовита", "Кислая почва"),
    ("Гибискус", "hibiscus", "Hibiscus rosa-sinensis", "2-3 раза в неделю", "Яркий свет", "Раз в год", "Не ядовит", "Любит тепло"),
    ("Глоксиния", "gloxinia", "Sinningia speciosa", "2 раза в неделю", "Рассеянный свет", "После цветения", "Не ядовита", "Не мочить листья"),
    ("Декенбахия", "dieffenbachia", "Dieffenbachia plant", "1 раз в неделю", "Полутень", "Раз в 2 года", "Ядовита", "Очищает воздух"),
    ("Дизиготека", "dizygotheca", "Schefflera elegantissima", "1 раз в неделю", "Рассеянный свет", "Раз в 2 года", "Слабо ядовита", "Нужна влажность"),
    ("Дипсис", "dypsis", "Dypsis lutescens", "2 раза в неделю", "Яркий рассеянный свет", "Раз в 2 года", "Не ядовит", "Тропическая пальма"),
    ("Жировка", "crassula-ovata", "Crassula ovata", "1 раз в 2 недели", "Прямое солнце", "Раз в 3 года", "Не ядовита", "Денежное дерево"),
    ("Бальзамин", "impatiens", "Impatiens walleriana", "2-3 раза в неделю", "Рассеянный свет", "Раз в год", "Не ядовит", "Обильное цветение"),
    ("Каладиум", "caladium", "Caladium plant", "2 раза в неделю", "Полутень", "Весной", "Ядовит", "Декоративные листья"),
    ("Колеус", "coleus", "Coleus scutellarioides", "2 раза в неделю", "Яркий рассеянный свет", "Раз в год", "Не ядовит", "Резать для густоты"),
    ("Крассула", "crassula", "Crassula succulent", "1 раз в 2 недели", "Солнце", "Раз в 3 года", "Не ядовита", "Суккулент"),
    ("Маранта", "maranta", "Maranta leuconeura", "2 раза в неделю", "Полутень", "Раз в 2 года", "Не ядовита", "Листья двигаются"),
    ("Мирт", "myrtle", "Myrtus communis", "1 раз в неделю", "Яркий свет", "Раз в 2 года", "Не ядовит", "Ароматные листья"),
    ("Нефролепис", "nephrolepis", "Nephrolepis exaltata", "2 раза в неделю", "Полутень", "Раз в 2 года", "Не ядовит", "Папоротник"),
    ("Пахира", "pachira", "Pachira aquatica", "1 раз в неделю", "Рассеянный свет", "Раз в 2 года", "Не ядовит", "Денежное дерево"),
    ("Пеларгония", "pelargonium", "Pelargonium zonale", "1 раз в 5-7 дней", "Яркий свет", "Раз в год", "Слабо ядовита", "Ароматная"),
    ("Пилея", "pilea", "Pilea peperomioides", "1 раз в неделю", "Рассеянный свет", "Раз в год", "Не ядовита", "Дает деток"),
    ("Примула", "primula", "Primula vulgaris", "2 раза в неделю", "Яркий рассеянный свет", "После цветения", "Слабо ядовита", "Весеннее цветение"),
    ("Радермахера", "radermachera", "Radermachera sinica", "2 раза в неделю", "Рассеянный свет", "Раз в 2 года", "Не ядовит", "Детское дерево"),
    ("Рипсалис", "rhipsalis", "Rhipsalis cactus", "1 раз в неделю", "Полутень", "Раз в 2 года", "Не ядовит", "Лесной кактус"),
    ("Розмарин", "rosemary", "Rosmarinus officinalis", "1 раз в неделю", "Прямое солнце", "Раз в 2 года", "Не ядовит", "Пряная трава"),
    ("Сенполия", "saintpaulia", "Saintpaulia ionantha", "1 раз в неделю", "Рассеянный свет", "Раз в год", "Не ядовита", "Узамбарская фиалка"),
    ("Стрелиция", "strelitzia", "Strelitzia reginae", "1 раз в неделю", "Яркий свет", "Раз в 2 года", "Слабо ядовита", "Птичка"),
    ("Строманта", "stromanthe", "Stromanthe sanguinea", "2 раза в неделю", "Полутень", "Раз в 2 года", "Не ядовита", "Влажный воздух"),
    ("Эхеверия", "echeveria", "Echeveria succulent", "1 раз в 2 недели", "Солнце", "Раз в 3 года", "Не ядовита", "Розетка"),
    ("Традесканция", "tradescantia", "Tradescantia zebrina", "2 раза в неделю", "Яркий рассеянный свет", "По необходимости", "Слабо ядовита", "Быстро растет"),
    ("Фаленопсис", "phalaenopsis", "Phalaenopsis orchid", "1 раз в 7-10 дней", "Рассеянный свет", "Раз в 2 года", "Не ядовит", "Орхидея-бабочка"),
    ("Фатсия", "fatsia", "Fatsia japonica", "1 раз в неделю", "Полутень", "Раз в 2 года", "Слабо ядовита", "Крупные листья"),
    ("Хойя", "hoya", "Hoya carnosa", "1 раз в 10 дней", "Яркий рассеянный свет", "Редко", "Молоко ядовито", "Восковой плющ"),
    ("Цикламен", "cyclamen", "Cyclamen persicum", "2 раза в неделю", "Рассеянный свет", "После цветения", "Ядовит", "Прохладная зимовка"),
    ("Лимон домашний", "lemon-tree", "Citrus limon indoor", "2 раза в неделю", "Прямое солнце", "Раз в 2 года", "Не ядовит", "Цитрус"),
    ("Шефлера", "schefflera", "Schefflera arboricola", "1 раз в неделю", "Рассеянный свет", "Раз в 2 года", "Слабо ядовита", "Декоративный куст"),
    ("Эписция", "episcia", "Episcia cupreata", "2 раза в неделю", "Полутень", "Раз в год", "Не ядовита", "Покрывное растение"),
    ("Агава", "agave", "Agave americana pot", "1 раз в 2-3 недели", "Прямое солнце", "Редко", "Слабо ядовита", "Суккулент"),
    ("Адениум", "adenium", "Adenium obesum", "1 раз в 10 дней", "Солнце", "Раз в 2 года", "Ядовит", "Пустынная роза"),
    ("Аспарагус", "asparagus-fern", "Asparagus setaceus", "2 раза в неделю", "Рассеянный свет", "Раз в 2 года", "Ягоды ядовиты", "Воздушный папоротник"),
    ("Аукуба", "aucuba", "Aucuba japonica", "1 раз в неделю", "Полутень", "Раз в 2 года", "Не ядовита", "Золотистые пятна"),
    ("Бегония королевская", "begonia-rex", "Begonia rex", "1 раз в неделю", "Рассеянный свет", "Раз в год", "Не ядовита", "Пестрые листья"),
    ("Кодиэум", "croton", "Codiaeum variegatum", "2 раза в неделю", "Яркий свет", "Раз в 2 года", "Ядовит", "Яркая окраска"),
    ("Кофейное дерево", "coffee-plant", "Coffea arabica houseplant", "2 раза в неделю", "Рассеянный свет", "Раз в 2 года", "Не ядовит", "Ароматное"),
    ("Мединилла", "medinilla", "Medinilla magnifica", "2 раза в неделю", "Рассеянный свет", "Раз в 2 года", "Не ядовита", "Экзотические цветы"),
    ("Пуансеттия", "poinsettia", "Euphorbia pulcherrima", "1 раз в неделю", "Яркий свет", "После цветения", "Молоко ядовито", "Рождественская звезда"),
    ("Нолина", "nolina", "Beaucarnea recurvata", "1 раз в 2 недели", "Солнце", "Редко", "Не ядовит", "Бутылочное дерево"),
    ("Опунция", "opuntia", "Opuntia cactus", "1 раз в 3 недели", "Солнце", "Раз в 3 года", "Не ядовит", "Кактус-опунция"),
    ("Полисиас", "polyscias", "Polyscias fruticosa", "1 раз в неделю", "Рассеянный свет", "Раз в 2 года", "Не ядовит", "Аралиевый куст"),
    ("Саговник", "cycas", "Cycas revoluta", "1 раз в 2 недели", "Яркий свет", "Редко", "Ядовит", "Пальмовидный"),
    ("Тиландсия", "tillandsia", "Tillandsia air plant", "Опрыскивание 2 раза в неделю", "Яркий рассеянный свет", "Не пересаживают", "Не ядовита", "Воздушная"),
    ("Хамедорея", "chamaedorea", "Chamaedorea elegans", "1 раз в неделю", "Полутень", "Раз в 2 года", "Не ядовит", "Нефтолюбивая пальма"),
    ("Алоказия", "alocasia", "Alocasia amazonica", "2 раза в неделю", "Рассеянный свет", "Раз в 2 года", "Ядовита", "Слоновое ухо"),
    ("Ардизия", "ardisia", "Ardisia crenata", "1 раз в неделю", "Полутень", "Раз в 2 года", "Ягоды ядовиты", "Коралловые ягоды"),
    ("Базилик", "basil", "Ocimum basilicum pot", "2-3 раза в неделю", "Солнце", "По необходимости", "Не ядовит", "Пряность"),
    ("Бегония элатиор", "begonia-elatior", "Begonia elatior", "2 раза в неделю", "Рассеянный свет", "Раз в год", "Не ядовита", "Зимнее цветение"),
    ("Венерин волос", "adiantum", "Adiantum raddianum", "2 раза в неделю", "Полутень", "Раз в год", "Не ядовит", "Нежный папоротник"),
    ("Гузмания", "guzmania", "Guzmania bromeliad", "1 раз в неделю", "Рассеянный свет", "Не пересаживают", "Не ядовита", "Яркое соцветие"),
    ("Каланхоэ", "kalanchoe", "Kalanchoe blossfeldiana", "1 раз в 10 дней", "Солнце", "Раз в 2 года", "Слабо ядовит", "Долго цветет"),
    ("Камелия", "camellia", "Camellia japonica pot", "2 раза в неделю", "Рассеянный свет", "Раз в 2 года", "Не ядовит", "Зимнее цветение"),
    ("Кливия", "clivia", "Clivia miniata", "1 раз в неделю", "Полутень", "Раз в 3 года", "Слабо ядовита", "Оранжевые цветы"),
    ("Кордилина", "cordyline", "Cordyline fruticosa", "1 раз в неделю", "Яркий рассеянный свет", "Раз в 2 года", "Слабо ядовита", "Красные листья"),
    ("Лаванда", "lavender", "Lavandula angustifolia pot", "1 раз в 10 дней", "Солнце", "Раз в год", "Не ядовит", "Аромат"),
    ("Молочай миля", "euphorbia-milii", "Euphorbia milii", "1 раз в 10 дней", "Солнце", "Раз в 2 года", "Молоко ядовито", "Терновый куст"),
    ("Орехокол", "fittonia", "Fittonia albivenis", "2 раза в неделю", "Полутень", "Раз в год", "Не ядовита", "Мозаичный лист"),
    ("Панданус", "pandanus", "Pandanus veitchii", "1 раз в неделю", "Яркий рассеянный свет", "Раз в 2 года", "Не ядовит", "Винтовая пальма"),
    ("Пеперомия арбузная", "peperomia-argyreia", "Peperomia argyreia", "1 раз в неделю", "Рассеянный свет", "Раз в 2 года", "Не ядовита", "Арбузные листья"),
    ("Плющ канарский", "ivy-canary", "Hedera canariensis", "1 раз в неделю", "Полутень", "Раз в год", "Ядовит", "Ампельный"),
    ("Птерис", "pteris", "Pteris cretica", "2 раза в неделю", "Полутень", "Раз в год", "Не ядовит", "Папоротник крената"),
    ("Сеткреазия", "setcreasea", "Tradescantia pallida", "2 раза в неделю", "Яркий свет", "По необходимости", "Слабо ядовита", "Фиолетовые листья"),
    ("Солейролия", "soleirolia", "Soleirolia soleirolii", "2-3 раза в неделю", "Полутень", "Раз в год", "Не ядовит", "Мох"),
    ("Спаржа декоративная", "asparagus-sprengeri", "Asparagus densiflorus", "1 раз в неделю", "Рассеянный свет", "Раз в 2 года", "Ягоды ядовиты", "Пушистая"),
    ("Толстянка", "sedum", "Sedum morganianum", "1 раз в 2 недели", "Солнце", "Редко", "Не ядовита", "Ослиный хвост"),
    ("Фикус каучуконосный", "ficus-elastica", "Ficus elastica", "1 раз в неделю", "Рассеянный свет", "Раз в 2 года", "Молоко ядовито", "Резиновое дерево"),
    ("Фикус лиреобразный", "ficus-lyrata", "Ficus lyrata", "1 раз в неделю", "Яркий рассеянный свет", "Раз в 2 года", "Молоко ядовито", "Скрипичный лист"),
    ("Фуксия", "fuchsia", "Fuchsia hybrid", "2 раза в неделю", "Рассеянный свет", "Раз в год", "Ягоды съедобны", "Ампельная"),
    ("Церопегия", "ceropegia", "Ceropegia woodii", "1 раз в 10 дней", "Рассеянный свет", "Редко", "Не ядовита", "Сердце виноград"),
    ("Цитронелла", "citronella", "Pelargonium citrosum", "1 раз в неделю", "Солнце", "Раз в год", "Не ядовит", "Лимонный запах"),
    ("Шлюмбергера", "schlumbergera", "Schlumbergera truncata", "1 раз в неделю", "Рассеянный свет", "Раз в 3 года", "Не ядовит", "Декабрист"),
    ("Эустома", "eustoma", "Eustoma grandiflorum", "2 раза в неделю", "Яркий рассеянный свет", "Раз в год", "Слабо ядовита", "Лизиантус"),
    ("Ясень комнатный", "fraxinus", "Fraxinus ornus bonsai", "2 раза в неделю", "Солнце", "Раз в 2 года", "Не ядовит", "Бонсай"),
    ("Абутилон", "abutilon", "Abutilon hybridum", "2 раза в неделю", "Яркий свет", "Раз в год", "Не ядовит", "Кленовый куст"),
    ("Ахименес", "achimenes", "Achimenes longiflora", "2 раза в неделю", "Полутень", "После цветения", "Не ядовита", "Теневыноосимый"),
]


def sql_escape(value: str) -> str:
    return value.replace("'", "''")


def fetch_image_url(search: str) -> str | None:
    params = {
        "action": "query",
        "format": "json",
        "generator": "search",
        "gsrsearch": f"filetype:bitmap {search}",
        "gsrnamespace": "6",
        "gsrlimit": "5",
        "prop": "imageinfo",
        "iiprop": "url",
        "iiurlwidth": "600",
    }
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "PlantCareAssistant/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))

    pages = data.get("query", {}).get("pages", {})
    for page in pages.values():
        infos = page.get("imageinfo") or []
        if not infos:
            continue
        thumb = infos[0].get("thumburl") or infos[0].get("url")
        if thumb:
            return thumb
    return None


def download_image(url: str, dest: Path) -> bool:
    req = urllib.request.Request(url, headers={"User-Agent": "PlantCareAssistant/1.0"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        content = resp.read()
    if len(content) < 3000:
        return False
    dest.write_bytes(content)
    return True


def ensure_default_image(targets: list[Path]) -> None:
    for path in targets:
        if path.exists() and path.stat().st_size > 3000:
            default = IMAGES_DIR / "default.jpg"
            if not default.exists():
                default.write_bytes(path.read_bytes())
            return


def main() -> None:
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    SQL_FILE.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "-- PlantCare catalog seed: 80 new plants + image paths for 100 plants",
        "-- Run once: psql -h localhost -p 5433 -U postgres -d plantcare -f catalog-seed.sql",
        "",
    ]

    all_slugs = []

    for item in EXISTING:
        slug = item["slug"]
        all_slugs.append(slug)
        dest = IMAGES_DIR / f"{slug}.jpg"
        image_path = f"/images/plants/{slug}.jpg"

        if not dest.exists():
            print(f"Downloading [{item['id']}] {slug}...")
            try:
                url = fetch_image_url(item["search"])
                if url and download_image(url, dest):
                    print(f"  OK: {dest.name}")
                else:
                    print(f"  FAIL: {slug}")
                    image_path = "/images/plants/default.jpg"
            except Exception as exc:
                print(f"  ERROR {slug}: {exc}")
                image_path = "/images/plants/default.jpg"
            time.sleep(0.4)
        else:
            print(f"Skip existing {slug}")

        lines.append(
            f"UPDATE plants SET image_path = '{image_path}' WHERE id = {item['id']};"
        )

    for name, slug, search, water, light, transfer, poison, optional in NEW_PLANTS:
        all_slugs.append(slug)
        dest = IMAGES_DIR / f"{slug}.jpg"
        image_path = f"/images/plants/{slug}.jpg"

        if not dest.exists():
            print(f"Downloading [new] {slug} ({name})...")
            try:
                url = fetch_image_url(search)
                if url and download_image(url, dest):
                    print(f"  OK: {dest.name}")
                else:
                    print(f"  FAIL: {slug}")
                    image_path = "/images/plants/default.jpg"
            except Exception as exc:
                print(f"  ERROR {slug}: {exc}")
                image_path = "/images/plants/default.jpg"
            time.sleep(0.4)
        else:
            print(f"Skip existing {slug}")

        lines.append(
            "INSERT INTO plants (name, watering_recomendation, lightning_recomendation, "
            "transfer_information, poison_information, optional_info_care, image_path) "
            f"SELECT '{sql_escape(name)}', '{sql_escape(water)}', '{sql_escape(light)}', "
            f"'{sql_escape(transfer)}', '{sql_escape(poison)}', '{sql_escape(optional)}', "
            f"'{image_path}' "
            f"WHERE NOT EXISTS (SELECT 1 FROM plants WHERE name = '{sql_escape(name)}');"
        )

    # default image from first successful download
    for slug in all_slugs:
        candidate = IMAGES_DIR / f"{slug}.jpg"
        if candidate.exists() and candidate.stat().st_size > 3000:
            default = IMAGES_DIR / "default.jpg"
            if not default.exists():
                default.write_bytes(candidate.read_bytes())
            break

    SQL_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"\nSQL written to {SQL_FILE}")
    print(f"Images in {IMAGES_DIR}")


if __name__ == "__main__":
    main()
