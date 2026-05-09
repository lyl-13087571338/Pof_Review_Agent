import logging
import os
import sys
import time
import shutil
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

import yaml
from skills.email_download.download import download_new_pof_pdf
from skills.auto_review.review import review_pdf

CONFIG_PATH = ROOT_DIR / "config" / "config.yaml"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def load_config(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"配置文件不存在: {path}")

    with path.open("r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    if not isinstance(config, dict):
        raise ValueError("配置文件格式不正确，期望返回 YAML 映射对象")

    return config


def validate_config(config: dict) -> None:
    required = {
        "email": ["address", "password", "imap_server"],
        "paths": ["download_folder", "review_folder"],
    }
    missing = []

    for section, keys in required.items():
        if section not in config or not isinstance(config[section], dict):
            missing.append(section)
            continue
        for key in keys:
            if config[section].get(key) in (None, ""):
                missing.append(f"{section}.{key}")

    if missing:
        raise ValueError(f"配置缺失或不完整: {', '.join(missing)}")


def run_agent() -> None:
    try:
        config = load_config(CONFIG_PATH)
        validate_config(config)
    except Exception:
        logger.exception("配置加载失败")
        sys.exit(1)

    destination_folder = config.get("agent", {}).get("destination_folder", os.path.expanduser("~/Desktop"))
    download_folder = config.get("paths", {}).get("download_folder", "./downloads")
    os.makedirs(destination_folder, exist_ok=True)

    logger.info("Agent started. Running demo once...")

    # First, try to download from email
    try:
        pdf_files = download_new_pof_pdf()
    except Exception:
        logger.exception("下载 PDF 时发生错误")
        pdf_files = []

    # Also check local downloads folder
    if os.path.exists(download_folder):
        for filename in os.listdir(download_folder):
            if filename.lower().endswith(".pdf"):
                filepath = os.path.join(download_folder, filename)
                if os.path.isfile(filepath) and filepath not in pdf_files:
                    pdf_files.append(filepath)

    if not pdf_files:
        logger.info("当前没有新的 PDF 文件（这是正常的 demo 输出）")
    else:
        logger.info("Found %d PDF file(s) to process", len(pdf_files))
        for pdf_file in pdf_files:
            try:
                logger.info("Processing: %s", pdf_file)
                word_file = review_pdf(pdf_file)
                target_path = os.path.join(destination_folder, os.path.basename(word_file))
                shutil.copy(word_file, target_path)
                logger.info("审稿完成，文件已生成: %s", target_path)
            except Exception:
                logger.exception("处理文件 %s 时发生错误", pdf_file)

    logger.info("Demo 运行完成！")


if __name__ == "__main__":
    run_agent()
