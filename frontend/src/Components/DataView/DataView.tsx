import { Component } from 'react';
import { Button } from '@mui/material';
import './dataview.css';
import { isPropertySignature } from 'typescript';

interface Props {
  moocletID: number;
  organizationID: number;
  moocletName: string;
  moocletPolicy: number;
}

interface State {
  moocletID: number;
  organizationID: number;
  moocletName: string;
  moocletPolicy: number;
}

export default class DataView extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      moocletID: props.moocletID,
      organizationID: props.organizationID,
      moocletName: props.moocletName,
      moocletPolicy: props.moocletPolicy,
    };
  }

  downloadData = (): void => {
    alert('Your data is being downloaded');
    // add some call here so that the data is actually downloaded
  };

  renderDownloadButton = (): JSX.Element => {
    return (
      <Button onClick={this.downloadData} variant="outlined">
        Download
      </Button>
    );
  };

  renderMOOCletDetails = (): JSX.Element => {
    const details = {
      moocletName: this.state.moocletName,
      moocletID: this.state.moocletID,
      organizationID: this.state.organizationID,
      policy: this.state.moocletPolicy,
    };
    return (
      <div className="details-wrapper">
        <p>
          This is the dataview for your MOOClet with <i>id</i> {details.moocletID}. Here are its details:{' '}
        </p>
        <p>
          The <i>name</i> is: {details.moocletName}
        </p>
        <p>
          The <i>organizationID</i> is: {details.organizationID}
        </p>
        <p>
          The <i>policy</i> is: {details.policy}
        </p>
      </div>
    );
  };

  render(): JSX.Element {
    // in this section we need to call the API to figure out these details
    return (
      <div className="dataview-wrapper">
        <h1>Your MOOClet Data</h1>
        <div className="details-wrapper">{this.renderMOOCletDetails()}</div>
        {/* <div className="download-wrapper">{this.renderDownloadButton()}</div>
        <p></p> */}
      </div>
    );
  }
}

/*
The main things we still have to do are:
      - modify details so that it calls the API and actually retrieves the mooclet's details
      - add some place where the user actually specifies the moocletID to pass into DataView
      - add a call to backend in downloadData so that it actually gets downloaded
      - (later, perhaps D3): actually display the data in some form, such as:
          - having a preview of the reformatted csv file
          - reformatting the data in such a way that we can graph it
      - (later, for D3): allow for some statistical tests:
          - access and reformat the data so that we can set up statistical tests
          - have a dropdown of what tests they can do, and then run them
      - other things:
          - (for D2 / D3): either add a section for all of this user's mooclets at the top, or 
            have this view called underneath the MOOCletView so that the user can see all their 
            mooclets
          - (for D3): add a dropdown menu so the user can select which of their mooclets they want 
            the data view for
*/
