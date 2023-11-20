import React from 'react';
import { AppBar, Toolbar, Button, Typography } from '@mui/material';
import { Link } from 'react-router-dom';

const Navbar = () => {
    const handleLogout = () => {
        // Add your logout logic here

        console.log('Logging out...');
    };

    return (
        <AppBar position="static">
            <Toolbar>
                <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                    My Auction App
                </Typography>
                <Button color="inherit" component={Link} to="/Auction">
                    Auction
                </Button>
                <Button color="inherit" component={Link} to="/Winnings">
                    Auctions Won
                </Button>
                <Button color="inherit" component={Link} to="/MyAuction">
                    Auctions Posted
                </Button>
                <Button color="inherit" onClick={handleLogout} component={Link} to="/">
                    Logout
                </Button>
            </Toolbar>
        </AppBar>
    );
};

export default Navbar;