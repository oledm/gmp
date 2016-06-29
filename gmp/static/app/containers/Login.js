import React, { Component } from 'react'
import { connect } from 'react-redux'
//import { withRouter } from 'react-router'
import TabLink from '../components/TabLink'
import LoginRegisterForm from '../components/forms/LoginRegisterForm'
import LoginForm from '../components/forms/LoginForm'

class Login extends Component {
  render() {
    const { isAuthenticated } = this.props

    return (
            <LoginRegisterForm>
                <LoginForm />
            </LoginRegisterForm>
    )
  }
}

const mapStateToProps = state => ({
    isAuthenticated: state.auth.isAuthenticated
})


export default connect(mapStateToProps)(Login)
