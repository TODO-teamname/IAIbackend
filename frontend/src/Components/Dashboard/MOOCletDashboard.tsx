import * as React from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import IconButton from '@mui/material/IconButton';
import AccountCircle from '@mui/icons-material/AccountCircle';
import People from '@mui/icons-material/People';
import MenuItem from '@mui/material/MenuItem';
import Menu from '@mui/material/Menu';
import Drawer from '@mui/material/Drawer';
import List from '@mui/material/List';
import Divider from '@mui/material/Divider';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
import ListItemIcon from '@mui/material/ListItemIcon';
import DownloadIcon from '@mui/icons-material/Download';
import AddToDriveIcon from '@mui/icons-material/AddToDrive';
import axios from 'axios';
import DataView from '../DataView/DataView';
import { useHistory } from 'react-router-dom';
import { useEffect } from 'react';

const BASE_URL = 'http://127.0.0.1:8000/api/';

export default function MOOCletDashboard(): JSX.Element {
  const [currentSelection, setCurrentSelection] = React.useState('Please select a MOOClet');
  const [auth] = React.useState(true);
  const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null);

  //   const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
  //     setAuth(event.target.checked);
  //   };

  const handleMenu = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };
  const history = useHistory();

  const handleRoute = (pagePath: string) => {
    history.push(pagePath);
  };
  const [currentDataName, setCurrentDataName] = React.useState<string>('');
  const [currentDataPolicy, setCurrentDataPolicy] = React.useState<number>(0);

  const handleSubmit = (e: React.MouseEvent<HTMLElement>): void => {
    console.log('clicked button');
    e.preventDefault();
    axios.get(BASE_URL + 'mooclet/?mooclet_id=' + '106').then((res) => {
      console.log(res.data.name, res.data.policy);
      setCurrentDataName(currentDataName + res.data.name);
      setCurrentDataPolicy(() => res.data.policy);
      // React.useEffect(() => {
      //   setCurrentDataName(res.data.name);
      // }, [res.data.name]);
      console.log(currentDataName, currentDataPolicy);
    });
  };

  const drawerWidth = '15%';
  return (
    <>
      <Box sx={{ flexGrow: 1 }}>
        <AppBar position="fixed" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}>
          <Toolbar>
            <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
              MOOClet Dashboard
            </Typography>
            {auth && (
              <div>
                <IconButton
                  size="large"
                  aria-label="organizations of current user"
                  aria-haspopup="true"
                  color="inherit"
                >
                  <People />
                </IconButton>
                <IconButton
                  size="large"
                  aria-label="account of current user"
                  aria-controls="menu-appbar"
                  aria-haspopup="true"
                  onClick={handleMenu}
                  color="inherit"
                >
                  <AccountCircle />
                </IconButton>
                <Menu
                  id="menu-appbar"
                  anchorEl={anchorEl}
                  anchorOrigin={{
                    vertical: 'top',
                    horizontal: 'right',
                  }}
                  keepMounted
                  transformOrigin={{
                    vertical: 'top',
                    horizontal: 'right',
                  }}
                  open={Boolean(anchorEl)}
                  onClose={handleClose}
                >
                  <MenuItem onClick={handleClose}>My Account</MenuItem>
                  <MenuItem onClick={() => handleRoute('/login')}>Sign Out</MenuItem>
                </Menu>
                <Menu
                  id="menu-appbar"
                  anchorEl={anchorEl}
                  anchorOrigin={{
                    vertical: 'top',
                    horizontal: 'right',
                  }}
                  keepMounted
                  transformOrigin={{
                    vertical: 'top',
                    horizontal: 'right',
                  }}
                  open={Boolean(anchorEl)}
                  onClose={handleClose}
                >
                  <MenuItem onClick={handleClose}>My Account</MenuItem>
                  <MenuItem onClick={handleClose}>Sign Out</MenuItem>
                </Menu>
              </div>
            )}
          </Toolbar>
        </AppBar>
        <Drawer
          variant="permanent"
          sx={{
            width: drawerWidth,
            flexShrink: 0,
            [`& .MuiDrawer-paper`]: { width: drawerWidth, boxSizing: 'border-box' },
          }}
        >
          <Toolbar />
          <Box sx={{ overflow: 'auto' }}>
            <List>
              <ListItem button onClick={(e) => handleSubmit(e)}>
                <ListItemText primary={'MOOClet'} />
              </ListItem>
            </List>
            <Divider />
          </Box>
        </Drawer>
        <div style={{ marginLeft: '17%', marginTop: '5%' }}>
          <DataView
            moocletID={106}
            organizationID={0}
            moocletName={currentDataName}
            moocletPolicy={currentDataPolicy}
          />
        </div>
        <Drawer
          variant="permanent"
          anchor="right"
          sx={{
            width: drawerWidth,
            flexShrink: 0,
            [`& .MuiDrawer-paper`]: { width: drawerWidth, boxSizing: 'border-box' },
          }}
        >
          <Toolbar />
          <Box sx={{ overflow: 'auto' }}>
            <List>
              <ListItem>
                <ListItemText primary={currentSelection} />
              </ListItem>
            </List>
            <Divider />
            <List>
              <ListItem button>
                <ListItemText primary={'Download CSV'} />
                <ListItemIcon>{<DownloadIcon />}</ListItemIcon>
              </ListItem>
            </List>
            <Divider />
            <List>
              <ListItem button>
                <ListItemText primary={'Export to Google Drive'} />
                <ListItemIcon>{<AddToDriveIcon />}</ListItemIcon>
              </ListItem>
            </List>
            <Divider />
          </Box>
        </Drawer>
      </Box>
    </>
  );
}
