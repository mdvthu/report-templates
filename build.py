#!/usr/bin/env python3
"""(re-)builds standardised reports from YAML content files"""

# SPDX-FileCopyrightText: 2024 Mark Thurston
#
# SPDX-License-Identifier: Apache-2.0

import filecmp
import logging
import os
import shutil
import sys

import jinja2

import yaml

# locations of user configuration files
config_file = "config.yaml"
config_file_template = "config.yaml.default"

# absolute directory paths
cwd = os.path.abspath(os.path.dirname(__file__))
INPUT_DATA_DIR = os.path.join(cwd, "yaml")
OUTPUT_DATA_DIR = os.path.join(cwd, "output")

try:
    # load user configuration
    with open(config_file, "tr") as f:
        config = yaml.safe_load(f)
except FileNotFoundError:
    # user config doesn't exist, create from default
    print(
        f"{config_file} not found. Copying {config_file_template}",
        file=sys.stderr,
    )
    shutil.copyfile(config_file_template, config_file)
    sys.exit(1)

if filecmp.cmp(config_file, config_file_template):
    # config file not customised
    print(
        f"{config_file} not customised. Please edit and rerun.",
        file=sys.stderr,
    )
    sys.exit(1)


class YAMLTemplate:
    def __init__(self, filename: str):
        """
        Load data and populate into a template

        filename:
            YAML file present within the template directory
            (filename only, not full path)
        """
        self._yaml_path = os.path.join(INPUT_DATA_DIR, filename)
        logging.debug("Loading template %s", filename)
        with open(self._yaml_path, "tr") as f:
            self.yaml_content = yaml.safe_load(f)
        self.vr_shortcut_suffix = self.yaml_content["vr_shortcut_suffix"]
        self.vr_shortcut_name = (
            config["vr_shortcut_prefix"] + " " + self.vr_shortcut_suffix
        )
        self.render_text()

    def __repr__(self):
        return self.text_template

    def render_text(self):
        """Render plain text Jinja template"""
        # set up text templating
        env = jinja2.Environment(loader=jinja2.FileSystemLoader("templates"))
        # plain text report
        text_template = env.get_template("report.txt")
        self.text_template = text_template.render(
            config=config, template_data=self.yaml_content
        )
        # verbose output including the filename and rendered template
        logging.info("---")
        logging.info(self.text_template)
        logging.info("...")

    def save(self):
        """Save the text template to disk"""
        # ensure the output directory exists
        text_template_loc = os.path.join(OUTPUT_DATA_DIR, "text/")
        os.makedirs(text_template_loc, exist_ok=True)
        output_fn = "{}.txt".format(
            self.vr_shortcut_name.replace(" ", "_"),
        )
        with open(os.path.join(text_template_loc, output_fn), "wt") as fout:
            fout.write(self.text_template)


all_templates = {YAMLTemplate(fn) for fn in os.listdir(INPUT_DATA_DIR)}

for template in all_templates:
    template.save()

# create a single XML file with all templates, for Dragon 12 import
env = jinja2.Environment(loader=jinja2.FileSystemLoader("templates"))
dragon_v12_template = env.get_template("dragon_mycmds.xml")
rendered_dragon_template = dragon_v12_template.render(
    config=config, template_data=all_templates
)
dragon_template_dir = os.path.join(OUTPUT_DATA_DIR, "dragon/")
os.makedirs(dragon_template_dir, exist_ok=True)
# Dragon VR templates XML
with open(os.path.join(dragon_template_dir, "dragon_v12.xml"), "wt") as fout:
    fout.write(rendered_dragon_template)
