# -*- coding: utf-8 -*-
import os.path

from pynwb.spec import (
    NWBNamespaceBuilder,
    export_spec,
    NWBGroupSpec,
    NWBAttributeSpec,
    NWBLinkSpec,
)


def main():
    ns_builder = NWBNamespaceBuilder(
        name="""ndx-vame""",
        version="""0.1.0""",
        doc="""NWB extension for VAME""",
        author=[
            "Luiz Tauffer",
        ],
        contact=[
            "luiz.tauffer@catalystneuro.com",
        ],
    )
    ns_builder.include_namespace("core")

    # If your extension builds on another extension, include the namespace
    # of the other extension below
    # ns_builder.include_namespace("ndx-pose")
    ns_builder.include_type("PoseEstimation", namespace="ndx-pose")

    # Define your new data types
    # see https://pynwb.readthedocs.io/en/stable/tutorials/general/extensions.html
    # for more information
    motif_series = NWBGroupSpec(
        neurodata_type_def="MotifSeries",
        neurodata_type_inc="TimeSeries",
        doc="An extension of TimeSeries to include relevant information about the VAME motif data.",
        attributes=[
            NWBAttributeSpec(
                name="unit",
                doc="The base unit of measurement. Non-applicable for this data type.",
                dtype="text",
                required=False,
                default_value="n/a",
            ),
        ],
    )
    community_series = NWBGroupSpec(
        neurodata_type_def="CommunitySeries",
        neurodata_type_inc="TimeSeries",
        doc="An extension of TimeSeries to include relevant information about the VAME community data.",
        attributes=[
            NWBAttributeSpec(
                name="unit",
                doc="The base unit of measurement. Non-applicable for this data type.",
                dtype="text",
                required=False,
                default_value="n/a",
            ),
        ],
        links=[
            NWBLinkSpec(
                name="motif_series",
                doc="The motif series associated with this community series.",
                target_type="MotifSeries",
                quantity="?",
            ),
        ],
    )

    vame_group = NWBGroupSpec(
        neurodata_type_def="VAMEGroup",
        neurodata_type_inc="NWBDataInterface",
        doc="A group to hold VAME data.",
        attributes=[
            NWBAttributeSpec(
                name="vame_settings",
                doc="The VAME settings.",
                dtype="text",
                required=True,
            ),
        ],
        groups=[
            motif_series,
            community_series,
        ],
        links=[
            NWBLinkSpec(
                name="pose_estimation",
                doc="The pose estimation data used to generate the VAME data.",
                target_type="PoseEstimation",
                quantity="?",
            ),
        ],
    )

    # Add all of your new data types to this list
    new_data_types = [
        motif_series,
        community_series,
        vame_group,
    ]

    # export the spec to yaml files in the spec folder
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "spec"))
    export_spec(ns_builder, new_data_types, output_dir)


if __name__ == "__main__":
    # usage: python create_extension_spec.py
    main()
