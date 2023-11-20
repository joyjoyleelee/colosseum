import React, { useState } from 'react'
import Navbar from '../components/Navbar'
import StaticListing from "../components/winnings/StaticListing";
//import axios from "axios";

const Winnings = () => {

    // Temporary list for items in auctions won
    const tempPropsList = [
        {
            image: "favicon.ico",
            title: "Child Slave",
            description: "straight from Mongolia",
            price: 1000,
            end: 202311012359, // YYYYMMDD, time (military)
            bidder: "none",
        },
        {
            image: "favicon.ico",
            title: "Adult Slave",
            description: "straight from Czech Republic",
            price: 3000,
            end: 202311012359, // YYYYMMDD, time (military)
            bidder: "none",
        },
    ];

    // //Creating listings object for populating
    // const [listings, setListings] = useState([])
    //
    // // Code below to populate the listings
    // axios.post('/', {}) //Fill in path for winnings listing
    //     .then(function (response) {
    //         setListings(response);
    //         console.log(response);
    //     })
    //     .catch(function (error) {
    //         console.log('Populating winnings listing did not work: ', error);
    //     });

    return (
        <>
            <Navbar></Navbar>
            <div style={{ display: 'flex', gap: '20px', marginTop: '20px' }}>
                {tempPropsList.map((tempProp, index) => (
                    <StaticListing key={index} {...tempProp} />
                ))}
            </div>
        </>
    )
}

export default Winnings