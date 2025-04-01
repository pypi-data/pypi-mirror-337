from bluer_ai.help.generic import help_functions as generic_help_functions
from bluer_ai.help.actions import help_perform_action
from bluer_ai.help.assets import help_functions as help_assets
from bluer_ai.help.blueness import help_blueness
from bluer_ai.help.browse import help_browse
from bluer_ai.help.conda import help_functions as help_conda
from bluer_ai.help.clone import help_clone
from bluer_ai.help.docker import help_functions as help_docker
from bluer_ai.help.env import help_functions as help_env
from bluer_ai.help.eval import help_eval
from bluer_ai.help.gif import help_gif
from bluer_ai.help.git import help_functions as help_git
from bluer_ai.help.gpu import help_functions as help_gpu
from bluer_ai.help.host import help_functions as help_host
from bluer_ai.help.init import help_init
from bluer_ai.help.instance import help_functions as help_instance
from bluer_ai.help.latex import help_functions as help_latex
from bluer_ai.help.logging import help_cat
from bluer_ai.help.logging import help_functions as help_log
from bluer_ai.help.list import help_functions as help_list
from bluer_ai.help.ls import help_ls
from bluer_ai.help.metadata import help_functions as help_metadata
from bluer_ai.help.mlflow import help_functions as help_mlflow
from bluer_ai.help.notebooks import help_functions as help_notebooks
from bluer_ai.help.object import help_functions as help_object
from bluer_ai.help.open import help_open
from bluer_ai.help.pause import help_pause
from bluer_ai.help.plugins import help_functions as help_plugins
from bluer_ai.help.publish import help_functions as help_publish
from bluer_ai.help.repeat import help_repeat
from bluer_ai.help.sagemaker import help_functions as help_sagemaker
from bluer_ai.help.seed import help_functions as help_seed
from bluer_ai.help.select import help_select
from bluer_ai.help.session import help_functions as help_session
from bluer_ai.help.storage import help_functions as help_storage
from bluer_ai.help.sleep import help_sleep
from bluer_ai.help.source import (
    help_source_caller_suffix_path,
    help_source_path,
)
from bluer_ai.help.terminal import help_badge
from bluer_ai.help.terraform import help_functions as help_terraform
from bluer_ai.help.watch import help_watch

help_functions = generic_help_functions(plugin_name="bluer_ai")


help_functions.update(
    {
        "assets": help_assets,
        "badge": help_badge,
        "blueness": help_blueness,
        "browse": help_browse,
        "cat": help_cat,
        "clone": help_clone,
        "conda": help_conda,
        "docker": help_docker,
        "env": help_env,
        "eval": help_eval,
        "gif": help_gif,
        "git": help_git,
        "gpu": help_gpu,
        "host": help_host,
        "init": help_init,
        "instance": help_instance,
        "latex": help_latex,
        "log": help_log,
        "list": help_list,
        "ls": help_ls,
        "metadata": help_metadata,
        "mlflow": help_mlflow,
        "notebooks": help_notebooks,
        "object": help_object,
        "open": help_open,
        "pause": help_pause,
        "perform_action": help_perform_action,
        "plugins": help_plugins,
        "publish": help_publish,
        "repeat": help_repeat,
        "sagemaker": help_sagemaker,
        "seed": help_seed,
        "select": help_select,
        "sleep": help_sleep,
        "session": help_session,
        "storage": help_storage,
        "source_caller_suffix_path": help_source_caller_suffix_path,
        "source_path": help_source_path,
        "terraform": help_terraform,
        "watch": help_watch,
    }
)
