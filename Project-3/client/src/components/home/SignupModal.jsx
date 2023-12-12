import { TextField, Button, Container, Grid } from '@mui/material';
import React, { useState } from 'react';

const SignupModal = ({handleClose}) =>{
    const [usernames,setUser] = useState('')
    const [passwords, setPass] = useState('')

    const handleUser = (e) => {
        setUser(e.target.value);
    };

    const handlePass = (e) => {
        setPass(e.target.value);
    };

    const sendData = async () =>{
        //TODO: Implement send to backend
        //User http://locahost:8080/register when testing locally
        const response = await fetch('http://localhost:8080/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: usernames,
                password: passwords,
            }),
        });
        if (!response.ok) {
            console.log(response.ok)
            throw new Error('User was not registered');
        }
        const responseData = await response.json();
        console.log(responseData);
        handleClose();
    }

    return (
        <Container maxWidth="auto"
                   style={{ display: 'flex',
                       alignItems: 'center',
                       justifyContent: 'center',
                       backgroundColor: 'lightgrey',
                       minHeight: 'auto',
                       padding:'10px',}}>
            <Grid container spacing={2}>
            <Grid item xs={12}>
                <TextField
                    label="Username"
                    required
                    type="text"
                    variant="outlined"
                    value={usernames}
                    onChange={handleUser}
                />
            </Grid>
            <Grid item xs={12}>
                <TextField
                    label="Password"
                    required
                    type="password"
                    variant="outlined"
                    onChange={handlePass}
                    value={passwords}
                />
            </Grid>
            <Grid item xs={6}>
                <Button
                    onClick={sendData}
                    variant="contained"
                    color="primary"
                    sx={{ width: '150px', height: '50px'}}
                >
                    Register
                </Button>
            </Grid>
            <Grid item xs={6}>
                <Button
                    onClick={handleClose}
                    variant="contained"
                    color="primary"
                    sx={{ width: '150px', height: '50px'}}
                >
                    Cancel
                </Button>
            </Grid>
        </Grid>
    </Container>
    );
};

export default SignupModal