import React, { Component, PropTypes } from 'react'
import { reduxForm } from 'redux-form'
import { bindActionCreators } from 'redux'
import InputText from '../inputs/InputText'
import DepartmentSelector from '../../containers/DepartmentSelector'
import LoginValidation from './LoginValidation'
import { login } from '../../actions/index'

//const fields = [ 'username', 'email', 'age', 'department' ]
const fields = [ 'username', 'department' ]

const submit = (values, dispatch) => {
    console.log(values)
    return new Promise((resolve, reject) => {
        dispatch(login()).then(response)
    })
}


class LoginForm extends Component {
  render() {
//    const { fields: { username, email, age, department },
    const { fields: { username, department },
        resetForm, valid, handleSubmit, submitting } = this.props

    return (<form onSubmit={handleSubmit(this.props.createPost.bind(this))}>
        {valid ? <p>Form is valid!</p> : <p>Form INVALID!</p> }
        <div className="row">
            <InputText className="col-xs-6" label="Имя пользователя" {...username} />
        </div>
        <div className="row">
            <DepartmentSelector className="col-xs-6" label="Отдел" {...department} />
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
//            <InputText className="col-xs-6" label="E-mail" {...email} />
//            <InputText className="col-xs-6" label="Возраст" {...age} />

LoginForm.propTypes = {
  fields: PropTypes.object.isRequired,
  handleSubmit: PropTypes.func.isRequired,
  resetForm: PropTypes.func.isRequired,
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
)(LoginForm)
