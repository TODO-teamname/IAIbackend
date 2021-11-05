import { Component } from 'react';
import './dataview.css';

interface Props {
  moocletID: number;
  organizationId: number;
}

interface State {
  moocletID: number;
  organizationId: number;
}

export default class DataView extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      moocletID: props.moocletID,
      organizationId: props.organizationId,
    };
  }

  render(): JSX.Element {
    // in this section we need to call the API to figure out these details
    const details = {
      name: 'Dummy Name',
      id: this.state.moocletID,
      environment: 'This is a dummy environment',
      policy: 0,
    };
    return (
      <div className="dataview-wrapper">
        <p>This is a the dataview for your MOOClet with id {details.id}. Here are its details: </p>
        <div className="details-wrapper">
          <p>The name is: {details.name}</p>
          <p>The environment is: {details.environment}</p>
          <p>The policy is: {details.policy}</p>
        </div>
        <h1>Your MOOClet Data</h1>
      </div>
    );
  }
}

/*
The main things we still have to do are:
      - modify details so that it calls the API and actually retrieves the mooclet's details
      - add some place where the user actually specifies the moocletID to pass into DataView
      - perhaps add the "Download this MOOClet's data" button at the end
      - (later, perhaps D3): actually display the data in some form, such as:
          - having a preview of the reformatted csv file
          - reformatting the data in such a way that we can graph it
      - (later, for D3): allow for some statistical tests:
          - access and reformat the data so that we can set up statistical tests
          - have a dropdown of what tests they can do, and then run them
      - other things:
          - (for D2): clean up the code a little bit and separate things into their own functions
          - (for D2 / D3): either add a section for all of this user's mooclets at the top, or 
            have this view called underneath the MOOCletView so that the user can see all their 
            mooclets
          - (for D3): add a dropdown menu so the user can select which of their mooclets they want 
            the data view for
*/
