import os
BASEDIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

VECTOR_DB_PATH = os.path.join(BASEDIR, "db","chroma_local")
CURRENT_SPL_FOLDER = "dm_spl_monthly_update_aug2023"