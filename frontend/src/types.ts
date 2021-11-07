/* eslint-disable no-unused-vars */
export interface User {
  id: number;
  name: string;
  email: never; // must be encrypted
  password: never; // must be encrypted
  gooogle_drive_info: unknown;
  organizations: number[]; // Array of Organization.id
}

export interface Organization {
  id: number;
  name: string;
  admins: number[]; // Array of User.id
  staff: number[]; // Array of User.id
  mooclets: unknown; // All mooclet objects belong to orgs, unknown shape (could be the IAI API access token?)
}

export enum PolicyType {
  thompson_sampling_contextual = 6,
  choose_policy_group = 12,
  ts_configurable = 17,
}

export interface MOOClet {
  id: number;
  environment: null;
  mooclet_id: null;
  name: string;
  policy: number;
}

export interface Policy {
  id: number;
  mooclet: number;
  policy: number;
  parameters: Record<string, unknown>;
}

export interface ChoosePolicyGroupParameters {
  policy_options: {
    [index: string]: number;
  };
}

export interface TSConfigurableParameters {
  prior: {
    success: number;
    failure: number;
  };
  batch_size: number;
  max_rating: number;
  min_rating: number | undefined;
  uniform_threshold: number;
  tspostdiff_thresh: number | undefined;
  outcome_variable_name: string; // TODO: Ask why this is outcome_variable_name and tsContext is just outcome_variable ?
}

export interface ThompsonSamplingContextualParameters {
  coef_cov: number[][];
  coef_mean: number[];
  batch_size: number;
  variance_a: number;
  variance_b: number;
  action_space: Record<string, number[]>;
  outcome_variable: string;
  include_intercept: boolean;
  uniform_threshold: number;
  regression_formula: string; //"dummy_reward_name ~ isarm1 + context1 * isarm1 + context2 * isarm1"
  contextual_variables: string[];
}

export interface Variable {
  id: number;
  environment: null;
  variable_id: null;
  name: string;
}

export interface Version {
  id: number;
  name: string;
  text: string;
  version_id: null;
  mooclet: number; // MOOClet.id ?
  version_json: JSON;
}

export interface Value {
  id: number;
  variable: string; // Variable.name
  learner: string;
  mooclet: number; // MOOClet.id ?
  version: number; // Version.id ?
  policy: number; // Policy.id ?
  value: number;
  text: string;
  timestamp: Date;
}
