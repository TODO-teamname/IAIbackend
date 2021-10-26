import { Component } from 'react';
import './moocletview.css';

interface Props {
  moocletId: number | null;
}

interface State {
  moocletId: number;
}

export default class MOOCletView extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    const moocletId = props.moocletId || 0; // TODO: api call to get a new mooclet id
    this.state = {
      moocletId: moocletId,
    };
  }

  render(): JSX.Element {
    return <p>MOOCLET</p>;
  }
}
