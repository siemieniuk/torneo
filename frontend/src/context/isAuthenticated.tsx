const isAuthenticated = () => {
    return localStorage.getItem('access-token') !== "" && localStorage.getItem('access-token') !== null
}

export default isAuthenticated;