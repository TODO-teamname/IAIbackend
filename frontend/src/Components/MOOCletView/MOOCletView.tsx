import { Component } from 'react';
import { uid } from 'react-uid';
import MOOCletCreator from '../MOOCletCreator/MOOCletCreator';
import './moocletview.css';
import axios from 'axios';
import { MOOClet } from '../../types';

const BASE_URL = 'http://127.0.0.1:8000/api/';

interface Props {
  userId: number;
  organizationId: number;
}

interface State {
  userId: number;
  organizationId: number;
  mooclet_ids: number[];
  mooclets: MOOClet[];
}

export default class MOOCletView extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      userId: props.userId,
      organizationId: props.organizationId,
      mooclet_ids: [105, 106],
      mooclets: [],
    };
  }

  componentDidMount = (): void => {
    const mooclets = this.state.mooclets;
    for (const mooclet_id of this.state.mooclet_ids) {
      const url = BASE_URL + 'mooclet/?mooclet_id=' + mooclet_id;
      axios.get(url).then(
        (res) => {
          mooclets.push(res.data);
          this.setState({
            mooclets: mooclets,
          });
        },
        (err) => {
          console.log(err);
        },
      );
    }
  };

  addMOOClet = (mooclet_id: number): void => {
    const mooclets = this.state.mooclets;
    const url = BASE_URL + 'mooclet/?mooclet_id=' + mooclet_id;
    axios.get(url).then(
      (res) => {
        mooclets.push(res.data);
        this.setState({
          mooclets: mooclets,
        });
      },
      (err) => {
        console.log(err);
      },
    );
  };

  renderMOOClets = (): JSX.Element => {
    return (
      <div className="existing-mooclets-wrapper">
        <h1>Your MOOClets</h1>
        <div className="existing-mooclets">
          {this.state.mooclets.map((mooclet) => {
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
          {this.renderMOOClets()}
          {/* <MOOCletCreator submitCallback={this.addMOOClet} /> */}
        </div>
      </div>
    );
  }
}
