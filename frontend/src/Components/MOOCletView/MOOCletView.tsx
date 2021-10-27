import { Component } from 'react';
import { uid } from 'react-uid';
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
    const mooclets = [{}]; // API: get all mooclets by org ID
    return (
      <div className="existing-mooclets">
        {mooclets.map((mooclet) => {
          return <div key={uid(mooclet)}></div>;
        })}
      </div>
    );
  };

  render(): JSX.Element {
    return (
      <div className="moocletview-wrapper">
        <p>MOOCletView</p>
        <MOOCletCreator />
        <h1>Your MOOClets</h1>
        {this.renderMOOClets}
      </div>
    );
  }
}
