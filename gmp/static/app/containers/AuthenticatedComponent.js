import React from 'react'
import { withRouter } from 'react-router'
import { connect } from 'react-redux'
import { redirectTo } from '../actions/index'

const requireAuthentication = Component => {
    class AuthenticatedComponent extends React.Component {
        componentWillMount() {
            this.checkAuth(this.props.isAuthenticated);
        }

        componentWillReceiveProps(nextProps) {
            this.checkAuth(nextProps.isAuthenticated);
        }

        checkAuth(isAuthenticated) {
            if (!isAuthenticated) {
                this.props.dispatch(redirectTo('/login'));
            }
        }

        render() {
            return (
                <div>
                    {this.props.isAuthenticated
                        ? <Component {...this.props} />
                        : null
                    }
                </div>
            )
        }
    }


    const mapStateToProps = state => ({
        isAuthenticated: state.auth.isAuthenticated
    })

    return withRouter(connect(mapStateToProps)(AuthenticatedComponent))
}

export default requireAuthentication
