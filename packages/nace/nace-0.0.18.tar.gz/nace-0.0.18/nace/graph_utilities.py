import json

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def _create_plot_collection(to_graph, save_as=None, x_label="", y_label=""):
    df = pd.DataFrame.from_dict(to_graph)
    plt.clf()
    # svm = sns.regplot(data=df, y='Frequency perturbation %', x="Number of properties") #, hue="ok")
    # plt.savefig(fn+'.2.png')
    # create the plot
    fig, ax = plt.subplots()
    fig.set_size_inches(18.5, 10.5)
    handle = sns.lineplot(data=df, ax=ax)

    handle.set(xlabel=x_label, ylabel=y_label)

    fig.show()
    if save_as is not None:
        plt.savefig(save_as, dpi=200)


def _produce_behaviour_chart(statistic_series, save_as):
    sub_sampled = []
    bucket_size = 100
    for i in range(len(statistic_series)):
        if i > bucket_size:
            n = float(bucket_size)
            window_data = statistic_series[i - bucket_size:i]
        else:
            n = float(i + 1)
            window_data = statistic_series[:i]

        sum_curious = sum(r['plan.behavior.curious'] for r in window_data)
        sum_explore = sum(r['plan.behavior.explore'] for r in window_data)
        sum_babble = sum(r['plan.behavior.babble'] for r in window_data)
        sum_achieve = sum(r['plan.behavior.achieve'] for r in window_data)

        sub_sampled.append(
            {
                "curious": sum_curious / n,
                "explore": sum_explore / n,
                "babble": sum_babble / n,
                "achieve": sum_achieve / n
            }
        )
    y_label = "Proportion"
    x_label = "Step"
    _create_plot_collection(sub_sampled, save_as, x_label, y_label)


def _produce_confidence_chart(statistic_series, save_as):
    sub_sampled = []
    for i in range(len(statistic_series)):
        sub_sampled.append(
            {
                "AIRIS_confidence": statistic_series[i]['plan.lowest_AIRIS_confidence'] * 100.0,
            }
        )
    y_label = "AIRIS Confidence"
    x_label = "Step"
    _create_plot_collection(sub_sampled, save_as, x_label, y_label)


def _produce_average_return_chart(statistic_series, save_as):
    sub_sampled = []
    for i in range(len(statistic_series)):
        produce_data_for_index = -1
        if (i == len(statistic_series) - 1):
            produce_data_for_index = i
        if i > 0 and 'episode_count' in statistic_series[i] and statistic_series[i - 1]['episode_count'] != \
                statistic_series[i]['episode_count']:
            produce_data_for_index = i - 1

        if produce_data_for_index > -1:
            reward = statistic_series[produce_data_for_index]['cumulative_gym_reward'] if 'cumulative_gym_reward' in \
                                                                                          statistic_series[
                                                                                              produce_data_for_index] else 0.0
            episode_count = statistic_series[produce_data_for_index]['episode_count'] + 1 if 'episode_count' in \
                                                                                             statistic_series[
                                                                                                 produce_data_for_index] else 1  # zero based
            aer = reward / episode_count
            sub_sampled.append(
                {
                    "average_episode_return": aer
                }
            )
    y_label = "Average return per episode"
    x_label = "Episode"
    _create_plot_collection(sub_sampled, save_as, x_label, y_label)


def produce_charts(statistic_series, prefix):
    _produce_confidence_chart(statistic_series, save_as="./data/" + prefix + "_confidence.png")
    _produce_behaviour_chart(statistic_series, save_as="./data/" + prefix + "_behaviour.png")
    _produce_average_return_chart(statistic_series, save_as="./data/" + prefix + "_average_return.png")


if __name__ == "__main__":
    fn = "../data/" + "series_statistics.json"
    with open(fn, "r") as f:
        statistic_series = json.load(f)
    prefix = ""
    # note the different assumed working directory
    _produce_confidence_chart(statistic_series, save_as="../data/" + prefix + "_confidence.png")
    _produce_behaviour_chart(statistic_series, save_as="../data/" + prefix + "_behaviour.png")
    _produce_average_return_chart(statistic_series, save_as="../data/" + prefix + "_average_return.png")
