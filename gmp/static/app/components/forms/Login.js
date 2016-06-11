import React, { Component, PropTypes } from 'react'
import { reduxForm } from 'redux-form'
import InputText from '../inputs/InputText'
import LoginValidation from './LoginValidation'
import { login } from '../../actions/index'

const fields = [ 'email', 'password' ]

const submit = (values, dispatch) => {
    console.log(values)
    return new Promise((resolve, reject) => {
        dispatch(login(values))
        resolve()
    })
}

class Login extends Component {
  render() {
    const { fields: { email, password },
        valid, handleSubmit, submitting } = this.props

    return (
        <form onSubmit={handleSubmit(this.props.createPost.bind(this))}>
            <div className="form-group">
                <div className="row">
                    <InputText
                        className="col-md-offset-1 col-md-10 col-lg-offset-2 col-lg-8"
                        label="Email"
                        icon="user"
                        type="email"
                        {...email}
                    />
                </div>
                <div className="row">
                    <InputText
                        className="col-md-offset-1 col-md-10 col-lg-offset-2 col-lg-8"
                        label="Пароль"
                        icon="lock"
                        type="password"
                        {...password}
                    />
                </div>
            </div>
            <div className="form-group">
                <div className="row">
                  <div className="col-md-offset-1 col-md-10 col-lg-offset-2 col-lg-8">
                      <button className="btn btn-primary" type="submit" disabled={submitting || !valid}>
                        {submitting ? <i/> : <i/>} Войти
                      </button>
                  </div>
                </div>
            </div>
        </form>
    )
  }
}

Login.propTypes = {
    fields: PropTypes.object.isRequired,
    handleSubmit: PropTypes.func.isRequired,
    submitting: PropTypes.bool.isRequired
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
)(Login)
