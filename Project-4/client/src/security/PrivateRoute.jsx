import React, {useEffect, useState} from "react";
import {Outlet, Navigate} from "react-router-dom";
import {makeHTTPRequest} from "../utils/http";

const PrivateRoute = () => {
	const [auth, setAuth] = useState(null);
	const [loading, setLoading] = useState(true);

	useEffect(() => {
		const getAuth = async () => {
			try {
				const response = await makeHTTPRequest(
					"GET",
                    // Figure out the path later
					"/"
				);
				setAuth(response.data.code);
			} catch (error) {
				console.error(error);
			} finally {
				setLoading(false);
			}
		};

		getAuth();
	}, []);

	if (loading) {
		return null;
	}
	return auth ? <Outlet /> : <Navigate to='/login' />;
};

export default PrivateRoute;
