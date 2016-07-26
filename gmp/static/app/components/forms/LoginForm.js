import React, { Component, PropTypes } from 'react'
import { reduxForm } from 'redux-form'
import InputText from '../inputs/InputText'
import LoginValidation from './LoginValidation'
import { login } from '../../actions/index'

const fields = [ 'email', 'password' ]

const submit = (values, dispatch) => {
    return new Promise((resolve, reject) => {
        dispatch(login(values))
        resolve()
    })
}

class LoginForm extends Component {

    render() {
        const { fields: { email, password },
            valid, handleSubmit, submitting } = this.props
      
        return (
            <form onSubmit={handleSubmit(this.props.submit.bind(this))}>
                    <div className="row">
                        <InputText
                            className="col-md-offset-1 col-md-10 col-lg-offset-2 col-lg-8"
                            label="E-mail"
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

                    <div className="row">
                      <div className="col-md-offset-1 col-md-10 col-lg-offset-2 col-lg-8">
                          <button className="btn btn-primary" type="submit" disabled={submitting || !valid}>
                            {submitting ? <i/> : <i/>} Войти
                          </button>
                      </div>
                    </div>
            </form>
        )
    }
}

LoginForm.propTypes = {
    fields: PropTypes.object.isRequired,
    handleSubmit: PropTypes.func.isRequired,
    submitting: PropTypes.bool.isRequired,
    valid: PropTypes.bool.isRequired
}

const mapDispatchToProps = dispatch => ({
    submit
})

export default reduxForm({
    form: 'Login',
    fields,
    validate: LoginValidation,
},
    null,
    mapDispatchToProps
)(LoginForm)
