import { TextField, Button, Container, Grid } from '@mui/material';
import React, { useState } from 'react';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';

const NewListingModal = ({handleClose}) =>{
    const [name, setName] = useState("");
    const [descr, setDescr] = useState("");
    const [price, setPrice] = useState(1.0);
    const [endDate, setEndDate] = useState(null);
    const [photo, setPhoto] = useState(null);

    const handleName = (e) => {
        setName(e.target.value);
    };

    const handleDescr = (e) =>{
        setDescr(e.target.value);
    };

    const handlePrice = (e) =>{
        setPrice(e.target.value);
    };

    const handleDate = (date) =>{
        setEndDate(date);
    };

    const sendData = async () =>{
    //     Send http
        const response = await fetch('http://localhost:8080/create-listing', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                item_name: name,
                item_description: descr,
                end_date: endDate,
                price: price,
            }),
            credentials: "include",
        });
        if (!response.ok) {
            console.log(response.ok)
            throw new Error('User was not registered');
        }
        handleClose();
    }

    const handlePhoto = (event) => {
        const file = event.target.files[0];
        setPhoto(file);
    };

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
                <input type="file" accept="image/*" onChange={handlePhoto} />
            </Grid>
            <Grid item xs={12}>
                <TextField
                    label="Item Name"
                    required
                    type="text"
                    variant="outlined"
                    value={name}
                    onChange={handleName}
                />
            </Grid>
            <Grid item xs={12}>
                <TextField
                    label="Item Description"
                    required
                    type="text"
                    variant="outlined"
                    onChange={handleDescr}
                    value={descr}
                    multiline
                    rows={4}
                />
            </Grid>
            <Grid item xs={12}>
                <TextField
                    label="Price"
                    required
                    type="number"
                    variant="outlined"
                    onChange={handlePrice}
                    value={price}
                />
            </Grid>
            <Grid item xs={12}>
                <h2>Select Auction End Date</h2>
                <DatePicker
                    selected={endDate}
                    onChange={handleDate}
                    showTimeSelect
                    dateFormat="Pp"
                />
            </Grid>
            <Grid item xs={6}>
                <Button
                    onClick={sendData}
                    variant="contained"
                    color="primary"
                    sx={{ width: '150px', height: '50px'}}
                >
                    Create Listing
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

export default NewListingModal