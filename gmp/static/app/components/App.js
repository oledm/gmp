import React from 'react'
import { connect } from 'react-redux'
import Toolbar from '../components/Toolbar'
import LoginRegisterForm from '../components/forms/LoginRegisterForm'
import { logout } from '../actions/index'

class App extends React.Component {
    render() {
        const { isAuthenticated, handleClick, children } = this.props
        return (
            <div>
                <Toolbar isAuthenticated={isAuthenticated} handleClick={handleClick} />
                    { children }
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
