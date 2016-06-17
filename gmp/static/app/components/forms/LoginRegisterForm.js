import React, { Component, PropTypes } from 'react'
import { reduxForm } from 'redux-form'
import InputText from '../inputs/InputText'
import LoginValidation from './LoginValidation'
import { login } from '../../actions/index'
import TabLink from '../TabLink'

const fields = [ 'email', 'password' ]

const submit = (values, dispatch) => {
    console.log(values)
    return new Promise((resolve, reject) => {
        dispatch(login(values))
        resolve()
    })
}

class LoginRegisterForm extends Component {

    componentWillReceiveProps(nextProps) {
        if (this.props.isAuthenticated) {
            this.context.router.push('/')
        }
    }

    render() {
        const { isAuthenticated, fields: { email, password },
            valid, handleSubmit, submitting } = this.props
      
        if (isAuthenticated) {
            return null
        }
      
        return (
            <div>
                <ul className="nav nav-tabs">
                    <TabLink to="/login">Вход</TabLink>
                    <TabLink to="/register">Регистрация</TabLink>
                </ul>
      
                {this.props.children}
            </div>
        )
    }
}

LoginRegisterForm.propTypes = {
    isAuthenticated: PropTypes.bool.isRequired,
    fields: PropTypes.object.isRequired,
    handleSubmit: PropTypes.func.isRequired,
    submitting: PropTypes.bool.isRequired
}

LoginRegisterForm.contextTypes = {
    router: PropTypes.object.isRequired
}

const mapDispatchToProps = dispatch => ({
    createPost: submit
})

export default reduxForm({
    form: 'Login',
    fields,
    validate: LoginValidation,
},
    null,
    mapDispatchToProps
)(LoginRegisterForm)
