import React, { Component, PropTypes } from 'react'
import { reduxForm } from 'redux-form'
import InputText from '../inputs/InputText'
import LoginValidation from './LoginValidation'

const fields = [ 'username', 'email', 'age' ]
const onSubmit = data => console.log('onSubmit:', data) 

class LoginForm extends Component {
  render() {
    const { fields: { username, email, age }, resetForm, valid, handleSubmit, submitting } = this.props

    return (<form onSubmit={handleSubmit(onSubmit)}>
        {valid ? <p>Form is valid!</p> : <p>Form INVALID!</p> }
        <div className="row">
            <InputText className="col-xs-6" label="Имя пользователя" {...username} />
            <InputText className="col-xs-6" label="E-mail" {...email} />
        </div>
        <div className="row">
            <InputText className="col-xs-3" label="Возраст" {...age} />
        </div>
        <div>
          <button className="btn btn-primary" type="submit" disabled={submitting || !valid}>
            {submitting ? <i/> : <i/>} Submit
          </button>
          <button className="btn" type="button" disabled={submitting} onClick={resetForm}>
            Clear Values
          </button>
        </div>
      </form>
    )
  }
}

LoginForm.propTypes = {
  fields: PropTypes.object.isRequired,
  handleSubmit: PropTypes.func.isRequired,
  resetForm: PropTypes.func.isRequired,
  submitting: PropTypes.bool.isRequired
}

export default reduxForm({
  form: 'Login',
  fields,
  validate: LoginValidation,
})(LoginForm)



