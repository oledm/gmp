import AddTodoForm from '../components/AddTodoForm'
import { connect } from 'react-redux'
import { fetchDepartments } from '../actions/index'

const mapDispatchToProps = (dispatch) => {
    return {
//        onSubmit: text => dispatch(addTodo(text))
        onSubmit: text => dispatch(fetchDepartments())
    }
}

const AddTodo = connect(null, mapDispatchToProps)(AddTodoForm)

export default AddTodo
