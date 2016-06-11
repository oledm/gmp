import React from 'react'
import { connect } from 'react-redux'
import Toolbar from '../components/Toolbar'
import LoginRegisterForm from '../components/forms/LoginRegisterForm'
import { logout } from '../actions/index'

const App = ({ isAuthenticated, handleClick, children }) => (
    <div>
        <Toolbar isAuthenticated={isAuthenticated} handleClick={handleClick} />
        <LoginRegisterForm isAuthenticated={isAuthenticated}>
            { children }
        </LoginRegisterForm>
    </div>
)

const mapStateToProps = state => ({
    isAuthenticated: state.auth.isAuthenticated
})

const mapDispatchToProps = dispatch => ({
    handleClick: () => dispatch(logout())
})

export default connect(mapStateToProps, mapDispatchToProps)(App)
