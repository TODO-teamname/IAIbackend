import * as React from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import IconButton from '@mui/material/IconButton';
import AccountCircle from '@mui/icons-material/AccountCircle';
import People from '@mui/icons-material/People';
import Settings from '@mui/icons-material/Settings';
import MenuItem from '@mui/material/MenuItem';
import Menu from '@mui/material/Menu';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import { CardActionArea } from '@mui/material';
import { useHistory } from 'react-router-dom';
import MOOCletCreator from '../MOOCletCreator/MOOCletCreator';
import { uid } from 'react-uid';

interface MOOCletInfo {
  name: string;
  policy: number;
}

export default function Dashboard(): JSX.Element {
  const [auth] = React.useState(true);
  const [accountAnchorEl, setAccountAnchorEl] = React.useState<null | HTMLElement>(null);
  const [settingsAnchorEl, setSettingsAnchorEl] = React.useState<null | HTMLElement>(null);
  const [MOOClets, setMOOClets] = React.useState<MOOCletInfo[]>([
    {
      name: 'MHA - November',
      policy: 6,
    },
    {
      name: 'MHA - October',
      policy: 12,
    },
  ]);

  // const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
  //   setAuth(event.target.checked);
  // };

  const handleAccountMenu = (event: React.MouseEvent<HTMLElement>) => {
    setAccountAnchorEl(event.currentTarget);
  };

  const handleSettingsMenu = (event: React.MouseEvent<HTMLElement>) => {
    setSettingsAnchorEl(event.currentTarget);
  };

  const handleAccountClose = () => {
    setAccountAnchorEl(null);
  };

  const handleSettingsClose = () => {
    setSettingsAnchorEl(null);
  };
  const history = useHistory();

  const handleRoute = (pagePath: string) => {
    history.push(pagePath);
  };

  const navbar = () => {
    return (
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            MOOClet Dashboard
          </Typography>
          {auth && (
            <div>
              <IconButton size="large" aria-label="organizations of current user" aria-haspopup="true" color="inherit">
                <People />
              </IconButton>
              <IconButton
                size="large"
                aria-label="account of current user"
                aria-controls="account-menu-appbar"
                aria-haspopup="true"
                onClick={handleAccountMenu}
                color="inherit"
              >
                <AccountCircle />
              </IconButton>
              <Menu
                id="account-menu-appbar"
                anchorEl={accountAnchorEl}
                anchorOrigin={{
                  vertical: 'top',
                  horizontal: 'right',
                }}
                keepMounted
                transformOrigin={{
                  vertical: 'top',
                  horizontal: 'right',
                }}
                open={Boolean(accountAnchorEl)}
                onClose={handleAccountClose}
              >
                <MenuItem onClick={handleAccountClose}>My Account</MenuItem>
                <MenuItem onClick={() => handleRoute('/login')}>Sign Out</MenuItem>
              </Menu>
            </div>
          )}
        </Toolbar>
      </AppBar>
    );
  };

  return (
    <>
      <Box sx={{ flexGrow: 1 }}>{navbar()}</Box>
      <div style={{ marginLeft: '1%' }}>
        <h1>Your Organizations</h1>
        <h2 style={{ float: 'left' }}>CSC301</h2>
        <div style={{ float: 'right' }}>
          <IconButton
            size="large"
            aria-label="account of current user"
            aria-controls="settings-menu-appbar"
            aria-haspopup="true"
            onClick={handleSettingsMenu}
            color="inherit"
          >
            <Settings />
          </IconButton>
          <Menu
            id="settings-menu-appbar"
            anchorEl={settingsAnchorEl}
            anchorOrigin={{
              vertical: 'top',
              horizontal: 'right',
            }}
            keepMounted
            transformOrigin={{
              vertical: 'top',
              horizontal: 'right',
            }}
            open={Boolean(settingsAnchorEl)}
            onClose={handleSettingsClose}
          >
            <MenuItem onClick={() => handleRoute('/mooclet')}>Add MOOClet</MenuItem>
            <MenuItem onClick={handleSettingsClose}>Add Person</MenuItem>
          </Menu>
        </div>
      </div>
      <br style={{ clear: 'both' }} />
      <div style={{ display: 'flex' }}>
        <h3 style={{ marginLeft: '1%', marginRight: '50%' }}>MOOClets</h3>
        <h3>People</h3>
      </div>
      <div style={{ display: 'flex', alignItems: 'start' }}>
        {MOOClets.map((MOOCletInfo) => {
          return (
            <Card key={uid(MOOCletInfo)} sx={{ width: '15%', marginLeft: '1%', marginRight: '1%' }}>
              <CardActionArea onClick={() => handleRoute('/moocletdashboard')}>
                <CardMedia component="img" height="140" image="logo192.png" alt="green iguana" />
                <CardContent>
                  <Typography gutterBottom variant="h5" component="div">
                    {MOOCletInfo.name}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Policy: {MOOCletInfo.policy}
                  </Typography>
                </CardContent>
              </CardActionArea>
            </Card>
          );
        })}
        <Card sx={{ maxWidth: '15%', marginRight: '1%', marginLeft: '23%', display: 'flex' }}>
          <CardMedia component="img" sx={{ width: '50%' }} image="logo192.png" />
          <Box sx={{ display: 'flex', flexDirection: 'column' }}>
            <CardContent sx={{ flex: '1 0 auto' }}>
              <Typography component="div" variant="h5">
                John Doe
              </Typography>
              <Typography variant="subtitle1" color="text.secondary" component="div">
                Owner
              </Typography>
            </CardContent>
          </Box>
        </Card>
        <Card sx={{ maxWidth: '15%', marginRight: '1%', display: 'flex' }}>
          <CardMedia component="img" sx={{ width: '50%' }} image="logo192.png" />
          <Box sx={{ display: 'flex', flexDirection: 'column' }}>
            <CardContent sx={{ flex: '1 0 auto' }}>
              <Typography component="div" variant="h5">
                Jane Smith
              </Typography>
              <Typography variant="subtitle1" color="text.secondary" component="div">
                Staff
              </Typography>
            </CardContent>
          </Box>
        </Card>
      </div>
      <MOOCletCreator
        submitCallback={(name: string, policy: number) => {
          setMOOClets((oldArray) => [...oldArray, { name: name, policy: policy }]);
        }}
      />
    </>
  );
}
