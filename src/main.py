import argparse
import json
import os
import sys

import supervisely as sly
from dotenv import load_dotenv

import src.options as o
import src.settings as s
from dataset_tools import ProjectRepo
from src.convert import convert_and_upload_supervisely_project

PARENT_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
LOCAL_ENV = os.path.join(PARENT_PATH, "local.env")
load_dotenv(os.path.expanduser("~/ninja.env"))
load_dotenv(LOCAL_ENV)
SERVER_ADDRESS = os.getenv("SERVER_ADDRESS")
TEAM_ID = sly.env.team_id()
WORKSPACE_ID = sly.env.workspace_id()


def get_project_info(api: sly.Api):
    s.check_names()

    project_info = api.project.get_info_by_name(WORKSPACE_ID, s.PROJECT_NAME)
    if not project_info:
        # If project doesn't found on instance, create it and use new project info.
        sly.logger.info(f"Project {s.PROJECT_NAME} not found on instance. Creating a new one...")
        project_info = convert_and_upload_supervisely_project(api, WORKSPACE_ID, s.PROJECT_NAME)
        sly.logger.info("Now you can explore created project and choose 'preview_image_id'.")
        sys.exit(0)
    else:
        sly.logger.info(f"Found project {s.PROJECT_NAME} on instance, will use it.")

    return project_info


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload dataset to instance.")
    parser.add_argument(
        "--forces", type=json.loads, default="{}", help="Which parameters to force."
    )

    args = parser.parse_args()
    forces = args.forces

    sly.logger.info(f"Script is starting with forces: {forces}")

    sly.fs.mkdir("./stats")
    sly.fs.mkdir("./visualizations")

    api = sly.Api.from_env()
    sly.logger.info(
        f"Connected to Supervisely. Server address: {SERVER_ADDRESS}, team_id: {TEAM_ID}, workspace_id: {WORKSPACE_ID}."
    )
    project_id = get_project_info(api).id
    settings = s.get_settings()

    stat_options = o.get_stats_options()
    vis_options = o.get_visualization_options()

    sly.logger.info(f"Starting to work with project id: {project_id}.")

    force_stats = forces.get("force_stats")
    force_visuals = forces.get("force_visuals")
    force_demo = forces.get("force_demo")
    force_download_sly_url = forces.get("force_download_sly_url")
    force_texts = forces.get("force_texts")

    settings["force_texts"] = force_texts
    settings["force_download_sly_url"] = force_download_sly_url
    project_repo = ProjectRepo(api, project_id, settings)
    project_repo.build_stats(force=force_stats, settings=stat_options)
    project_repo.build_visualizations(force=force_visuals, settings=vis_options)
    project_repo.build_demo(force=force_demo)
    project_repo.build_texts(force=force_texts, preview_class=o.PREVIEW_CLASS)

    sly.logger.info("Script finished.")
