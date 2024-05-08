#!/usr/bin/env python3
"""(re-)builds standardised reports from YAML content files
"""

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
output_data_dir = "output/text/"

try:
    # load user configuration
    with open(config_file, "tr") as f:
        config = yaml.safe_load(f)
except FileNotFoundError:
    # user config doesn't exist, create from default
    print(f"{config_file} not found. Copying {config_file_template}", file=sys.stderr)
    shutil.copyfile(config_file_template, config_file)
    sys.exit(1)

if filecmp.cmp(config_file, config_file_template):
    # config file not customised
    print(f"{config_file} not customised. Please edit and rerun.", file=sys.stderr)
    sys.exit(1)

# set up templating
env = jinja2.Environment(loader=jinja2.FileSystemLoader("templates"))
# plain text report
template = env.get_template("report.txt")

for fn in os.listdir(input_data_dir):
    logging.debug("Processing %s", fn)
    with open(os.path.join(input_data_dir, fn), "tr") as f:
        yaml_content = yaml.safe_load(f)
    logging.debug(yaml_content)
    rendered_template = template.render(
        config=config,
        template_data=yaml_content,
    )
    output_fn = "{}_{}.txt".format(
        config["vr_shortcut_prefix"], yaml_content["vr_shortcut_suffix"]
    ).replace(" ", "_")
    # verbose output including the filename and rendered template
    logging.info("output/text/%s:", output_fn)
    logging.info("---")
    logging.info(rendered_template)
    logging.info("...")
    with open(os.path.join(output_data_dir, output_fn), "wt") as fout:
        fout.write(rendered_template)
