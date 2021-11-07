import { Add, Close } from '@mui/icons-material';
import {
  Alert,
  AlertTitle,
  Button,
  FormControlLabel,
  MenuItem,
  Select,
  SelectChangeEvent,
  Switch,
  TextField,
  Tooltip,
} from '@mui/material';
import { Component, FormEvent, SyntheticEvent } from 'react';
import { uid } from 'react-uid';
import {
  PolicyType,
  ChoosePolicyGroupParameters,
  TSConfigurableParameters,
  ThompsonSamplingContextualParameters,
} from '../../types';
import './moocletcreator.css';
import axios from 'axios';

const BASE_URL = 'http://127.0.0.1:8000/api/';

// eslint-disable-next-line @typescript-eslint/no-empty-interface
interface Props {
  // eslint-disable-next-line no-unused-vars
  submitCallback: (arg0: number) => void;
}

interface PolicyFragment {
  policy: number;
  parameters:
    | Record<string, never>
    | ChoosePolicyGroupParameters
    | TSConfigurableParameters
    | ThompsonSamplingContextualParameters;
}

interface VariableFragment {
  name: string;
}

interface VersionFragment {
  name: string;
}

interface State {
  moocletName: string;
  policies: PolicyFragment[];
  variables: VariableFragment[];
  versions: VersionFragment[];
  showAlert: boolean;
  alertTexts: string[];
}

export default class MOOCletCreator extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      moocletName: '',
      policies: [
        {
          policy: PolicyType.choose_policy_group,
          parameters: {
            policy_options: {},
          },
        },
      ],
      variables: [],
      versions: [],
      showAlert: false,
      alertTexts: [],
    };
  }

  handleSubmit = (e: FormEvent): void => {
    e.preventDefault();
    if (this.validateNewMOOClet()) {
      // POST new MOOClet
      const policies = this.state.policies.map((policy) => policy.policy);
      const policy = policies.includes(PolicyType.choose_policy_group)
        ? PolicyType.choose_policy_group
        : this.state.policies[0].policy;
      const mooclet_url = BASE_URL + 'mooclet/?policy_id=' + policy + '&mooclet_name=' + this.state.moocletName;
      console.log(this.state.policies);
      console.log('Submitting new MOOClet', mooclet_url);
      axios.post(mooclet_url).then(
        (res) => {
          console.log(res);
          this.props.submitCallback(res.data.id);
        },
        (err) => {
          console.log(err);
        },
      );

      // POST policies
      for (const policy of this.state.policies) {
        // const policy_url = BASE_URL + ''
        // TODO: POST policy
      }

      // POST versions
      for (const version of this.state.versions) {
        // TODO: POST version
      }

      // POST variables
      for (const variable of this.state.variables) {
        // TODO: POST variable
      }
    }
  };

  validateNewMOOClet = (): boolean => {
    let validation = true;
    const validationMessages = [];
    // Validate that there is at least one policy
    if (this.state.policies.length <= 0) {
      validationMessages.push('You must have at least one policy.');
      validation = false;
    }
    const policyTypes = this.state.policies.map((policy) => policy.policy);
    // Validate no duplicate policies
    if (new Set(policyTypes).size !== policyTypes.length) {
      validationMessages.push('You may only have at most one of each policy type.');
      validation = false;
    }
    // Validate CPG if more than 1 policy
    if (policyTypes.length > 1 && !policyTypes.includes(PolicyType.choose_policy_group)) {
      validationMessages.push('You must use Choose Policy Group if you have more than one policy.');
      validation = false;
    }
    // Validate Policies
    for (const policy of this.state.policies) {
      switch (policy.policy) {
        case PolicyType.choose_policy_group:
          const paramsCPG = policy.parameters as ChoosePolicyGroupParameters;
          let probabilitySums = 0;
          for (const option of Object.values(paramsCPG.policy_options)) {
            probabilitySums += option;
          }
          if (probabilitySums != 1) {
            validationMessages.push('Choose Policy Group probabilities must add up to 1.');
            validation = false;
          }
          break;
        case PolicyType.ts_configurable:
          const paramsTSConfig = policy.parameters as TSConfigurableParameters;
          if (paramsTSConfig.min_rating && paramsTSConfig.min_rating >= paramsTSConfig.max_rating) {
            validationMessages.push('Min rating must be lower than max rating.');
            validation = false;
          }
          break;
        case PolicyType.thompson_sampling_contextual:
          // const paramsTSContext = policy.parameters as ThompsonSamplingContextualParameters;
          break;
      }
    }
    this.setState({
      showAlert: !validation,
      alertTexts: validationMessages,
    });
    return validation;
  };

  handleNameChange = (e: SyntheticEvent): void => {
    const target = e.target as HTMLInputElement;
    const value = target.value;
    this.setState({
      moocletName: value,
    });
  };

  updatePolicyType = (e: SelectChangeEvent<unknown>, policyFragment: PolicyFragment): void => {
    policyFragment.policy = parseInt(e.target.value as string);
    switch (e.target.value) {
      case PolicyType.choose_policy_group:
        policyFragment.parameters = {
          policy_options: {},
        };
        break;
      case PolicyType.ts_configurable:
        policyFragment.parameters = {
          prior: {
            failure: 1,
            success: 1,
          },
          batch_size: 1,
          max_rating: 1,
          min_rating: undefined,
          uniform_threshold: 1,
          tspostdiff_thresh: undefined,
          outcome_variable_name: 'unknown',
        };
        break;
      case PolicyType.thompson_sampling_contextual:
        policyFragment.parameters = {
          coef_cov: [[]] as number[][],
          coef_mean: [] as number[],
          batch_size: 1,
          variance_a: 2,
          variance_b: 1,
          action_space: {},
          outcome_variable: 'unknown',
          include_intercept: true,
          uniform_threshold: 1,
          regression_formula: '',
          contextual_variables: [],
        };
        break;
    }
    this.setState({});
  };

  updatePolicyParams = (e: SyntheticEvent, policyFragment: PolicyFragment): void => {
    const target = e.target as HTMLInputElement;
    switch (policyFragment.policy) {
      case PolicyType.choose_policy_group:
        const cpgParams = policyFragment.parameters as ChoosePolicyGroupParameters;
        cpgParams.policy_options[target.name] = parseFloat(target.value);
        break;
      case PolicyType.ts_configurable:
        const tsConfigParams = policyFragment.parameters as TSConfigurableParameters;
        switch (target.name) {
          case 'batch_size':
            tsConfigParams.batch_size = parseInt(target.value);
            break;
          case 'max_rating':
            tsConfigParams.max_rating = parseFloat(target.value);
            break;
          case 'min_rating':
            tsConfigParams.min_rating = parseFloat(target.value);
            break;
          case 'uniform_threshold':
            tsConfigParams.uniform_threshold = parseInt(target.value);
            break;
          case 'tspostdiff_thresh':
            tsConfigParams.tspostdiff_thresh = parseFloat(target.value);
            break;
          case 'outcome_variable_name':
            tsConfigParams.outcome_variable_name = target.value;
            break;
        }
        break;
      case PolicyType.thompson_sampling_contextual:
        const tsContextualParams = policyFragment.parameters as ThompsonSamplingContextualParameters;
        switch (target.name) {
          case 'batch_size':
            tsContextualParams.batch_size = parseInt(target.value);
            break;
          case 'variance_a':
            tsContextualParams.variance_a = parseFloat(target.value);
            break;
          case 'variance_b':
            tsContextualParams.variance_b = parseFloat(target.value);
            break;
          case 'action_space':
            break;
          case 'outcome_variable':
            tsContextualParams.outcome_variable = target.value;
            break;
          case 'include_intercept':
            tsContextualParams.include_intercept = target.checked;
            break;
          case 'uniform_threshold':
            tsContextualParams.uniform_threshold = parseInt(target.value);
            break;
        }
    }
    // Debug:
    // this.setState({}, () => console.log(policyFragment));
    this.setState({});
  };

  renderPolicy = (policyFragment: PolicyFragment): JSX.Element => {
    switch (policyFragment.policy) {
      case PolicyType.choose_policy_group:
        return (
          <div className="policy-menu choose-policy-group-menu">
            <Tooltip title="Probability of Uniform Random">
              <TextField
                className="policy-menu-item"
                type="number"
                required
                name="uniform_random"
                label="Uniform Random"
                InputProps={{
                  inputProps: {
                    max: 1,
                    min: 0,
                    step: 0.01,
                  },
                }}
                onChange={(e) => this.updatePolicyParams(e, policyFragment)}
              />
            </Tooltip>
            <Tooltip title="Probability of TS Configurable">
              <TextField
                className="policy-menu-item"
                type="number"
                required
                name="ts_configurable"
                label="TS Configurable"
                InputProps={{
                  inputProps: {
                    max: 1,
                    min: 0,
                    step: 0.01,
                  },
                }}
                onChange={(e) => this.updatePolicyParams(e, policyFragment)}
              />
            </Tooltip>
            <Tooltip title="Probability of Thompson Sampling Contextual">
              <TextField
                className="policy-menu-item"
                type="number"
                required
                name="thompson_sampling_contexual"
                label="Thompson Sampling Contextual"
                InputProps={{
                  inputProps: {
                    max: 1,
                    min: 0,
                    step: 0.01,
                  },
                }}
                onChange={(e) => this.updatePolicyParams(e, policyFragment)}
              />
            </Tooltip>
          </div>
        );
        break;
      case PolicyType.ts_configurable:
        return (
          <div className="policy-menu ts-configurable-menu">
            <Tooltip title="Batch Size">
              <TextField
                className="policy-menu-item"
                required
                type="number"
                name="batch_size"
                label="Batch Size"
                InputProps={{
                  inputProps: {
                    min: 1,
                    step: 1,
                  },
                }}
                onChange={(e) => this.updatePolicyParams(e, policyFragment)}
              />
            </Tooltip>
            <Tooltip title="Max Rating">
              <TextField
                className="policy-menu-item"
                required
                type="number"
                name="max_rating"
                label="Max Rating"
                InputProps={{
                  inputProps: {
                    min: 0,
                  },
                }}
                onChange={(e) => this.updatePolicyParams(e, policyFragment)}
              />
            </Tooltip>
            <Tooltip title="Min Rating (Optional)">
              <TextField
                className="policy-menu-item"
                type="number"
                name="min_rating"
                label="Min Rating (Optional)"
                InputProps={{
                  inputProps: {
                    min: 0,
                  },
                }}
                onChange={(e) => this.updatePolicyParams(e, policyFragment)}
              />
            </Tooltip>
            <Tooltip title="Uniform Threshold (contains burn-in size)">
              <TextField
                className="policy-menu-item"
                required
                type="number"
                name="uniform_threshold"
                label="Uniform Threshold"
                InputProps={{
                  inputProps: {
                    min: 0,
                    step: 1,
                  },
                }}
                onChange={(e) => this.updatePolicyParams(e, policyFragment)}
              />
            </Tooltip>
            <Tooltip title="TS PostDiff Threshold (Optional)">
              <TextField
                className="policy-menu-item"
                type="number"
                name="tspostdiff_thresh"
                label="TS PostDiff Thresh (Optional)"
                InputProps={{
                  inputProps: {
                    min: 0.00001, //TODO: ask about this
                    step: 0.00001,
                    max: 0.99999,
                  },
                }}
                onChange={(e) => this.updatePolicyParams(e, policyFragment)}
              />
            </Tooltip>
            <Tooltip title="Outcome Variable Name">
              <TextField
                className="policy-menu-item"
                required
                name="outcome_variable_name"
                label="Outcome Variable Name"
                onChange={(e) => this.updatePolicyParams(e, policyFragment)}
              />
            </Tooltip>
          </div>
        );
        break;
      case PolicyType.thompson_sampling_contextual:
        return (
          <div className="policy-menu ts-contextual-menu">
            <TextField
              className="policy-menu-item"
              required
              type="number"
              name="batch_size"
              label="Batch Size"
              InputProps={{
                inputProps: {
                  min: 1,
                  step: 1,
                },
              }}
              onChange={(e) => this.updatePolicyParams(e, policyFragment)}
            />
            <TextField
              className="policy-menu-item"
              required
              type="number"
              name="variance_a"
              label="Variance A"
              onChange={(e) => this.updatePolicyParams(e, policyFragment)}
            />
            <TextField
              className="policy-menu-item"
              required
              type="number"
              name="variance_b"
              label="Variance B"
              onChange={(e) => this.updatePolicyParams(e, policyFragment)}
            />
            <TextField
              className="policy-menu-item"
              required
              name="outcome_variable"
              label="Outcome Variable"
              onChange={(e) => this.updatePolicyParams(e, policyFragment)}
            />
            <FormControlLabel
              control={
                <Switch
                  className="policy-menu-item"
                  defaultChecked
                  name="include_intercept"
                  onChange={(e) => this.updatePolicyParams(e, policyFragment)}
                />
              }
              label="Include Intercept"
            />
            <TextField
              className="policy-menu-item"
              required
              type="number"
              name="uniform_threshold"
              label="Uniform Threshold"
              InputProps={{
                inputProps: {
                  min: 0,
                  step: 1,
                },
              }}
              onChange={(e) => this.updatePolicyParams(e, policyFragment)}
            />
          </div>
        );
        break;
      default:
        return (
          <div className="policy-menu empty-policy-menu">
            <p>Please Choose a Policy</p>
          </div>
        );
        break;
    }
  };

  removePolicy = (policy: PolicyFragment): void => {
    this.setState({
      policies: this.state.policies.filter((p) => p !== policy),
    });
  };

  render(): JSX.Element {
    return (
      <div className="mooclet-creator">
        <h1>New MOOClet</h1>
        <form onSubmit={this.handleSubmit} className="new-mooclet-form">
          <div className="new-mooclet-form-section">
            <TextField
              required
              name="moocletName"
              label="MOOClet Name"
              value={this.state.moocletName}
              onChange={this.handleNameChange}
            />
          </div>
          <h2>Policies</h2>
          {this.state.policies.map((policy) => {
            return (
              <div key={uid(policy)} className="new-mooclet-form-section bottom-border">
                <Select
                  className="policy-select"
                  required
                  name="policy"
                  value={policy.policy}
                  onChange={(e) => this.updatePolicyType(e, policy)}
                >
                  <MenuItem value={PolicyType.choose_policy_group}>Choose Policy Group</MenuItem>
                  <MenuItem value={PolicyType.thompson_sampling_contextual}>Thompson Sampling Contextual</MenuItem>
                  <MenuItem value={PolicyType.ts_configurable}>TS Configurable</MenuItem>
                </Select>
                <Button
                  color="error"
                  onClick={() => {
                    this.setState({
                      policies: this.state.policies.filter((p) => p !== policy),
                    });
                  }}
                >
                  <Close />
                </Button>
                {this.renderPolicy(policy)}
              </div>
            );
          })}
          <div className="new-mooclet-form-section">
            <Tooltip title="Add new policy">
              <Button
                onClick={() => {
                  const policies = this.state.policies;
                  policies.push({
                    policy: PolicyType.choose_policy_group,
                    parameters: {
                      policy_options: {},
                    },
                  });
                  this.setState({
                    policies: policies,
                  });
                }}
              >
                <Add />
              </Button>
            </Tooltip>
          </div>
          <h2>Variables</h2>
          {this.state.variables.map((variable) => {
            return (
              <div key={uid(variable)} className="new-mooclet-form-section">
                <TextField
                  required
                  className="variable"
                  name="variable_name"
                  label="Variable Name"
                  onChange={(e) => {
                    const vars = this.state.variables;
                    const index = this.state.variables.indexOf(variable);
                    vars[index].name = e.target.value;
                    this.setState({
                      variables: vars,
                    });
                  }}
                />
                <Button
                  color="error"
                  onClick={() => {
                    this.setState({
                      variables: this.state.variables.filter((v) => v !== variable),
                    });
                  }}
                >
                  <Close />
                </Button>
              </div>
            );
          })}
          <div className="new-mooclet-form-section">
            <Tooltip title="Add new variable">
              <Button
                onClick={() => {
                  const vars = this.state.variables;
                  vars.push({ name: '' });
                  this.setState({
                    variables: vars,
                  });
                }}
              >
                <Add />
              </Button>
            </Tooltip>
          </div>
          <h2>Versions</h2>
          {this.state.versions.map((version) => {
            return (
              <div key={uid(version)} className="new-mooclet-form-section">
                <TextField
                  required
                  className="version"
                  name="version_name"
                  label="Version Name"
                  onChange={(e) => {
                    const vers = this.state.versions;
                    const index = this.state.versions.indexOf(version);
                    vers[index].name = e.target.value;
                    this.setState({
                      versions: vers,
                    });
                  }}
                />
                <Button
                  color="error"
                  onClick={() => {
                    this.setState({
                      versions: this.state.versions.filter((v) => v !== version),
                    });
                  }}
                >
                  <Close />
                </Button>
              </div>
            );
          })}
          <div className="new-mooclet-form-section">
            <Tooltip title="Add new version">
              <Button
                onClick={() => {
                  const vers = this.state.versions;
                  vers.push({ name: '' });
                  this.setState({
                    versions: vers,
                  });
                }}
              >
                <Add />
              </Button>
            </Tooltip>
          </div>
          <div className="new-mooclet-form-section">
            <Button type="submit" variant="contained">
              Submit
            </Button>
          </div>
        </form>
        <div className="alert-container">
          {this.state.showAlert ? (
            // eslint-disable-next-line @typescript-eslint/no-empty-function
            <Alert
              severity="error"
              onClose={() => {
                this.setState({ showAlert: false });
              }}
            >
              <AlertTitle>MOOClet Creation Failed</AlertTitle>
              {this.state.alertTexts.map((alert) => {
                return <p key={uid(alert)}>{alert}</p>;
              })}
            </Alert>
          ) : null}
        </div>
      </div>
    );
  }
}
