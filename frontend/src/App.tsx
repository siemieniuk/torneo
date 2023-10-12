import React from 'react'
import {
  Route,
  Routes,
  BrowserRouter
} from 'react-router-dom'
import { useState } from 'react'

import Home from "./components/layout/Home"
import Register from "./components/Register"
import NoPage from "./components/NoPage"
import Layout from "./components/layout/Layout"
import Login from "./components/Login"
import axios from 'axios'

axios.defaults.withCredentials = true;

const serverUrl = process.env.REACT_APP_SERVER_URL

export type GlobalContent = {
  isAuthenticated: boolean,
  setIsAuthenticated: (b: boolean) => void
}

export const GlobalContext = React.createContext<GlobalContent>({
  isAuthenticated: false,
  setIsAuthenticated: () => { },
})

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false)

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Home />} />
          <Route path="register" element={<Register />} />
          <Route path="login" element={<Login />} />
          <Route path="*" element={<NoPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App;
