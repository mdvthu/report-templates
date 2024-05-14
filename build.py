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

config_file = "config.yaml"
config_file_template = "config.yaml.default"
input_data_dir = "yaml"
output_data_dir = "output/"

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

all_templates = {}

# load the YAML templates into memory
for fn in os.listdir(input_data_dir):
    logging.debug("Processing %s", fn)
    with open(os.path.join(input_data_dir, fn), "tr") as f:
        yaml_content = yaml.safe_load(f)
    logging.debug(yaml_content)
    all_templates[fn] = yaml_content

# set up text templating
env = jinja2.Environment(loader=jinja2.FileSystemLoader("templates"))
# plain text report
text_template = env.get_template("report.txt")

# create all the text templates
for k in all_templates:
    rendered_template = text_template.render(
        config=config,
        template_data=all_templates[k],
    )
    output_fn = "{}_{}.txt".format(
        config["vr_shortcut_prefix"], all_templates[k]["vr_shortcut_suffix"]
    ).replace(" ", "_")
    # verbose output including the filename and rendered template
    logging.info("output/text/%s:", output_fn)
    logging.info("---")
    logging.info(rendered_template)
    logging.info("...")
    # ensure the output directory exists
    text_template_output_dir = os.path.join(output_data_dir, "text/")
    os.makedirs(text_template_output_dir, exist_ok=True)
    with open(os.path.join(text_template_output_dir, output_fn), "wt") as fout:
        fout.write(rendered_template)

# create a single XML file with all templates, for Dragon 12 import
dragon_v12_template = env.get_template("dragon_mycmds.xml")
rendered_dragon_template = dragon_v12_template.render(
    config=config, template_data=all_templates
)
dragon_template_dir = os.path.join(output_data_dir, "dragon/")
os.makedirs(dragon_template_dir, exist_ok=True)
# Dragon VR templates XML
with open(os.path.join(dragon_template_dir, "dragon_v12.xml"), "wt") as fout:
    fout.write(rendered_dragon_template)
