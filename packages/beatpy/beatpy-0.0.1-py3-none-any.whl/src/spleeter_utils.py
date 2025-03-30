"""
- Vocals (singing voice) / accompaniment separation (2 stems)
- Vocals / drums / bass / other separation (4 stems)
- Vocals / drums / bass / piano / other separation (5 stems)
"""
from typing import Literal
import subprocess
from pathlib import Path
import logging
import os

logger = logging.getLogger(__name__)
PATH_ENV = Path.cwd() / os.getenv("ENV_SPLEETER", "_env_spleeter")
if not PATH_ENV.exists():
    raise Exception(f"Necesitas crear el entorno de spleeter `./1_spleeter_create_env.sh`")

T_Stems = Literal[2, 4, 5]
ALLOWED_STEMS = (2, 4, 5)

def run_in_python_env(*, cmd: str, path_env: Path = PATH_ENV) -> None:
    activate_script = path_env / "bin" / "activate"
    full_command = f"source {activate_script} && {cmd}"
    subprocess.run(["bash", "-c", full_command], check=True)

def get_cmd_run_spleeter(*, youtube_id: str, stems: T_Stems) -> None:
    """
    - TODO: https://github.com/deezer/spleeter/wiki/2.-Getting-started#using-models-up-to-16khz
    """
    logger.info(f"- Run spleeter - youtube_id={youtube_id}")
    if stems not in ALLOWED_STEMS:
        raise ValueError(f"Invalid stem {stems}.")
    CMD_RUN_SPLEETER = (
        f"spleeter separate -p spleeter:{stems}stems "
        # Este crea la carpeta con el nombre del archivo de mp3.
        # Como ya existe por mi estructura de proyecto, entonces no hace nada.
        "-o data/extracted "
        f"data/extracted/{youtube_id}/{youtube_id}.mp3"
    )
    run_in_python_env(cmd=CMD_RUN_SPLEETER, path_env=PATH_ENV)
