import React, {useEffect, useState} from "react";
import {Badge, Card, CardActionArea, CardContent, CardMedia,
    Modal, Typography, Box, Button, TextField,} from "@mui/material";
import NewListingModal from "./NewListingModal";


const NewListingButton = (props) => {
    const [listOpen, setList] = useState(false);

    const handleLogOpen = () =>{
        setList(true);
    };

    const handleLogClose = () => {
        setList (false);
    };

    const handleNewBid = async () => {
        handleLogOpen();
        // const response = await fetch('http://localhost:8080/create-listing', {
        //     method: 'POST',
        //     headers: {
        //         'Content-Type': 'application/json',
        //     },
        //     body: JSON.stringify({
        //         item_name: "Child slave",
        //         item_description: "Straight from Mongolia, well disciplined",
        //         start_date: "filler",
        //         end_date: "???",
        //         price: 1230.0,
        //     }),
        // });
        // if (!response.ok) {
        //     console.log(response.ok)
        //     throw new Error('User was not registered');
        // }
    };
    return (
            <>
                <Button
                    sx={{
                        position: 'absolute',
                        right: 5,
                        top: 80,
                        width: '150px',
                        height: '50px',
                    }}
                    variant="contained"
                    color="primary"
                    onClick={handleNewBid}
                >
                    Make New Listing
                </Button>
                <Modal
                open={listOpen}
                aria-labelledby='modal-title'
                aria-describedby='modal-description'>
                    <div>
                        <NewListingModal open={listOpen} handleClose={handleLogClose} />
                    </div>
             </Modal>
            </>
        );

}

export default NewListingButton