import os

from ent.base_ds import BaseConfig
from ent.job import GroupByCorrelationPerStockJob, VisualiseJob
from ent.utils import generate_file_path


# TODO add multiple files processing. Output name generate.
#  OSError: Cannot save file into a non-existent directory: '/Users/evakule/PycharmProjects/logos/output'
# Add stock name to output. Add database support


def visualise():
    c = BaseConfig().builder() \
        .with_file_path('/Users/evakule/PycharmProjects/logos/source_data/AAPL_5m.csv') \
        .with_sma_window(3) \
        .with_type_vol(0.25) \
        .with_depth(20) \
        .with_coordinates_basis('close') \
        .with_stop_loss(0.5) \
        .build()

    days = [
        "2022-03-31",
        "2022-04-13",
        "2022-04-18",
        "2022-04-19",
        "2022-05-06",
        "2022-05-12",
        "2022-05-13",
        "2022-05-25",


    ]
    VisualiseJob(c, days).execute()


if __name__ == '__main__':
    # job_configs = []
    # sd_folder_path = generate_file_path('source_data')
    # files = os.listdir(sd_folder_path)
    # for f in files:
    #     file_path = os.path.join(sd_folder_path, f)
    #     c = BaseConfig().builder() \
    #         .with_file_path(file_path) \
    #         .with_sma_window(3) \
    #         .with_type_vol(0.25) \
    #         .with_depth(20) \
    #         .with_coordinates_basis('close') \
    #         .with_stop_loss(0.5) \
    #         .build()
    #     job_configs.append(c)
    #
    # for config in job_configs:
    #     GroupByCorrelationPerStockJob(config).execute()
    visualise()
