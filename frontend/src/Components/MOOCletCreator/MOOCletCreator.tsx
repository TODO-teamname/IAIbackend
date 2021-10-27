import { Button, FormControl, TextField } from '@mui/material';
import { Component, SyntheticEvent } from 'react';
import './moocletcreator.css';

interface Props {}

interface State {
  moocletName: string;
  policyId: number;
}

export default class MOOCletCreator extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      moocletName: '',
      policyId: 0,
    };
  }

  handleInputChange = (e: SyntheticEvent): void => {
    const target = e.target as HTMLInputElement;
    const value = target.type === 'checkbox' ? target.checked : target.value;
    const name = target.name;
    this.setState({
      [name]: value,
    } as any); // <-- Hack
  };

  handleSubmit = (e: SyntheticEvent): void => {
    e.preventDefault();
    console.log('Submitting new MOOClet');
  };

  render(): JSX.Element {
    return (
      <div className="mooclet-creator">
        <form onSubmit={this.handleSubmit}>
          <FormControl className="new-mooclet-form">
            <TextField
              required
              name="moocletName"
              label="MOOClet Name"
              value={this.state.moocletName}
              onChange={this.handleInputChange}
            />
            <TextField
              required
              name="policyId"
              label="Policy"
              value={this.state.policyId}
              onChange={this.handleInputChange}
              type="number"
            />
            <Button type="submit" variant="contained">
              Submit
            </Button>
          </FormControl>
        </form>
      </div>
    );
  }
}
