import React from "react"
import { Outlet } from "react-router-dom"
import Header from "./Header"
import Footer from "./Footer"

function Layout(): JSX.Element {
  return (
    <>
      <Header />
      <div className="container vh-100">
        <Outlet />
      </div>
      <Footer />
    </>
  )
}

export default Layout;