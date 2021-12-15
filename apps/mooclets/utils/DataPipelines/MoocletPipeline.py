from .DataPipeline import DataPipeline
from ..mooclet_connector import MoocletConnector
import json
import pandas as pd
import numpy as np
from typing import Dict, TextIO

# TODO: remove external api call
### USE THIS API TOKEN WITH CARE ###
from .. import mooclet_connector
import requests
MOOCLET_API_TOKEN = mooclet_connector.DUMMY_MOOCLET_API_TOKEN
URL = mooclet_connector.DUMMY_MOOCLET_URL


class MoocletPipeline(DataPipeline):
    def __init__(self, mooclet_connector: MoocletConnector, var_names: Dict):
        super().__init__(mooclet_connector)
        self.mooclet_connector = mooclet_connector
        self.var_names = var_names  # e.g. {"reward": "mturk_ts_reward_round_8", "policy": 6}
        
        self.intermediate_data = {}  # Dict[str, pd.DataFrame]
        self.output_data = None
        print("*********", self.var_names)


    # def _parse_data(self):
    #     values = pd.DataFrame(self.values["results"])
    #     values["timestamp"] = pd.to_datetime(values["timestamp"])
    #     values.sort_values(by=["timestamp"])
    #     self.output_data = values


    def get_output(self, file: TextIO=None):
        self.step_1_obtain_all_mooclet_data()
        self.step_2_combine_data()
        self.step_3_add_parameters_updates()
        self.step_4_add_timestamp_filters()

        if not file:
            return self.output_data
        else:
            file.seek(0)
            self.output_data.to_csv(file)
            file.flush()
            file.seek(0)
            
    # the following steps for constructing the csv is based on IAI's code
    # https://github.com/Intelligent-Adaptive-Interventions-Lab/MHA-Data-Collection/blob/main/DataPipelines/mturk_data_pipeline.py

    def step_1_obtain_all_mooclet_data(self):
        # endpoints = ["mooclet", "values", "versions", "policyparameters", "policyparametershistory", "policy"]
        
        # raw_mooclet = self.mooclet_connector.get_mooclet()  
        # raw_mooclet = pd.DataFrame.from_records(raw_mooclet, index=[0])[["id", "name"]]
        # self.intermediate_data["mooclet"] = raw_mooclet  # not being used again
        
        raw_values = self.mooclet_connector.get_values()
        raw_values = pd.DataFrame.from_records(raw_values["results"])
        raw_values = raw_values.sort_values(by=["learner", "timestamp"])
        raw_values = raw_values.drop_duplicates(subset=["learner", "timestamp"])

        raw_versions = raw_values[raw_values["variable"] == "version"]  # extracting rows from values table where it's for version value
        self.intermediate_data["versions"] = raw_versions.sort_values(by=["learner", "timestamp"])

        self.intermediate_data["rewards"] = raw_values[raw_values["variable"] == self.var_names["reward"]]  # extracting rows from values table where it's for reward value

        raw_policy_parameters = self.mooclet_connector.get_policy_parameters()
        raw_policy_parameters = pd.DataFrame.from_records(raw_policy_parameters["results"])
        self.intermediate_data["policy_parameters"] = raw_policy_parameters[raw_policy_parameters["policy"] == self.var_names["policy"]]
        
        raw_policy_parameters_history = self.mooclet_connector.get_policy_parameters_history()
        raw_policy_parameters_history = pd.DataFrame.from_records(raw_policy_parameters_history["results"])
        self.intermediate_data["policy_parameters_history"] = raw_policy_parameters_history.sort_values(by=["creation_time"])

        # self.intermediate_data["policies"] = get_policies()
        # TODO: remove external api call
        raw_policies = self.mooclet_connector.get_policies()
        self.intermediate_data["policies"] = pd.DataFrame.from_records(raw_policies["results"])

        self.intermediate_data["learners"] = sorted(raw_values["learner"].unique())
        
        draws = {}
        for _draw in ["precesion_draw", "coef_draw"]:
                draws[_draw] = raw_values[raw_values["variable"] == _draw]
        self.intermediate_data["draws"] = draws


    def step_2_combine_data(self):
        rewards = self.intermediate_data["rewards"]
        versions = self.intermediate_data["versions"]
        parameters = self.intermediate_data["policy_parameters"]
        all_draws = self.intermediate_data["draws"]
        prec_draws = all_draws["precesion_draw"]
        coef_draws = all_draws["coef_draw"]
        parametershistory = self.intermediate_data["policy_parameters_history"]

        rows = []
        for learner in self.intermediate_data["learners"]:
            version_l = versions[versions["learner"] == learner]
            rewards_l = rewards[rewards["learner"] == learner]
            for v_id in version_l.index:
                version = version_l.loc[[v_id]][["text", "timestamp", "policy", "version"]]
                version_id = version["version"][v_id]
                row_dict = {}
                row_dict["version"] = version["text"][v_id]
                arm_strs = row_dict["version"].lower().split(" ")
                arm = arm_strs[arm_strs.index("arm"): arm_strs.index("arm")+2]
                row_dict["arm"] = " ".join(arm)
                row_dict["learner"] = learner
                row_dict["assign_t"] = version["timestamp"][v_id]
                row_dict["next_assign_t"] = get_learner_next_assign_t(version_l, version["timestamp"][v_id])
                reward = get_reward_in_timewindow(rewards_l, row_dict["assign_t"], row_dict["next_assign_t"])
                if reward is not None:
                    row_dict["reward"] = reward["value"].values[0]
                    row_dict["reward_time"] = reward["timestamp"].values[0]
                else:
                    row_dict["reward"] = np.NaN
                    row_dict["reward_time"] = np.NaN
                row_dict["parameters"] = get_valid_parameter_set(parametershistory, parameters, row_dict["assign_t"])
                row_dict["policy"] = get_policy_by_policy_id(self.intermediate_data["policies"], version["policy"][v_id])
                prec_draw = prec_draws[prec_draws["learner"] == learner]
                coef_draw = coef_draws[coef_draws["learner"] == learner]
                prec_draw = prec_draw[prec_draw["version"] == version_id]
                coef_draw = coef_draw[coef_draw["version"] == version_id]
                prec_draw = get_valid_draws_set(prec_draw, row_dict["assign_t"])
                coef_draw = get_valid_draws_set(coef_draw, row_dict["assign_t"])
                if prec_draw.size > 0 and coef_draw.size > 0:
                    prev_draw = prec_draw["text"].values[0]
                    coef_draw = coef_draw["text"].values[0]
                    row_dict["precision_draw_data"] = np.fromstring(prev_draw[1:-1], sep=" ")
                    row_dict["coef_draw_data"] = np.fromstring(coef_draw[1:-1], sep=" ")
                rows.append(row_dict)
        combined_df = pd.DataFrame.from_records(rows)
        arm_early_no = sorted(list(combined_df["arm"].unique()))[0]
        combined_df[f"is_arm{arm_early_no.split(' ')[-1]}"] = (
                    combined_df["arm"] == arm_early_no)
        combined_df[f"is_arm{arm_early_no.split(' ')[-1]}"] = combined_df[
            f"is_arm{arm_early_no.split(' ')[-1]}"].astype(int)
        self.intermediate_data["version_json"] = f"is_arm{arm_early_no.split(' ')[-1]}"
        combined_df = combined_df.sort_values(by=["assign_t"])
        combined_df.reset_index(inplace=True, drop=True)
        combined_df = pd.concat([combined_df.drop(['parameters'], axis=1), combined_df['parameters'].apply(pd.Series)], axis=1)
        batch_groups = combined_df.groupby("variance_a").obj.set_index(
            "variance_a")
        batch_groups_list = list(batch_groups.index.unique())
        combined_df["batch_group"] = combined_df["variance_a"].apply(
            batch_groups_list.index)
        self.output_data = combined_df

    def step_3_add_parameters_updates(self):
        df = self.output_data
        df["index"] = df.index
        df["coef_mean_updated"] = repr(0)
        df["coef_cov_updated"] = repr(0)
        df["variance_a_updated"] = np.NaN
        df["variance_b_updated"] = np.NaN
        df["update_size_updated"] = np.NaN
        df["batch_group_updated"] = np.NaN
        obs_record = {}
        for i in df["batch_group"].unique():
            obs = df[df["batch_group"] == i]
            obs = obs.head(1)
            mean = obs["coef_mean"].values[0]
            cov = obs["coef_cov"].values[0]
            var_a = obs["variance_a"].values[0]
            var_b = obs["variance_b"].values[0]
            obs_record[var_a] = len(obs_record)
            if "update_size" not in obs:
                update_size = np.NaN
            else:
                update_size = obs["update_size"].values[0]
            if "update_record" not in obs:
                continue
            for dict in obs["update_record"].values[0]:
                round_no = self.var_names["reward"].split("_")[-1]
                arm_text = self.intermediate_data[
                               "version_json"] + f"_round_{round_no}"
                # df  -> df_learner -> df_learner_arm_value -> df_reward_value
                record = df[df["batch_group"] == i]
                record = record[record["learner"] == get_learner_name_by_id(self.mooclet_connector, int(dict["user_id"]))]
                record = record[
                    record[self.intermediate_data["version_json"]] == dict[
                        arm_text]]
                record = record[record["reward"] == dict[self.var_names["reward"]]]
                if record.shape[0] > 1:
                    record = record.head(1)
                if record.size > 0:
                    r_id = record["index"].values[0]
                    df.loc[r_id, "coef_mean_updated"] = repr(mean)
                    df.loc[r_id, "coef_cov_updated"] = repr(cov)
                    df.loc[r_id, "variance_a_updated"] = float(var_a)
                    df.loc[r_id, "variance_b_updated"] = float(var_b)
                    df.loc[r_id, "batch_group_updated"] = obs_record[var_a]
                    df.loc[r_id, "update_size_updated"] = update_size
        df["coef_mean_updated"] = df["coef_mean_updated"].apply(eval)
        df["coef_cov_updated"] = df["coef_cov_updated"].apply(eval)
        df["coef_cov_updated"] = df["coef_cov_updated"].replace(0, np.NaN)
        df["coef_mean_updated"] = df["coef_mean_updated"].replace(0, np.NaN)
        df = df.set_index("index")
        if "coef_draw" in list(df.columns) and "precesion_draw" in list(df.columns):
            self.output_data = df.drop(columns=["coef_draw", "precesion_draw"])
        else:
            self.output_data = df

    def step_4_add_timestamp_filters(self, start_time=None, end_time=None):
        if start_time:
            self.output_data = self.output_data[self.output_data["timestamp"] > start_time]
        if end_time:
            self.output_data = self.output_data[self.output_data["timestamp"] < end_time]
        return self.output_data



# helper functions

def get_reward_in_timewindow(rewards, start_time, end_time):
    if rewards is not None:
        rewards = rewards.sort_values(by=["timestamp"])
        if start_time:
            rewards = rewards[rewards["timestamp"] > start_time]
        if end_time:
            rewards = rewards[rewards["timestamp"] < end_time]
        if rewards.shape[0] == 0:
            return None
        if rewards.shape[0] > 1:
            print(f"WARNING: {rewards.shape[0]}More than one reward found")
        # get last record of filtered reward
        return rewards.tail(1)
    return None


def get_key_not_empty(rewards):
    for key in rewards:
        if rewards[key] is not None and len(rewards) > 0:
            return {key: rewards[key]}
    return None


def get_learner_next_assign_t(versions, a_t, mooclet_id=None,timestamp_key="timestamp"):
    if mooclet_id:
        versions = versions[versions["mooclet"] == mooclet_id]
    assignment_times = sorted(versions[timestamp_key].unique().tolist())
    i = assignment_times.index(a_t)
    try:
        next = assignment_times[i+1]
        return next
    except IndexError:
        return None


def build_var_names_dict():
    pass


def get_valid_parameter_set(parameterhistory, parameter, a_t):
    parameterhistory = parameterhistory[parameterhistory["creation_time"] > a_t]
    if parameterhistory.shape[0] >= 1:
        return parameterhistory.head(1)["parameters"].values[0]
    else:
        return parameter["parameters"].values[0]


def get_valid_draws_set(draws, a_t, timestamp="timestamp"):
    return draws[draws[timestamp] < a_t].tail(1)


def get_policy_by_policy_id(policies, p_id):
    return policies[policies["id"] == p_id]["name"].values[0]


def get_version_by_version_id(versions, v_id):
    try:
        return versions[versions["id"] == v_id]["name"].values[0]
    except:
        return None


def get_learner_name_by_id(mooclet_connector, learner_id):
    # TODO: move external api call
    result = mooclet_connector.get_learner(learner_id)
    return result["name"]


def get_valid_contextual_values(contextuals, timestamp):
    if contextuals is None or len(contextuals) == 0:
        return None
    else:
        result = {}
        for k , v in contextuals.items():
            v = v.sort_values(by=["timestamp"])
            result_df = v[(v["variable"] == k) & (v["timestamp"] < timestamp)].tail()
            if not result_df.empty:
                result[k] = result_df["value"].values[0]
        return result


def get_valid_groups(groups, timestamp, v_id):
    def _check_delta_time(timestamp, input_timestamp):
        return (timestamp - input_timestamp).seconds/60 < 3
    dfs = []
    for key in groups:
        value = groups[key]
        filtered = value[value["version"] == v_id]
        sorted = filtered.sort_values(by=["timestamp"])
        dfs.append(sorted)
    if len(dfs) != 0:
        groups = pd.concat(dfs)
        # try:
        print(f"DIFF: {timestamp - pd.to_datetime(groups['timestamp'])}")
        groups["diff"] = (timestamp - pd.to_datetime(groups["timestamp"])).seconds / 60
        print(list(groups["diff"]))
        return groups[(timestamp - groups["timestamp"]).seconds/60 < 3].tail()["text"].values[0]
    return None


# TODO: implement external api calls
# TODO: modify current workflow of writing to csv according to the following code:



# usage notes to be modified:
#     mooclet_id = [52]

    # mturk_datapipeline = MturkDataPipeline(mooclet_id, True)
    # mturk_datapipeline(var_names)



    #     def step_5_save_output_data(self, name=None):
    #     now = datetime.datetime.now()
    #     if not os.path.isdir("../output_files/"):
    #         os.mkdir("../output_files/")
    #     if not name:
    #         workbook_name = f"../output_files/mturk_datapipeline_{now}.csv"
    #     else:
    #         workbook_name = f"../output_files/{name}.csv"
    #     self.output_data.to_csv(workbook_name)

    # def step_6_get_summarized_data(self, groups, name=None):
    #     if not self.summarized:
    #         return
    #     else:
    #         now = datetime.datetime.now()
    #         if not os.path.isdir("../output_files/"):
    #             os.mkdir("../output_files/")
    #         if not name:
    #             workbook_name = f"../output_files/mturk_datapipeline_summarized_{now}.csv"
    #         else:
    #             workbook_name = f"../output_files/{name}.csv"
    #         mturk_summarizer = MTurkDataSummarizer()
    #         mturk_summarizer.construct_summarized_df(groups=groups, dataframe=self.output_data)
    #         mturk_summarizer.save_data(workbook_name)

    # def __call__(self, var_names):
    #     self.step_0_initialize_data_downloaders()
    #     self.step_1_obtain_processed_data(var_names)
    #     self.step_2_combine_data()
    #     self.step_3_add_parameters_updates(var_names)
    #     self.step_4_add_timestamp_filters()
    #     self.step_5_save_output_data()
    #     self.step_6_get_summarized_data(groups=["policy", "arm"])
