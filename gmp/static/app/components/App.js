import React from 'react'
import { connect } from 'react-redux'
import Toolbar from '../components/Toolbar'
import LoginRegisterForm from '../components/forms/LoginRegisterForm'
import { logout } from '../actions/index'

class App extends React.Component {
    static onEnter(nextState, replace) {
        const loggedIn = localStorage.getItem('auth_token')
        if (loggedIn === null && nextState.location.pathname !== '/login') {
            console.log('NEED login')
            replace({
                pathname: '/login',
                state: { nextPathname: nextState.location.pathname }
            })
        }
    }

    render() {
        const { isAuthenticated, handleClick, children } = this.props
        return (
            <div>
                <Toolbar isAuthenticated={isAuthenticated} handleClick={handleClick} />
                <LoginRegisterForm isAuthenticated={isAuthenticated}>
                    { children }
                </LoginRegisterForm>
            </div>
        )
    }
}

const mapStateToProps = state => ({
    isAuthenticated: state.auth.isAuthenticated
})

const mapDispatchToProps = dispatch => ({
    handleClick: () => dispatch(logout())
})

export default connect(mapStateToProps, mapDispatchToProps)(App)
