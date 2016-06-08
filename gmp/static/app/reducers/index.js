import { combineReducers } from 'redux'
import { reducer as formReducer } from 'redux-form';
import departments from './departments'
import auth from './auth'

const rootReducer = combineReducers({
    departments,
    auth,
    form: formReducer,
})

export default rootReducer
