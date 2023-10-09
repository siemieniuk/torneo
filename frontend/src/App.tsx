import {
  Route,
  Routes,
  BrowserRouter
} from 'react-router-dom'
import Home from "./components/Home"
import Register from "./components/Register"
import NoPage from "./components/NoPage"
import Layout from "./components/Layout"
import Login from "./components/Login"
import axios from 'axios'

axios.defaults.withCredentials = true;

const serverUrl = process.env.REACT_APP_SERVER_URL

function App() {
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
