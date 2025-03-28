import os
import shutil
from .config import template_path, gitpaths
from .utils import create_names, replace_names, read_file_content, write_file_content
from ._git import _init_git
from ._react import _init_react


def create_new_project(name, path, with_react=False, nogit=False):
    basepath = os.path.join(path, name)
    module_name = name.replace(" ", "_").replace("-", "_").lower()
    package_name = module_name.replace("_", "-")

    project_name, module_name, package_name = create_names(name)

    print(f"Creating project {name} at {basepath}")
    os.system("python -m pip install uv --upgrade")

    if os.path.exists(basepath) and os.path.isdir(basepath):
        # check if empty
        if os.listdir(basepath):
            print(f"Project {name} already exists")
            return
        else:
            print(f"Project {name} already exists but is empty")
            os.rmdir(basepath)

    shutil.copytree(template_path, basepath)

    # get current git user

    git_user = os.popen("git config user.name").read().strip() or "Your Name"
    git_email = (
        os.popen("git config user.email").read().strip() or "your.email@send.com"
    )

    # in each file replace "{{ project_name }}" with name
    # and "{{ git_user }}" with git_user
    # and "{{ git_email }}" with git_email
    for root, _, files in os.walk(basepath):
        for file in files:
            filepath = os.path.join(root, file)
            try:
                content, enc = read_file_content(filepath)
            except UnicodeDecodeError:
                print(f"Error reading file {filepath}")
                continue
            content = replace_names(
                content,
                project_name=project_name,
                module_name=module_name,
                package_name=package_name,
                git_user=git_user,
                git_email=git_email,
            )
            write_file_content(filepath, content, enc)

    # rename the new_package folder to the project name
    os.rename(
        os.path.join(basepath, "src", "new_package"),
        os.path.join(basepath, "src", module_name),
    )

    # rename all files starting with "template__" by removing the "template__" prefix
    for root, _, files in os.walk(basepath):
        for file in files:
            if file.startswith("template__"):
                new_file = file.replace("template__", "")
                os.rename(os.path.join(root, file), os.path.join(root, new_file))

    if not nogit:
        _init_git(basepath)
    else:
        for gitpath in gitpaths:
            gitpath = os.path.join(basepath, gitpath)
            if os.path.exists(gitpath):
                shutil.rmtree(gitpath)

    reactfolder = os.path.join(basepath, "react_plugin")
    if not with_react:
        shutil.rmtree(reactfolder)
    else:
        _init_react(reactfolder)
        # remove the .git and .gitignore
