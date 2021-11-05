import { Add } from '@mui/icons-material';
import { Button, MenuItem, Select, SelectChangeEvent, TextField, Tooltip } from '@mui/material';
import { Component, FormEvent, SyntheticEvent } from 'react';
import { uid } from 'react-uid';
import {
  PolicyType,
  ChoosePolicyGroupParameters,
  TSConfigurableParameters,
  ThompsonSamplingContextualParameters,
} from '../../types';
import './moocletcreator.css';

// eslint-disable-next-line @typescript-eslint/no-empty-interface
interface Props {}

interface PolicyFragment {
  policy: number;
  parameters:
    | Record<string, never>
    | ChoosePolicyGroupParameters
    | TSConfigurableParameters
    | ThompsonSamplingContextualParameters;
}

interface State {
  moocletName: string;
  policies: PolicyFragment[];
  variables: string[];
  versions: string[];
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
    };
  }

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
      case PolicyType.thompson_sampling_contextual:
        break;
      case PolicyType.ts_configurable:
        break;
    }
    this.setState({});
  };

  updatePolicyParams = (e: SyntheticEvent, policyFragment: PolicyFragment): void => {
    const target = e.target as HTMLInputElement;
    const params = policyFragment.parameters as ChoosePolicyGroupParameters;
    params.policy_options[target.name] = parseFloat(target.value);
    this.setState({}, () => console.log(policyFragment));
  };

  handleSubmit = (e: FormEvent): void => {
    e.preventDefault();
    console.log('Submitting new MOOClet', this.state.moocletName, this.state.policies);
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
                onClick={(e) => this.updatePolicyParams(e, policyFragment)}
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
                onClick={(e) => this.updatePolicyParams(e, policyFragment)}
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
                onClick={(e) => this.updatePolicyParams(e, policyFragment)}
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
                name="batch-size"
                label="Batch Size"
                InputProps={{
                  inputProps: {
                    min: 1,
                    step: 1,
                  },
                }}
              />
            </Tooltip>
            <Tooltip title="Max Rating">
              <TextField
                className="policy-menu-item"
                required
                type="number"
                name="max-rating"
                label="Max Rating"
                InputProps={{
                  inputProps: {
                    min: 0,
                  },
                }}
              />
            </Tooltip>
            <Tooltip title="Min Rating (Optional)">
              <TextField
                className="policy-menu-item"
                type="number"
                name="min-rating"
                label="Min Rating (Optional)"
                InputProps={{
                  inputProps: {
                    min: 0,
                  },
                }}
              />
            </Tooltip>
            <Tooltip title="Uniform Threshold (contains burn-in size)">
              <TextField
                className="policy-menu-item"
                required
                type="number"
                name="uniform-threshold"
                label="Uniform Threshold"
                InputProps={{
                  inputProps: {
                    min: 0,
                    step: 1,
                  },
                }}
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
                    min: 0.00001,
                    step: 0.00001,
                    max: 0.99999,
                  },
                }}
              />
            </Tooltip>
            <Tooltip title="Outcome Variable Name">
              <TextField
                className="policy-menu-item"
                required
                type="string"
                name="outcome-variable-name"
                label="Outcome Variable Name"
              />
            </Tooltip>
          </div>
        );
        break;
      case PolicyType.thompson_sampling_contextual:
        return (
          <div className="policy-menu ts-contextual-menu">
            <TextField className="policy-menu-item" />
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
          <div className="new-mooclet-form-section">
            <Tooltip title="Add new variable">
              <Button>
                <Add />
              </Button>
            </Tooltip>
          </div>
          <h2>Versions</h2>
          <div className="new-mooclet-form-section">
            <Tooltip title="Add new version">
              <Button>
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
      </div>
    );
  }
}
