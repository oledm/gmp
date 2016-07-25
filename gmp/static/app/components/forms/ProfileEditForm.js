import React, { Component, PropTypes } from 'react'
import { reduxForm } from 'redux-form'
import InputText from '../inputs/InputText'
import RegisterValidation from './RegisterValidation'
import { register } from '../../actions/index'

const fields = [ 'last_name', 'first_name', 'middle_name', 'password' ]

const submit = (values, dispatch) => {
    return new Promise((resolve, reject) => {
        dispatch(register(values))
        resolve()
    })
}

class RegisterForm extends Component {

    render() {
        const { fields: { last_name, first_name, middle_name, password },
            valid, handleSubmit, submitting } = this.props
      
        return (
            <form onSubmit={handleSubmit(this.props.submit.bind(this))}>
                <div className="form-group">
                    <div className="row">
                        <InputText
                            className="col-md-offset-1 col-md-10 col-lg-offset-2 col-lg-8"
                            label="Фамилия"
                            icon="user"
                            type="text"
                            {...last_name}
                        />
                    </div>
                    <div className="row">
                        <InputText
                            className="col-md-offset-1 col-md-10 col-lg-offset-2 col-lg-8"
                            label="Имя"
                            icon="user"
                            type="text"
                            {...first_name}
                        />
                    </div>
                    <div className="row">
                        <InputText
                            className="col-md-offset-1 col-md-10 col-lg-offset-2 col-lg-8"
                            label="Отчество"
                            icon="user"
                            type="text"
                            {...middle_name}
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
                            {submitting ? <i/> : <i/>} Сохранить
                          </button>
                      </div>
                    </div>
                </div>
            </form>
        )
    }
}

RegisterForm.propTypes = {
    fields: PropTypes.object.isRequired,
    handleSubmit: PropTypes.func.isRequired,
    submitting: PropTypes.bool.isRequired,
    valid: PropTypes.bool.isRequired
}

const mapDispatchToProps = dispatch => ({
    submit
})

export default reduxForm({
    form: 'Register',
    fields,
    validate: RegisterValidation,
},
    null,
    mapDispatchToProps
)(RegisterForm)
