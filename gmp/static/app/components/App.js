import React from 'react'
import { connect } from 'react-redux'
import { withRouter } from 'react-router'
import Toolbar from '../components/Toolbar'
import LoginRegisterForm from '../components/forms/LoginRegisterForm'
import { logout, redirectTo } from '../actions/index'

class App extends React.Component {
    componentWillMount() {
        const { location: {pathname}, isAuthenticated, redirectTo } = this.props;
        const pathForAuthentication = (pathname === '/login' || pathname === '/register');

        if ( pathForAuthentication && isAuthenticated ) {
            redirectTo('/');
        }
    }

    render() {
        const { isAuthenticated, user, handleClick, children } = this.props
        return (
            <div>
                <Toolbar
                    isAuthenticated={isAuthenticated}
                    handleClick={() => handleClick()}
                    user={user}
                />
                { children }
            </div>
        )
    }
}

const mapStateToProps = state => ({
    isAuthenticated: state.auth.isAuthenticated,
    user: state.auth.user
})

export default withRouter(connect(
    mapStateToProps,
    {
        handleClick: logout,
        redirectTo
    }
)(App))
