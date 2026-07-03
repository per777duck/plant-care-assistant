#!/usr/bin/env python3
"""Retry missing plant images using direct Wikimedia URLs."""

import shutil
import time
import urllib.request
from pathlib import Path

IMAGES_DIR = Path(__file__).resolve().parents[1] / "src" / "main" / "resources" / "static" / "images" / "plants"

DIRECT_URLS = {
    "dizygotheca": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8d/Schefflera_elegantissima1.jpg/600px-Schefflera_elegantissima1.jpg",
    "impatiens": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Impatiens_walleriana_001.jpg/600px-Impatiens_walleriana_001.jpg",
    "pilea": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/Pilea_peperomioides_-_Karlsruhe.jpg/600px-Pilea_peperomioides_-_Karlsruhe.jpg",
    "primula": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Primula_vulgaris_-_flower_%28aka%29.jpg/600px-Primula_vulgaris_-_flower_%28aka%29.jpg",
    "rosemary": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/db/Rosmarinus_officinalis_003.jpg/600px-Rosmarinus_officinalis_003.jpg",
    "strelitzia": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Strelitzia_reginae_-_flower_1_%28aka%29.jpg/600px-Strelitzia_reginae_-_flower_1_%28aka%29.jpg",
    "echeveria": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0f/Echeveria_elegans.jpg/600px-Echeveria_elegans.jpg",
    "hoya": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/Hoya_carnosa.jpg/600px-Hoya_carnosa.jpg",
    "cyclamen": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Cyclamen_persicum_florescence.jpg/600px-Cyclamen_persicum_florescence.jpg",
    "lemon-tree": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/Citrus_limon_fruit.jpg/600px-Citrus_limon_fruit.jpg",
    "schefflera": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Schefflera_arboricola.jpg/600px-Schefflera_arboricola.jpg",
    "asparagus-fern": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/57/Asparagus_setaceus0.jpg/600px-Asparagus_setaceus0.jpg",
    "alocasia": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Alocasia_amazonica.jpg/600px-Alocasia_amazonica.jpg",
    "basil": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/90/Basil-Basilico-Ocimum_basilicum-albahaca.jpg/600px-Basil-Basilico-Ocimum_basilicum-albahaca.jpg",
    "adiantum": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/Adiantum_raddianum_001.jpg/600px-Adiantum_raddianum_001.jpg",
    "guzmania": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/Guzmania_lingulata1.jpg/600px-Guzmania_lingulata1.jpg",
    "kalanchoe": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Kalanchoe_blossfeldiana_1.jpg/600px-Kalanchoe_blossfeldiana_1.jpg",
    "camellia": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8d/Camellia_japonica_flower_2.jpg/600px-Camellia_japonica_flower_2.jpg",
    "clivia": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Clivia_miniata1.jpg/600px-Clivia_miniata1.jpg",
    "cordyline": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/Cordyline_fruticosa_%28leaf%29.jpg/600px-Cordyline_fruticosa_%28leaf%29.jpg",
    "lavender": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/60/Single_lavendar_flower02.jpg/600px-Single_lavendar_flower02.jpg",
    "euphorbia-milii": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Euphorbia_milii_1.jpg/600px-Euphorbia_milii_1.jpg",
    "peperomia-argyreia": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0b/Peperomia_argyreia.jpg/600px-Peperomia_argyreia.jpg",
    "pteris": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Pteris_cretica_%27Albolineata%27.jpg/600px-Pteris_cretica_%27Albolineata%27.jpg",
    "setcreasea": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8d/Tradescantia_pallida.jpg/600px-Tradescantia_pallida.jpg",
    "soleirolia": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Soleirolia_soleirolii_1.jpg/600px-Soleirolia_soleirolii_1.jpg",
    "sedum": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9b/Sedum_morganianum.jpg/600px-Sedum_morganianum.jpg",
    "ficus-elastica": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0f/Ficus_elastica_1.jpg/600px-Ficus_elastica_1.jpg",
    "ficus-lyrata": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Ficus_lyrata.jpg/600px-Ficus_lyrata.jpg",
    "fuchsia": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/Fuchsia_hybrid.jpg/600px-Fuchsia_hybrid.jpg",
    "citronella": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Pelargonium_graveolens_1.jpg/600px-Pelargonium_graveolens_1.jpg",
    "schlumbergera": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Schlumbergera_truncata_1.jpg/600px-Schlumbergera_truncata_1.jpg",
    "fraxinus": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Fraxinus_excelsior_tree.jpg/600px-Fraxinus_excelsior_tree.jpg",
    "abutilon": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/Abutilon_hybridum.jpg/600px-Abutilon_hybridum.jpg",
    "achimenes": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Achimenes_longiflora.jpg/600px-Achimenes_longiflora.jpg",
}

ALL_SLUGS = [
    "monstera", "ficus", "cactus", "orchid", "aloe", "spathiphyllum", "dracaena", "palm", "ivy", "begonia",
    "sansevieria", "philodendron", "zz-plant", "laurel", "rose", "geranium", "peperomia", "calathea",
    "chlorophytum", "yucca", "anthurium", "azalea", "lucky-bamboo", "bromeliad", "vriesea", "gardenia",
    "hibiscus", "gloxinia", "dieffenbachia", "dizygotheca", "dypsis", "crassula-ovata", "impatiens",
    "caladium", "coleus", "crassula", "maranta", "myrtle", "nephrolepis", "pachira", "pelargonium", "pilea",
    "primula", "radermachera", "rhipsalis", "rosemary", "saintpaulia", "strelitzia", "stromanthe", "echeveria",
    "tradescantia", "phalaenopsis", "fatsia", "hoya", "cyclamen", "lemon-tree", "schefflera", "episcia",
    "agave", "adenium", "asparagus-fern", "aucuba", "begonia-rex", "croton", "coffee-plant", "medinilla",
    "poinsettia", "nolina", "opuntia", "polyscias", "cycas", "tillandsia", "chamaedorea", "alocasia",
    "ardisia", "basil", "begonia-elatior", "adiantum", "guzmania", "kalanchoe", "camellia", "clivia",
    "cordyline", "lavender", "euphorbia-milii", "fittonia", "pandanus", "peperomia-argyreia", "ivy-canary",
    "pteris", "setcreasea", "soleirolia", "asparagus-sprengeri", "sedum", "ficus-elastica", "ficus-lyrata",
    "fuchsia", "ceropegia", "citronella", "schlumbergera", "eustoma", "fraxinus", "abutilon", "achimenes",
]


def download(url: str, dest: Path) -> bool:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "PlantCareAssistant/1.0"})
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = resp.read()
        if len(data) < 2000:
            return False
        dest.write_bytes(data)
        return True
    except Exception as exc:
        print(f"  fail {dest.stem}: {exc}")
        return False


def main() -> None:
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    default = IMAGES_DIR / "default.jpg"
    if not default.exists():
        for slug in ALL_SLUGS:
            candidate = IMAGES_DIR / f"{slug}.jpg"
            if candidate.exists():
                shutil.copy(candidate, default)
                break

    for slug in ALL_SLUGS:
        dest = IMAGES_DIR / f"{slug}.jpg"
        if dest.exists() and dest.stat().st_size > 2000:
            continue
        url = DIRECT_URLS.get(slug)
        if url:
            print(f"Downloading {slug}...")
            if download(url, dest):
                print("  OK")
            time.sleep(1.5)
        if not dest.exists() and default.exists():
            shutil.copy(default, dest)
            print(f"Fallback default for {slug}")

    print("Total images:", len(list(IMAGES_DIR.glob("*.jpg"))))


if __name__ == "__main__":
    main()
