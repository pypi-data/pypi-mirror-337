#!/usr/bin/env python3
# -*- coding: utf-8 -*-



from poppy.core.task import Task


__all__ = ["DescriptorReport"]


class DescriptorReport(Task):
    """
    Class for managing reports from the ROC database.
    """

    plugin_name = "roc.punk"
    name = "descriptor_report"

    # def setup_inputs(self):
    #     """
    #     Init sessions, etc.
    #     """
    #
    #     # Get the output directory
    #     self.output = self.pipeline.get("output", args=True)
    #
    #     """
    #     Init the Jinja2 environment for loading templates with inheritance.
    #     """
    #
    #     # get the environment
    #     self.environment = Environment(loader=PackageLoader("roc.punk", "templates"))
    #
    # def get_software(self):
    #     """
    #     Get the list of software in the database for the specified version of
    #     the pipeline.
    #     """
    #     # get the pipeline
    #     # pipeline = self.roc.get_pipeline()
    #
    #     # query for software
    #     query = self.session.query(Plugin)
    #     # query = query.filter_by(pipeline=pipeline)
    #     return query.all()

    def run(self):
        """
        Make a report about software and their datasets.
        """

        raise DeprecationWarning("This task is deprecated and should be used.")

        # # Get roc connector
        # if not hasattr(self, "roc"):
        #     self.roc = Connector.manager[PIPELINE_DATABASE]
        #
        # # Get the database connection if needed
        # if not hasattr(self, "session"):
        #     self.session = self.roc.session
        #
        # # Initialize inputs
        # self.setup_inputs()
        #
        # # get software inside the ROC database for the specified version of
        # # the pipeline
        # software = self.get_software()
        #
        # # create a list of datasets from the software
        # datasets = set()
        # for current_software in software:
        #     for dataset in current_software.datasets:
        #         datasets.add(dataset)
        #
        # # get the template for the report about software
        # template = self.environment.get_template("software_report.html")
        #
        # # render the template
        # html = template.render(software_list=software, dataset_list=datasets)
        #
        # # get current datetime
        # now = datetime.datetime.now()
        #
        # # the filename prefix
        # filename = osp.join(
        #     self.output,
        #     "_".join(
        #         [
        #             self.roc.get_pipeline().release.release_version,
        #             now.strftime("%Y-%m-%d-%H-%M-%S"),
        #         ]
        #     ),
        # )
        #
        # # store into a file
        # with open(".".join([filename, "html"]), "w") as f:
        #     f.write(html)
        #
        # # write the PDF
        # HTML(string=html).write_pdf(".".join([filename, "pdf"]))
