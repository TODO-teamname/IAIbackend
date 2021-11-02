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

// TODO: ask for policy types
export enum PolicyType {
  Noncontextual2x3FactorialThompsonSampling,
  NoncontextualSingleFactorThompsonSampling,
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
  parameters: {
    policy_options: {}; // what here <--
  };
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
