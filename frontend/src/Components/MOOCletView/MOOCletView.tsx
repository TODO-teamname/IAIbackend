import { Component } from 'react';
import { uid } from 'react-uid';
import { PolicyType } from '../../types';
import MOOCletCreator from '../MOOCletCreator/MOOCletCreator';
import './moocletview.css';

interface Props {
  userId: number;
  organizationId: number;
}

interface State {
  userId: number;
  organizationId: number;
}

export default class MOOCletView extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      userId: props.userId,
      organizationId: props.organizationId,
    };
  }

  renderMOOClets = (): JSX.Element => {
    const mooclets = [
      {
        id: 1,
        environment: null,
        mooclet_id: null,
        name: 'Test Mooclet 1',
        policy: PolicyType.choose_policy_group,
      },
      {
        id: 2,
        environment: null,
        mooclet_id: null,
        name: 'Test Mooclet 2',
        policy: PolicyType.choose_policy_group,
      },
    ]; // API: get all mooclets by org ID
    return (
      <div className="existing-mooclets-wrapper">
        <h1>Your MOOClets</h1>
        <div className="existing-mooclets">
          {mooclets.map((mooclet) => {
            return (
              <div className="existing-mooclet" key={uid(mooclet)}>
                <p>
                  <b>Name: </b>
                  {mooclet.name}
                </p>
                <p>
                  <b>Policy: </b>
                  {mooclet.policy}
                </p>
              </div>
            );
          })}
        </div>
      </div>
    );
  };

  render(): JSX.Element {
    return (
      <div className="moocletview-wrapper">
        <div className="moocletview">
          <MOOCletCreator />
          {this.renderMOOClets()}
        </div>
      </div>
    );
  }
}
